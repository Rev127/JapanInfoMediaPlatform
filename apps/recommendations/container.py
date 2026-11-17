# apps/recommendations/container.py

from functools import lru_cache
from pathlib import Path
import joblib

from apps.mediaProducts.models import Work
from apps.recommendations.ml.gradient_boosting_model import GradientBoostingRecommendationModel
from apps.recommendations.ml.linear_regression_model import LinearRegressionRecommendationModel
from apps.recommendations.services.candidate_generator import CandidateGenerator
from apps.recommendations.services.collaborative_candidate_source import CollaborativeCandidateSource
from apps.recommendations.services.content_candidate_source import ContentCandidateSource
from apps.recommendations.services.features_builder import FeaturesBuilder
from apps.recommendations.services.genre_mapper import GenreMapper
from apps.recommendations.services.popularity_source import PopularityCandidateSource
from apps.recommendations.services.recommendation_engine import RecommendationEngine
from apps.recommendations.services.recommendation_service import RecommendationService
from apps.recommendations.services.user_profile_builder import UserProfileBuilder
from apps.user.models import TrackedWork


# Тут імпортуємо наші компоненти:
# RecommendationService, RecommendationEngine,
# CandidateGenerator, UserProfileBuilder,
# FeaturesBuilder, GenreMapper,
# ContentCandidateSource, CollaborativeCandidateSource,
# PopularityCandidateSource, TrackedWork, Work,
# LinearRegressionRecommendationModel,
# GradientBoostingRecommendationModel.


@lru_cache(maxsize=1)
def get_recommendation_service():
    artifacts = (
        Path(__file__).resolve().parent
        / "ml"
        / "artifacts"
    )

    # 1. Завантажуємо preprocessing
    mlb = joblib.load(
        artifacts / "multilabel_binarizer.joblib"
    )
    tfidf = joblib.load(
        artifacts / "tfidf_vectorizer.joblib"
    )

    # 2. Створюємо компоненти підготовки ознак
    genre_mapper = GenreMapper(mlb)

    user_profile_builder = UserProfileBuilder(
        genre_mapper=genre_mapper,
        multilabel_binarizer=mlb
    )

    features_builder = FeaturesBuilder(
        mlb=mlb,
        tfidf=tfidf,
        genre_mapper=genre_mapper
    )

    # 3. Створюємо джерела кандидатів
    # У реальному проєкті works потрібно
    # обмежити лише аніме.
    works = Work.objects.all()

    content_source = ContentCandidateSource(
        works=works,
        tracked_work_model=TrackedWork
    )

    collaborative_source = CollaborativeCandidateSource(
        works=works,
        tracked_work_model=TrackedWork
    )

    candidate_generator = CandidateGenerator([
        content_source,
        collaborative_source
    ])

    # 4. Створюємо ML-стратегії
    linear_model = LinearRegressionRecommendationModel()
    gradient_model = GradientBoostingRecommendationModel()

    # 5. Створюємо резервне джерело
    popularity_source = PopularityCandidateSource(
        works=works,
        tracked_work_model=TrackedWork
    )

    # 6. Створюємо RecommendationEngine
    engine = RecommendationEngine(
        candidate_generator=candidate_generator,
        user_profile_builder=user_profile_builder,
        features_builder=features_builder,
        tracked_work_model=TrackedWork,
        strategies=[
            (5, linear_model),
            (150, gradient_model)
        ],
        popularity_source=popularity_source
    )

    # 7. Створюємо фасад
    return RecommendationService(engine)