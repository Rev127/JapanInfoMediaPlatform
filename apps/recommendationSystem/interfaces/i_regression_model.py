import abc

class IRegressionModel(abc.ABC):
    @abc.abstractmethod
    def predict(self, features):
        pass