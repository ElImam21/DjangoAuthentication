from rest_framework import serializers
from django.utils import timezone
from accounts.models.refresh_tokens import RefreshToken


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        token_value = attrs["refresh_token"]

        token = RefreshToken.objects.filter(
            token=token_value,
            revoked_at__isnull=True
        ).select_related("user").first()

        if not token:
            raise serializers.ValidationError("Refresh token tidak valid")

        if token.is_expired:
            raise serializers.ValidationError("Refresh token sudah expired")

        attrs["token_obj"] = token
        attrs["user"] = token.user
        return attrs
