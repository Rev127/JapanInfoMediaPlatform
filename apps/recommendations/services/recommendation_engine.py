
import numpy as np

from scipy.sparse import vstack
from django.db.models import prefetch_related_objects

from apps.recommendations.interfaces.i_recommendation_engine import (
    IRecommendationEngine
)
from apps.recommendations.services.candidate_generator import CandidateGenerator
from apps.recommendations.services.features_builder import FeaturesBuilder
from apps.recommendations.services.user_profile_builder import UserProfileBuilder


class RecommendationEngine(IRecommendationEngine):
    def __init__(
        self,
        candidate_generator: CandidateGenerator,
        user_profile_builder: UserProfileBuilder,
        features_builder: FeaturesBuilder,
        tracked_work_model,
        strategies,
        popularity_source,
        candidate_limit=100,
    ):
        self._candidate_generator = candidate_generator
        self._user_profile_builder = user_profile_builder
        self._features_builder = features_builder
        self._tracked_work_model = tracked_work_model
        self._popularity_source = popularity_source
        self._candidate_limit = candidate_limit

        if not strategies:
            raise ValueError(
                "Потрібно передати хоча б одну ML-стратегію"
            )

        # [(мінімальна історія, модель), ...]
        self._strategies = sorted(
            strategies,
            key=lambda item: item[0],
            reverse=True
        )

        self._min_history = min(
            threshold for threshold, _ in self._strategies
        )

    def _get_user_history(self, user, exclude_work_id=None):
        history = (
            self._tracked_work_model.objects
            .filter(
                user=user,
                rating__isnull=False
            )
            .select_related("work")
            .prefetch_related("work__genre")
        )

        if exclude_work_id is not None:
            history = history.exclude(
                work_id=exclude_work_id
            )

        return list(history)

    def _build_user_profile(self, history):
        user_ratings = [
            {
                "rating": entry.rating,
                "genre": list(
                    entry.work.genre.all()
                )
            }
            for entry in history
        ]

        return self._user_profile_builder.build_user_profile(
            user_ratings
        )

    def _select_strategy(self, history_size):
        for min_history, strategy in self._strategies:
            if history_size >= min_history:
                return strategy

        return None

    def _get_popular_recommendations(self, user, top_n):
        excluded_ids = set(
            user.tracking_works.values_list(
                "pk", flat=True
            )
        )

        works = self._popularity_source.get_candidates(
            user,
            max(top_n * 3, top_n)
        )

        recommendations = []
        seen = set(excluded_ids)

        for work in works:
            if work.pk in seen:
                continue

            recommendations.append((work, None))
            seen.add(work.pk)

            if len(recommendations) >= top_n:
                break

        return recommendations

    def predict_rating(self, user, work):
        history = self._get_user_history(
            user,
            exclude_work_id=work.pk
        )

        strategy = self._select_strategy(len(history))

        if strategy is None:
            return None

        user_profile = self._build_user_profile(history)

        prefetch_related_objects([work], "genre")

        features = self._features_builder.build(
            user_profile,
            work
        )

        predictions = np.asarray(
            strategy.predict(features)
        ).ravel()

        if len(predictions) != 1:
            raise ValueError(
                "Модель повинна повернути один прогноз"
            )

        rating = float(predictions[0])

        if not np.isfinite(rating):
            raise ValueError("Некоректний прогноз моделі")

        return rating

    def recommend(self, user, top_n=10):
        if top_n <= 0:
            return []

        history = self._get_user_history(user)

        strategy = self._select_strategy(len(history))

        if strategy is None:
            print("нема стратегії")
            return self._get_popular_recommendations(
                user, top_n
            )

        user_profile = self._build_user_profile(history)

        candidates = self._candidate_generator.generate(
            user,
            limit=max(self._candidate_limit, top_n)
        )

        if not candidates:
            return self._get_popular_recommendations(
                user, top_n
            )

        candidates = list(candidates)
        prefetch_related_objects(candidates, "genre")

        feature_matrices = [
            self._features_builder.build(
                user_profile,
                work
            )
            for work in candidates
        ]

        X = vstack(
            feature_matrices,
            format="csr"
        )

        predictions = np.asarray(
            strategy.predict(X)
        ).ravel()

        if len(predictions) != len(candidates):
            raise ValueError(
                "Кількість прогнозів не відповідає "
                "кількості кандидатів"
            )

        if not np.isfinite(predictions).all():
            raise ValueError(
                "Модель повернула некоректні прогнози"
            )

        ranked = sorted(
            zip(candidates, predictions),
            key=lambda pair: (
                -float(pair[1]),
                pair[0].pk
            )
        )

        return [
            (work, float(predicted_rating))
            for work, predicted_rating in ranked[:top_n]
        ]
