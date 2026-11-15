
class CandidateGenerator:
    def __init__(self, sources):
        self.sources = sources

    def generate(self, user, limit=100):
        candidates = {}
        for source in self.sources:
            results = source.get_candidates(user, int(limit / len(self.sources)))

            for candidate in results:
                candidates[candidate.pk] = candidate

        viewed_ids = set(
            user.tracking_works.values_list("pk", flat=True)
        )

        return [
            work
            for work_id, work in candidates.items()
            if work_id not in viewed_ids
        ][:limit]
