
# apps/recommendationSystem/container.py

from pathlib import Path
import joblib

from dependency_injector import containers, providers

from apps.mediaProducts.models import Work
from apps.recommendationSystem.services.strategy_elector import StrategySelector
from apps.user.models import TrackedWork

from apps.recommendationSystem.ml.linear_regression_model import (
    LinearRegressionRecommendationModel
)
from apps.recommendationSystem.ml.gradient_boosting_model import (
    GradientBoostingRecommendationModel
)

from apps.recommendationSystem.services.candidate_generator import CandidateGenerator
from apps.recommendationSystem.services.collaborative_candidate_source import CollaborativeCandidateSource
from apps.recommendationSystem.services.content_candidate_source import ContentCandidateSource
from apps.recommendationSystem.services.popularity_source import PopularityCandidateSource
from apps.recommendationSystem.services.features_builder import FeaturesBuilder
from apps.recommendationSystem.services.genre_mapper import GenreMapper
from apps.recommendationSystem.services.user_profile_builder import UserProfileBuilder
from apps.recommendationSystem.services.recommendation_engine import RecommendationEngine
from apps.recommendationSystem.services.recommendation_service import RecommendationService


ARTIFACTS = Path(__file__).resolve().parent / "ml" / "artifacts"


def strategy_rule(min_history, model):
    return (min_history, model)


class RecommendationContainer(containers.DeclarativeContainer):

    # 1. Завантаження ML-артефактів
    mlb = providers.Singleton(
        joblib.load,
        ARTIFACTS / "multilabel_binarizer.joblib"
    )

    tfidf = providers.Singleton(
        joblib.load,
        ARTIFACTS / "tfidf_vectorizer.joblib"
    )

    # 2. Підготовка ознак
    genre_mapper = providers.Factory(
        GenreMapper,
        multilabel_binarizer=mlb
    )

    user_profile_builder = providers.Factory(
        UserProfileBuilder,
        genre_mapper=genre_mapper,
        multilabel_binarizer=mlb
    )

    features_builder = providers.Factory(
        FeaturesBuilder,
        mlb=mlb,
        tfidf=tfidf,
        genre_mapper=genre_mapper
    )

    # 3. Доступ до медіапродуктів
    works = providers.Callable(
        Work.objects.all
    )

    # 4. Джерела кандидатів
    content_source = providers.Factory(
        ContentCandidateSource,
        works=works,
        tracked_work_model=TrackedWork
    )

    collaborative_source = providers.Factory(
        CollaborativeCandidateSource,
        works=works,
        tracked_work_model=TrackedWork
    )

    popularity_source = providers.Factory(
        PopularityCandidateSource,
        works=works,
        tracked_work_model=TrackedWork
    )

    candidate_generator = providers.Factory(
        CandidateGenerator,
        sources=providers.List(
            content_source,
            collaborative_source
        )
    )

    # 5. ML-моделі
    linear_model = providers.Singleton(
        LinearRegressionRecommendationModel
    )

    gradient_model = providers.Singleton(
        GradientBoostingRecommendationModel
    )

    strategy_rules = providers.List(
        providers.Callable(
            strategy_rule, 5, linear_model
        ),
        providers.Callable(
            strategy_rule, 150, gradient_model
        )
    )

    strategy_selector = providers.Factory(
        StrategySelector,
        strategies=strategy_rules
    )

    # 6. Рекомендаційний рушій
    recommendation_engine = providers.Factory(
        RecommendationEngine,
        candidate_generator=candidate_generator,
        user_profile_builder=user_profile_builder,
        features_builder=features_builder,
        tracked_work_model=TrackedWork,
        strategy_selector=strategy_selector,
        popularity_source=popularity_source,
        candidate_limit=100
    )

    # 7. Сервіс / Facade
    recommendation_service = providers.Factory(
        RecommendationService,
        engine=recommendation_engine
    )


# Один екземпляр контейнера в межах процесу
container = RecommendationContainer()
