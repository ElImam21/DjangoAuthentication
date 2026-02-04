from .utils.job_runner import run_cleanup_if_needed


def run_cleanup_after_migrate(sender, **kwargs):
    # aman: migrate sudah selesai
    run_cleanup_if_needed()
