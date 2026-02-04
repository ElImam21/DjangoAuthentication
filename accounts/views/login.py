import secrets
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status

from accounts.serializers.login import LoginSerializer
from accounts.models.refresh_tokens import RefreshToken
from accounts.utils.jwt import generate_access_token


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # update last_login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # generate tokens
        access_token = generate_access_token(user)

        refresh_token_value = secrets.token_urlsafe(64)

        RefreshToken.objects.create(
            user=user,
            token=refresh_token_value,
            expires_at=timezone.now() + timedelta(days=15),
        )

        return Response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token_value,
                "token_type": "Bearer",
                "expires_in": 1800,
            },
            status=status.HTTP_200_OK
        )
    

