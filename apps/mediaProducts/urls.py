from django.urls import path
from .views import work_view, publication_view, publication_unit_view

urlpatterns = [
    path('work/<str:link>/', work_view, name='work'),
    path('publication/<str:publication_type>/<str:link>/', publication_view, name='publication'),
    path('publication-unit/<str:publication_unit_type>/<str:link>/', publication_unit_view, name='publication_unit'),
]