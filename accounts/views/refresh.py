import secrets
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers.refresh import RefreshTokenSerializer
from accounts.models.refresh_tokens import RefreshToken
from accounts.utils.jwt import generate_access_token


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_token = serializer.validated_data["token_obj"]
        user = serializer.validated_data["user"]

        # revoke refresh token lama (ROTATION)
        old_token.revoked_at = timezone.now()
        old_token.save(update_fields=["revoked_at"])

        # generate access token baru
        access_token = generate_access_token(user)

        # generate refresh token baru
        new_refresh_token = secrets.token_urlsafe(64)

        RefreshToken.objects.create(
            user=user,
            token=new_refresh_token,
            expires_at=old_token.expires_at,
        )

        return Response(
            {
                "access_token": access_token,
                "refresh_token": new_refresh_token,
                "token_type": "Bearer",
                "expires_in": 1800,
            },
            status=status.HTTP_200_OK
        )
