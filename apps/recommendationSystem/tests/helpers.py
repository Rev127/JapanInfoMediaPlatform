"""Невеликі тестові об'єкти, без звернень до реальної бази Django."""
from types import SimpleNamespace
from unittest.mock import Mock


def genre(pk, ml_name, name=None):
    return SimpleNamespace(pk=pk, ml_name=ml_name, name=name or ml_name)


def work(pk, genres=(), ml_description="", title=None):
    related = Mock()
    related.all.return_value = list(genres)
    return SimpleNamespace(
        pk=pk,
        title=title or f"Work {pk}",
        genres=related,
        ml_description=ml_description,
    )


def user(tracked_ids=()):
    tracking = Mock()
    tracking.values_list.return_value = list(tracked_ids)
    tracking.values.return_value = [{"pk": pk} for pk in tracked_ids]
    return SimpleNamespace(pk=99, tracking_works=tracking)


def history_entry(work_obj, rating):
    return SimpleNamespace(work=work_obj, work_id=work_obj.pk, rating=rating)
