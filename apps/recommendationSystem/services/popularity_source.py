
from django.db.models import (
    Avg,
    Count,
    ExpressionWrapper,
    F,
    FloatField,
    Value,
)

from apps.recommendationSystem.interfaces.i_candidate_source import (
    ICandidateSource
)


class PopularityCandidateSource(ICandidateSource):

    def __init__(
        self,
        works,
        tracked_work_model,
        prior_weight=10
    ):
        self.works = works
        self.tracked_work_model = tracked_work_model

        if prior_weight <= 0:
            raise ValueError(
                "prior_weight має бути додатним"
            )

        self.prior_weight = prior_weight

    def get_candidates(self, user, limit):
        if limit <= 0:
            return []

        # 1. Виключаємо відстежувані твори
        excluded_ids = user.tracking_works.values_list(
            "pk", flat=True
        )

        available_works = self.works.exclude(
            pk__in=excluded_ids
        )

        # 2. Оцінки всіх допустимих творів
        all_ratings = (
            self.tracked_work_model.objects
            .filter(
                rating__isnull=False,
                work_id__in=self.works.values("pk")
            )
        )

        # Середній рейтинг каталогу
        global_mean = all_ratings.aggregate(
            mean=Avg("rating")
        )["mean"]

        ranked_ids = []

        # 3. Якщо є оцінки, розраховуємо
        # байєсівський рейтинг
        if global_mean is not None:
            m = self.prior_weight
            C = float(global_mean)

            ranked_ids = list(
                all_ratings
                .exclude(work_id__in=excluded_ids)
                .values("work_id")
                .annotate(
                    rating_count=Count("pk"),
                    avg_rating=Avg("rating")
                )
                .annotate(
                    weighted_rating=ExpressionWrapper(
                        (
                            F("rating_count") * F("avg_rating")
                            + Value(m * C)
                        ) / (
                            F("rating_count") + Value(m)
                        ),
                        output_field=FloatField()
                    )
                )
                .order_by(
                    "-weighted_rating",
                    "-rating_count",
                    "work_id"
                )
                .values_list("work_id", flat=True)[:limit]
            )

        # 4. Якщо оцінених творів недостатньо,
        # доповнюємо за кількістю відстежувань
        remaining = limit - len(ranked_ids)

        if remaining > 0:
            tracked_ids = list(
                self.tracked_work_model.objects
                .filter(
                    work_id__in=available_works.values("pk")
                )
                .exclude(work_id__in=ranked_ids)
                .values("work_id")
                .annotate(
                    tracking_count=Count("pk")
                )
                .order_by(
                    "-tracking_count",
                    "work_id"
                )
                .values_list(
                    "work_id", flat=True
                )[:remaining]
            )

            ranked_ids.extend(tracked_ids)

        # 5. Якщо взаємодій взагалі недостатньо,
        # доповнюємо списком з каталогу
        remaining = limit - len(ranked_ids)

        if remaining > 0:
            fallback_ids = list(
                available_works
                .exclude(pk__in=ranked_ids)
                .order_by("pk")
                .values_list(
                    "pk", flat=True
                )[:remaining]
            )

            ranked_ids.extend(fallback_ids)

        # 6. Отримуємо Work у правильному порядку
        works_by_id = self.works.in_bulk(ranked_ids)

        return [
            works_by_id[work_id]
            for work_id in ranked_ids
            if work_id in works_by_id
        ]
