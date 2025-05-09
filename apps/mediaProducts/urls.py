from django.urls import path
from .views import work_view, publication_view, publication_unit_view

urlpatterns = [
    path('work/', work_view, name='work'),
    path('publication/', publication_view, name='publication'),
    path('publication-unit/', publication_unit_view, name='publication_unit'),
]