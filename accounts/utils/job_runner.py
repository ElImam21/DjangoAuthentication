from django.utils import timezone
from django.core.management import call_command
from accounts.models import JobLock


def run_cleanup_if_needed(trigger: str):
    now = timezone.now()
    lock_name = f"cleanup_refresh_tokens:{trigger}"

    lock, _ = JobLock.objects.get_or_create(name=lock_name)

    # sudah pernah jalan untuk trigger ini
    if lock.last_run_at:
        return

    call_command("cleanup_refresh_tokens")

    lock.last_run_at = now
    lock.save(update_fields=["last_run_at"])
