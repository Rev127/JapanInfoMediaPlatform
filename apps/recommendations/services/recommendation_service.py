from apps.recommendations.interfaces.i_recommendation_services import IRecommendationService


class RecommendationService(IRecommendationService):
    def __init__(self, engine):
        self._engine = engine

    def recommend(self, user, limit):
        return self._engine.recommend(user, limit)