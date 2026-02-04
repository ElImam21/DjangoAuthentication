import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models.users import User


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def is_revoked(self):
        return self.revoked_at is not None
