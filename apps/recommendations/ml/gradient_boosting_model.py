from apps.recommendations.interfaces.i_regression_model import IRegressionModel
from django.conf import settings
import joblib

class GradientBoostingRecommendationModel(IRegressionModel):
    def __init__(self):
        model_path = (
                settings.BASE_DIR
                / "artifacts"
                / "gradient_boosting.joblib"
        )

        self.__model = joblib.load(model_path)

    def predict(self, features):
        return self.__model.predict(features)