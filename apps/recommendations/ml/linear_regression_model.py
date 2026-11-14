from apps.recommendations.interfaces.i_regression_model import IRegressionModel
from django.conf import settings
import joblib

class LinearRegressionModel(IRegressionModel):
    def __init__(self):
        model_path = (
                settings.BASE_DIR
                / "artifacts"
                / "linear_regression_model.joblib"
        )

        self.__model = joblib.load(model_path)

    def predict(self, features):
        return self.__model.predict(features)