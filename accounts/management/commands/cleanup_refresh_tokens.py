from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from accounts.models.refresh_tokens import RefreshToken


class Command(BaseCommand):
    help = "Hapus refresh token yang sudah di-revoke dan expired lebih dari 3 hari"

    def handle(self, *args, **options):
        threshold = timezone.now() - timedelta(days=3)

        qs = RefreshToken.objects.filter(
            revoked_at__isnull=False,
            expires_at__lte=threshold
        )

        count = qs.count()
        qs.delete()

        self.stdout.write(
            self.style.SUCCESS(f"{count} refresh token berhasil dihapus")
        )
