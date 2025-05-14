from django.urls import path
from .views import index, ajax_search

urlpatterns = [
    path("", index, name="index"),
    path('search/', ajax_search, name='search')
]