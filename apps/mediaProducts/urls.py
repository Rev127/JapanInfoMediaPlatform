from django.urls import path
from .views import work_view, publication_view, publication_unit_view, rate_work

urlpatterns = [
    path('work/<str:link>/', work_view, name='work'),
    path('publication/<str:publication_type>/<str:link>/', publication_view, name='publication'),
    path('publication-unit/<str:publication_unit_type>/<str:link>/',
         publication_unit_view, name='publication_unit'),
    path('work-rating/<str:link>/', rate_work, name='rate_work'),
]