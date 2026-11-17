from unittest import TestCase
from unittest.mock import Mock

from apps.recommendations.services.content_candidate_source import ContentCandidateSource
from apps.recommendations.services.collaborative_candidate_source import CollaborativeCandidateSource
from .helpers import genre, history_entry, user, work


class ContentCandidateSourceTests(TestCase):
    def setUp(self):
        self.current_user = user(tracked_ids=[1])
        self.action = genre(1, "Action")
        self.fantasy = genre(2, "Fantasy")
        self.drama = genre(3, "Drama")
        self.tracked = Mock()
        self.works = Mock()

    def _configure(self, history, candidates):
        history_qs = Mock()
        history_qs.prefetch_related.return_value = history
        self.tracked.objects.filter.return_value = history_qs

        filtered = Mock()
        excluded = Mock()
        distinct = Mock()
        self.works.filter.return_value = filtered
        filtered.exclude.return_value = excluded
        excluded.distinct.return_value = distinct
        distinct.prefetch_related.return_value = candidates

    def test_ranks_positive_genres_and_ignores_negative_ones(self):
        self._configure(
            history=[
                history_entry(work(1, [self.action]), 9),
                history_entry(work(2, [self.fantasy]), 8),
                history_entry(work(3, [self.drama]), 2),
            ],
            candidates=[
                work(10, [self.fantasy]),
                work(20, [self.action, self.fantasy]),
                work(30, [self.drama]),
            ],
        )
        source = ContentCandidateSource(self.works, self.tracked)
        result = source.get_candidates(self.current_user, limit=3)
        self.assertEqual([w.pk for w in result], [20, 10])
        self.works.filter.assert_called_once_with(genres__pk__in=[1, 2])

    def test_without_ratings_returns_empty(self):
        self._configure(history=[], candidates=[])
        source = ContentCandidateSource(self.works, self.tracked)
        self.assertEqual(source.get_candidates(self.current_user, limit=10), [])
        self.works.filter.assert_not_called()

    def test_without_positively_rated_genres_returns_empty(self):
        self._configure(
            history=[history_entry(work(1, [self.drama]), 2)],
            candidates=[],
        )
        source = ContentCandidateSource(self.works, self.tracked)
        self.assertEqual(source.get_candidates(self.current_user, limit=10), [])
        self.works.filter.assert_not_called()


class CollaborativeCandidateSourceTests(TestCase):
    def setUp(self):
        self.current_user = user(tracked_ids=[1, 2, 3])
        self.tracked = Mock()
        self.works = Mock()
        self.works.values.return_value = [{"pk": pk} for pk in (4, 5, 6)]
        self.works.filter.return_value = [work(4), work(5), work(6)]

    def _configure_queries(self, own, shared=None, neighbor_recommendations=None):
        own_qs = Mock()
        own_qs.values_list.return_value = own
        shared_qs = Mock()
        shared_qs.exclude.return_value = shared_qs
        shared_qs.values_list.return_value = shared or []
        candidate_qs = Mock()
        candidate_qs.exclude.return_value = candidate_qs
        candidate_qs.values_list.return_value = neighbor_recommendations or []
        self.tracked.objects.filter.side_effect = [own_qs, shared_qs, candidate_qs]

    def test_recommends_works_from_similar_neighbors_only(self):
        self._configure_queries(
            own=[(1, 9), (2, 8), (3, 7)],
            shared=[
                (10, 1, 9), (10, 2, 8), (10, 3, 7),
                (11, 1, 7), (11, 2, 8), (11, 3, 9),
            ],
            neighbor_recommendations=[
                (10, 4, 9), (10, 5, 7), (10, 6, 10),
            ],
        )
        source = CollaborativeCandidateSource(self.works, self.tracked)
        result = source.get_candidates(self.current_user, limit=2)
        self.assertEqual([w.pk for w in result], [6, 4])
        self.assertEqual(self.tracked.objects.filter.call_count, 3)

    def test_short_history_gives_no_collaborative_candidates(self):
        self._configure_queries(own=[(1, 9), (2, 8)])
        source = CollaborativeCandidateSource(self.works, self.tracked, min_common=3)
        self.assertEqual(source.get_candidates(self.current_user, limit=10), [])
        self.assertEqual(self.tracked.objects.filter.call_count, 1)

    def test_no_valid_pearson_neighbors_returns_empty(self):
        self._configure_queries(
            own=[(1, 8), (2, 8), (3, 8)],
            shared=[(10, 1, 8), (10, 2, 9), (10, 3, 10)],
        )
        source = CollaborativeCandidateSource(self.works, self.tracked)
        self.assertEqual(source.get_candidates(self.current_user, limit=10), [])
        self.assertEqual(self.tracked.objects.filter.call_count, 2)
