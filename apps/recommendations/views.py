from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

class RecommendationsView(LoginRequiredMixin, TemplateView):
    template_name = "recomendation.html"

    service_provider = None

    default_limit = 10
    max_limit = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Отримуємо кількість рекомендацій
        raw_limit = self.request.GET.get("limit")

        try:
            limit = (
                int(raw_limit)
                if raw_limit is not None
                else self.default_limit
            )
        except (ValueError, TypeError):
            limit = self.default_limit

        limit = max(1, min(limit, self.max_limit))

        if self.service_provider is None:
            raise ImproperlyConfigured(
                "Не налаштовано провайдер RecommendationService"
            )

        # Отримуємо сервіс через DI
        service = self.service_provider()

        # Отримуємо рекомендації для поточного користувача
        results = service.get_recommendations(
            user=self.request.user,
            limit=limit
        )

        # Перетворюємо результат у зручний формат
        recommendations = [
            {
                "work": work,
                "predicted_rating": rating
            }
            for work, rating in results
        ]

        context["recommendations"] = recommendations
        context["limit"] = limit

        return context

