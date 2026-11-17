from apps.recommendations.interfaces.i_regression_model import IRegressionModel
from django.conf import settings
import joblib
from pathlib import Path

class GradientBoostingRecommendationModel(IRegressionModel):
    def __init__(self):
        model_path = (
                Path(settings.BASE_DIR)
                / "apps/recommendations/ml/artifacts/gradient_boosting.joblib"
        )

        if not model_path.is_file():
            raise FileNotFoundError(
                f"ML model not found: {model_path}"
            )

        self.__model = joblib.load(model_path)

    def predict(self, features):
        return self.__model.predict(features)