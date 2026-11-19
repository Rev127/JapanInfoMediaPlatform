from apps.recommendationSystem.interfaces.i_recommendation_services import IRecommendationService
from apps.recommendationSystem.interfaces.i_recommendation_engine import IRecommendationEngine


class RecommendationService(IRecommendationService):
    def __init__(self, engine: IRecommendationEngine):
        self._engine = engine

    def get_recommendations(self, user, limit):
        result = self._engine.recommend(user, limit)
        print(result)
        return result