import abc


class ICandidateSource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_candidates(self, user, limit):
        pass