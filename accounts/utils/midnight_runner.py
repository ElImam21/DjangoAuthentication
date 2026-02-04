# accounts/utils/midnight_runner.py
from django.utils import timezone
from accounts.utils.job_runner import run_cleanup_if_needed


def check_midnight():
    now = timezone.now()
    if now.hour == 0 and now.minute == 0:
        run_cleanup_if_needed("midnight")
