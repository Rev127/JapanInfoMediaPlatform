from django.urls import path

from apps.recommendations.views import RecommendationsView
from apps.recommendations.container import (
    get_recommendation_service
)

app_name = "recommendations"

urlpatterns = [
    path(
        "",
        RecommendationsView.as_view(
            service_provider=get_recommendation_service
        ),
        name="recommendations"
    )
]