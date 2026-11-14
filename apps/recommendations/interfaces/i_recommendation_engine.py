import abc

class IRecommendationEngine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def recommend(self, user, limit):
        pass
    @abc.abstractmethod
    def get_recommendation(self, user, limit):
        pass