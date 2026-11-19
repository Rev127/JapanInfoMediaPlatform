from collections import defaultdict
import numpy as np

from apps.recommendationSystem.interfaces.i_candidate_source import (
    ICandidateSource
)


class CollaborativeCandidateSource(ICandidateSource):

    def __init__(
        self,
        works,
        tracked_work_model,
        min_common=3,
        max_neighbors=30
    ):
        self.works = works
        self.tracked_work_model = tracked_work_model
        self.min_common = min_common
        self.max_neighbors = max_neighbors

    def get_candidates(self, user, limit):

        # 1. Оцінки поточного користувача
        own_ratings = dict(
            self.tracked_work_model.objects
            .filter(
                user=user,
                rating__isnull=False
            )
            .values_list("work_id", "rating")
        )

        if len(own_ratings) < self.min_common:
            return []

        # 2. Знаходимо інших користувачів,
        # які оцінювали ті самі медіапродукти
        shared_ratings = (
            self.tracked_work_model.objects
            .filter(
                work_id__in=own_ratings.keys(),
                rating__isnull=False
            )
            .exclude(user=user)
            .values_list(
                "user_id", "work_id", "rating"
            )
        )

        neighbor_history = defaultdict(dict)

        for user_id, work_id, rating in shared_ratings:
            neighbor_history[user_id][work_id] = rating

        # 3. Обчислюємо схожість користувачів
        similarities = []

        for neighbor_id, ratings in neighbor_history.items():
            common = sorted(
                own_ratings.keys() & ratings.keys()
            )

            if len(common) < self.min_common:
                continue

            x = np.array(
                [own_ratings[i] for i in common],
                dtype=np.float32
            )
            y = np.array(
                [ratings[i] for i in common],
                dtype=np.float32
            )

            x -= x.mean()
            y -= y.mean()

            denominator = (
                np.linalg.norm(x) *
                np.linalg.norm(y)
            )

            if denominator == 0:
                continue

            similarity = float(
                np.dot(x, y) / denominator
            )

            # Зменшуємо вплив малого перетину
            similarity *= (
                len(common) / (len(common) + 10)
            )

            if similarity > 0:
                similarities.append(
                    (similarity, neighbor_id)
                )

        similarities.sort(reverse=True)

        neighbors = dict(
            (neighbor_id, similarity)
            for similarity, neighbor_id
            in similarities[:self.max_neighbors]
        )

        if not neighbors:
            return []

        # 4. Отримуємо високо оцінені твори сусідів
        excluded_ids = set(
            user.tracking_works.values_list(
                "pk", flat=True
            )
        )

        ratings = (
            self.tracked_work_model.objects
            .filter(
                user_id__in=neighbors.keys(),
                rating__gte=7,
                work_id__in=self.works.values("pk")
            )
            .exclude(work_id__in=excluded_ids)
            .values_list(
                "user_id", "work_id", "rating"
            )
        )

        scores = defaultdict(float)
        weights = defaultdict(float)
        support = defaultdict(int)

        for neighbor_id, work_id, rating in ratings:
            similarity = neighbors[neighbor_id]

            scores[work_id] += similarity * (rating - 5.5)
            weights[work_id] += similarity
            support[work_id] += 1

        # 5. Ранжуємо кандидатів
        def candidate_score(work_id):
            average = scores[work_id] / weights[work_id]
            confidence = support[work_id] / (
                support[work_id] + 2
            )
            return average * confidence

        ranked_ids = sorted(
            scores,
            key=lambda work_id: (
                -candidate_score(work_id),
                work_id
            )
        )[:limit]

        works_by_id = {
            work.pk: work
            for work in self.works.filter(
                pk__in=ranked_ids
            )
        }

        return [
            works_by_id[work_id]
            for work_id in ranked_ids
            if work_id in works_by_id
        ]