from django.urls import path
from accounts.views.register import RegisterView
from accounts.views.login import LoginView
from accounts.views.refresh import RefreshTokenView

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("refresh", RefreshTokenView.as_view()),
]
