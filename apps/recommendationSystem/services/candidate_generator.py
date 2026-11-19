
class CandidateGenerator:
    def __init__(self, sources):
        self.sources = sources

    def generate(self, user, limit=100):
        if limit <= 0 or not self.sources:
            return []

        excluded_ids = set(
            user.tracking_works.values_list(
                "pk", flat=True
            )
        )

        base, remainder = divmod(
            limit, len(self.sources)
        )

        candidates = []
        seen = set(excluded_ids)

        for index, source in enumerate(self.sources):
            source_limit = base + (
                1 if index < remainder else 0
            )

            if source_limit == 0:
                continue

            results = source.get_candidates(
                user, source_limit
            )

            for candidate in results:
                if candidate.pk not in seen:
                    seen.add(candidate.pk)
                    candidates.append(candidate)

        return candidates[:limit]
