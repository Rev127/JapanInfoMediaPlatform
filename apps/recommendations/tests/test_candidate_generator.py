from unittest import TestCase
from unittest.mock import Mock

from apps.recommendations.services.candidate_generator import CandidateGenerator
from .helpers import user, work


class CandidateGeneratorTests(TestCase):
    def test_combines_sources_removes_duplicates_and_tracked_works(self):
        current_user = user(tracked_ids=[1])
        source_a = Mock()
        source_b = Mock()
        source_a.get_candidates.return_value = [work(1), work(2), work(3)]
        source_b.get_candidates.return_value = [work(3), work(4)]

        result = CandidateGenerator([source_a, source_b]).generate(current_user, 6)

        self.assertEqual([w.pk for w in result], [2, 3, 4])
        source_a.get_candidates.assert_called_once_with(current_user, 3)
        source_b.get_candidates.assert_called_once_with(current_user, 3)

    def test_odd_limit_is_distributed_without_losing_a_slot(self):
        """Regression-test: старий int(limit / N) недобирає кандидатів."""
        current_user = user()
        first, second = Mock(), Mock()
        first.get_candidates.side_effect = lambda _u, n: [work(i) for i in range(1, n + 1)]
        second.get_candidates.side_effect = lambda _u, n: [work(i) for i in range(20, 20 + n)]

        result = CandidateGenerator([first, second]).generate(current_user, limit=3)

        self.assertEqual(len(result), 3)
        first.get_candidates.assert_called_once_with(current_user, 2)
        second.get_candidates.assert_called_once_with(current_user, 1)

    def test_no_sources_returns_empty_list(self):
        """Без джерел метод повертає порожній список."""
        self.assertEqual(CandidateGenerator([]).generate(user(), limit=10), [])

    def test_nonpositive_limit_returns_empty_without_calling_sources(self):
        source = Mock()
        source.get_candidates.return_value = []
        result = CandidateGenerator([source]).generate(user(), limit=0)
        self.assertEqual(result, [])
        source.get_candidates.assert_not_called()
