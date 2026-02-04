from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models.users import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs["email"]).first()
        if not user or not user.check_password(attrs["password"]):
            raise serializers.ValidationError("Email atau password salah")

        attrs["user"] = user
        return attrs
