from unittest import TestCase
from unittest.mock import Mock, patch

import numpy as np
from scipy.sparse import csr_matrix

import apps.recommendationSystem.services.recommendation_engine as engine_module
from apps.recommendationSystem.services.recommendation_engine import RecommendationEngine
from apps.recommendationSystem.services.recommendation_service import RecommendationService
from .helpers import user, work


class RecommendationEngineTests(TestCase):
    def setUp(self):
        self.current_user = user(tracked_ids=[1])
        self.candidate_generator = Mock()
        self.profile_builder = Mock()
        self.profile_builder.build_user_profile.return_value = np.array([1.0, 2.0])
        self.features_builder = Mock()
        self.features_builder.build.side_effect = (
            lambda _profile, w: csr_matrix([[float(w.pk)]])
        )
        self.tracked_model = Mock()
        self.linear_model = Mock()
        self.xgboost_model = Mock()
        self.popularity_source = Mock()
        self.engine = RecommendationEngine(
            candidate_generator=self.candidate_generator,
            user_profile_builder=self.profile_builder,
            features_builder=self.features_builder,
            tracked_work_model=self.tracked_model,
            strategies=[(5, self.linear_model), (100, self.xgboost_model)],
            popularity_source=self.popularity_source,
            candidate_limit=10,
        )

    def test_strategy_selection_at_thresholds(self):
        self.assertIsNone(self.engine._select_strategy(4))
        self.assertIs(self.engine._select_strategy(5), self.linear_model)
        self.assertIs(self.engine._select_strategy(99), self.linear_model)
        self.assertIs(self.engine._select_strategy(100), self.xgboost_model)
        self.assertIs(self.engine._select_strategy(300), self.xgboost_model)

    def test_empty_strategy_list_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "хоча б одну"):
            RecommendationEngine(
                self.candidate_generator,
                self.profile_builder,
                self.features_builder,
                self.tracked_model,
                [],
                self.popularity_source,
            )

    def test_recommend_predicts_once_and_sorts_top_n(self):
        self.engine._get_user_history = Mock(return_value=[object()] * 6)
        self.engine._build_user_profile = Mock(return_value=np.array([1.0, 2.0]))
        self.candidate_generator.generate.return_value = [work(101), work(102), work(103)]
        self.linear_model.predict.return_value = np.array([7.9, 9.1, 8.3])

        with patch.object(engine_module, "prefetch_related_objects"):
            ranked = self.engine.recommend(self.current_user, top_n=2)

        self.assertEqual([w.pk for w, _rating in ranked], [102, 103])
        self.assertEqual([rating for _w, rating in ranked], [9.1, 8.3])
        self.candidate_generator.generate.assert_called_once_with(
            self.current_user, limit=10
        )
        self.linear_model.predict.assert_called_once()
        self.xgboost_model.predict.assert_not_called()
        X = self.linear_model.predict.call_args.args[0]
        self.assertEqual(X.shape, (3, 1))

    def test_cold_start_uses_popularity_and_excludes_tracked(self):
        self.engine._get_user_history = Mock(return_value=[])
        self.popularity_source.get_candidates.return_value = [
            work(1), work(2), work(2), work(3)
        ]
        result = self.engine.recommend(self.current_user, top_n=2)
        self.assertEqual([(w.pk, r) for w, r in result], [(2, None), (3, None)])
        self.candidate_generator.generate.assert_not_called()
        self.linear_model.predict.assert_not_called()

    def test_empty_candidate_list_uses_popularity(self):
        self.engine._get_user_history = Mock(return_value=[object()] * 5)
        self.engine._build_user_profile = Mock(return_value=np.array([1.0, 2.0]))
        self.candidate_generator.generate.return_value = []
        self.popularity_source.get_candidates.return_value = [work(10)]
        result = self.engine.recommend(self.current_user, top_n=1)
        self.assertEqual([(w.pk, r) for w, r in result], [(10, None)])

    def test_predict_rating_excludes_target_from_history(self):
        candidate = work(77)
        self.engine._get_user_history = Mock(return_value=[object()] * 5)
        self.engine._build_user_profile = Mock(return_value=np.array([1.0, 2.0]))
        self.linear_model.predict.return_value = np.array([8.7])

        with patch.object(engine_module, "prefetch_related_objects"):
            rating = self.engine.predict_rating(self.current_user, candidate)

        self.assertAlmostEqual(rating, 8.7)
        self.engine._get_user_history.assert_called_once_with(
            self.current_user, exclude_work_id=77
        )
        self.linear_model.predict.assert_called_once()

    def test_predict_rating_without_enough_history_returns_none(self):
        self.engine._get_user_history = Mock(return_value=[object()] * 4)
        self.assertIsNone(self.engine.predict_rating(self.current_user, work(77)))
        self.linear_model.predict.assert_not_called()

    def test_invalid_model_prediction_is_rejected(self):
        self.engine._get_user_history = Mock(return_value=[object()] * 5)
        self.engine._build_user_profile = Mock(return_value=np.array([1.0, 2.0]))
        self.candidate_generator.generate.return_value = [work(4)]
        self.linear_model.predict.return_value = np.array([np.nan])
        with patch.object(engine_module, "prefetch_related_objects"):
            with self.assertRaisesRegex(ValueError, "некоректні прогнози"):
                self.engine.recommend(self.current_user, top_n=1)

    def test_wrong_number_of_predictions_is_rejected(self):
        self.engine._get_user_history = Mock(return_value=[object()] * 5)
        self.engine._build_user_profile = Mock(return_value=np.array([1.0, 2.0]))
        self.candidate_generator.generate.return_value = [work(4), work(5)]
        self.linear_model.predict.return_value = np.array([8.0])
        with patch.object(engine_module, "prefetch_related_objects"):
            with self.assertRaisesRegex(ValueError, "Кількість прогнозів"):
                self.engine.recommend(self.current_user, top_n=2)

    def test_nonpositive_top_n_returns_empty_without_queries(self):
        self.assertEqual(self.engine.recommend(self.current_user, top_n=0), [])
        self.tracked_model.objects.filter.assert_not_called()


class RecommendationServiceTests(TestCase):
    def test_delegates_to_recommendation_engine(self):
        engine = Mock()
        expected = [(work(7), 9.2)]
        engine.recommend.return_value = expected
        service = RecommendationService(engine)

        result = service.get_recommendations(user(), limit=3)

        self.assertIs(result, expected)
        engine.recommend.assert_called_once()
        self.assertEqual(engine.recommend.call_args.args[1], 3)
