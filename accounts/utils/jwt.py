import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_access_token(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),  # access token 30 menit
    }
    return jwt.encode(payload, settings.ACCESS_TOKEN_SECRET, algorithm="HS256")

def generate_refresh_token(user):
    payload = {
        "sub": str(user.id),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=15),  # refresh token 15 hari
    }
    return jwt.encode(payload, settings.REFRESH_TOKEN_SECRET, algorithm="HS256")


