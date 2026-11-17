import abc

class IRecommendationEngine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def recommend(self, user, limit=10):
        pass

    @abc.abstractmethod
    def predict_rating(self, user, work):
        pass