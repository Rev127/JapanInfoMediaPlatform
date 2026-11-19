from django.urls import path

from apps.recommendationSystem.views import RecommendationsView
from apps.recommendationSystem.container import container
app_name = "recommendationSystem"

urlpatterns = [
    path(
        "recommendation",
        RecommendationsView.as_view(
            service_provider=container.recommendation_service
        ),
        name="recommendationSystem"
    )
]