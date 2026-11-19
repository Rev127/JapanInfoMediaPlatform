from apps.recommendationSystem.interfaces.i_candidate_source import ICandidateSource

from collections import defaultdict


class ContentCandidateSource(ICandidateSource):

    def __init__(self, works, tracked_work_model):
        self.works = works
        self.tracked_work_model = tracked_work_model

    def get_candidates(self, user, limit):
        history = (
            self.tracked_work_model.objects
            .filter(user=user, rating__isnull=False)
            .prefetch_related("work__genre")
        )

        genre_scores = defaultdict(list)

        for entry in history:
            for genre in entry.work.genre.all():
                genre_scores[genre.pk].append(entry.rating)

        if not genre_scores:
            return []

        genre_affinity = {
            genre_id: (
                sum(ratings) / len(ratings) - 5.5
            )
            for genre_id, ratings in genre_scores.items()
        }

        preferred_genres = [
            genre_id
            for genre_id, score in genre_affinity.items()
            if score > 0
        ]

        if not preferred_genres:
            return []

        works = (
            self.works
            .filter(genre__pk__in=preferred_genres)
            .exclude(
                pk__in=user.tracking_works.values("pk")
            )
            .distinct()
            .prefetch_related("genre")
        )

        candidates = []

        for work in works:
            genres = list(work.genre.all())

            # Середня відповідність жанрів
            score = sum(
                genre_affinity.get(genre.pk, 0)
                for genre in genres
            ) / max(len(genres), 1)

            if score > 0:
                candidates.append((score, work))

        candidates.sort(
            key=lambda item: (-item[0], item[1].pk)
        )

        return [
            work for score, work in candidates[:limit]
        ]
