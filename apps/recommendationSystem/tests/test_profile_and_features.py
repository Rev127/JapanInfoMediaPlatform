from unittest import TestCase
from unittest.mock import Mock

import numpy as np
from scipy.sparse import csr_matrix, issparse
from sklearn.preprocessing import MultiLabelBinarizer

from apps.recommendationSystem.services.genre_mapper import GenreMapper
from apps.recommendationSystem.services.user_profile_builder import UserProfileBuilder
from apps.recommendationSystem.services.features_builder import FeaturesBuilder
from .helpers import genre, work


class GenreMapperTests(TestCase):
    def setUp(self):
        self.mlb = MultiLabelBinarizer(classes=["Action", "Fantasy", "Romance"])
        self.mlb.fit([[]])
        self.mapper = GenreMapper(self.mlb)

    def test_maps_genres_and_removes_duplicates(self):
        result = self.mapper.map_genres([
            genre(1, "Action", "Екшен"),
            genre(2, "Fantasy", "Фентезі"),
            genre(3, "Action", "Екшен"),
        ])
        self.assertEqual(result, ["Action", "Fantasy"])

    def test_missing_ml_name_raises_clear_error(self):
        with self.assertRaisesRegex(ValueError, "не має ML-відповідника"):
            self.mapper.map_genres([genre(1, None, "Невідомий жанр")])

    def test_unknown_ml_name_raises_error(self):
        with self.assertRaisesRegex(ValueError, "Невідомий ML-жанр"):
            self.mapper.map_genres([genre(1, "Mecha")])


class UserProfileBuilderTests(TestCase):
    def setUp(self):
        self.mlb = MultiLabelBinarizer(classes=["Action", "Fantasy", "Romance"])
        self.mlb.fit([[]])
        self.mapper = GenreMapper(self.mlb)
        self.action = genre(1, "Action")
        self.fantasy = genre(2, "Fantasy")

    def test_calculates_mean_genre_ratings_and_preserves_fill_values(self):
        """Regression-test: self.fill_value vs self.fill_values."""
        builder = UserProfileBuilder(
            self.mapper, self.mlb,
            fill_values={"Action": 6, "Fantasy": 5, "Romance": 4.5},
        )
        result = builder.build_user_profile([
            {"rating": 9, "genres": [self.action, self.fantasy]},
            {"rating": 5, "genres": [self.action]},
        ])
        np.testing.assert_allclose(result, [7, 9, 4.5])
        self.assertEqual(result.shape, (3,))

    def test_default_scalar_fill_value_is_supported(self):
        """Regression-test: параметр fill_values=0 не індексується."""
        builder = UserProfileBuilder(self.mapper, self.mlb)
        result = builder.build_user_profile([])
        np.testing.assert_allclose(result, [0, 0, 0])

    def test_no_ratings_returns_fallbacks_unchanged(self):
        builder = UserProfileBuilder(
            self.mapper, self.mlb,
            fill_values={"Action": 5, "Fantasy": 6, "Romance": 7},
        )
        np.testing.assert_allclose(builder.build_user_profile([]), [5, 6, 7])


class FeaturesBuilderTests(TestCase):
    def setUp(self):
        # Саме 42 + 42 + 5000 ознак, як у поточній реалізації.
        self.names = [f"Genre{i:02d}" for i in range(42)]
        self.mlb = MultiLabelBinarizer(classes=self.names)
        self.mlb.fit([[]])
        self.mapper = GenreMapper(self.mlb)
        self.tfidf = Mock()
        self.text_vector = csr_matrix(
            (np.array([2.5]), (np.array([0]), np.array([12]))),
            shape=(1, 5000),
        )
        self.tfidf.transform.return_value = self.text_vector
        self.builder = FeaturesBuilder(self.mlb, self.tfidf, self.mapper)

    def test_builds_correct_feature_order_and_sparse_shape(self):
        profile = np.arange(42, dtype=np.float32)
        candidate = work(
            10, [genre(1, self.names[1]), genre(2, self.names[3])],
            ml_description="An English synopsis",
        )
        X = self.builder.build(profile, candidate)

        self.assertTrue(issparse(X))
        self.assertEqual(X.shape, (1, 5084))
        np.testing.assert_allclose(X.toarray()[0, :42], profile)
        self.assertEqual(X.toarray()[0, 42 + 1], 1)
        self.assertEqual(X.toarray()[0, 42 + 3], 1)
        self.assertEqual(X.toarray()[0, 84 + 12], 2.5)
        self.tfidf.transform.assert_called_once_with(["An English synopsis"])

    def test_missing_description_is_transformed_as_empty_string(self):
        self.builder.build(np.zeros(42), work(11, [], ml_description=None))
        self.tfidf.transform.assert_called_once_with([""])

    def test_incorrect_feature_count_raises(self):
        self.tfidf.transform.return_value = csr_matrix((1, 10))
        with self.assertRaisesRegex(ValueError, "Некоректна кількість ознак"):
            self.builder.build(np.zeros(42), work(11))
