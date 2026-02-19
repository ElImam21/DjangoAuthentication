from django.urls import path

# === Import Bawaan Teman Anda ===
from accounts.views.register import RegisterView
from accounts.views.login import LoginView
from accounts.views.refresh import RefreshTokenView

# === Import Tambahan Fitur Baru ===
# (Pastikan file user_features.py sudah dibuat di folder accounts/views/)
from accounts.views.user_features import UpdateProfileView, LogoutView

urlpatterns = [
    # === URL Asli Teman Anda ===
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("refresh", RefreshTokenView.as_view()),

    # === URL Tambahan (Update Profile & Logout) ===
    path("profile/update", UpdateProfileView.as_view()), # Method: PATCH
    path("logout", LogoutView.as_view()),                # Method: POST
]