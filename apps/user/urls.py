from django.urls import path
from .views import profile_view, RegisterView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
]