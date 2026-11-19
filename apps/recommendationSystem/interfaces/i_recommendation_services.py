import abc

class IRecommendationService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_recommendations(self, user, limit):
        pass
