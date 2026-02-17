from accounts.utils.job_runner import run_cleanup_if_needed
from accounts.utils.midnight_runner import check_midnight


class StartupCleanupMiddleware:
    _has_run = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 🔥 LEWATI PREFLIGHT
        if request.method == "OPTIONS":
            return self.get_response(request)

        if not StartupCleanupMiddleware._has_run:
            StartupCleanupMiddleware._has_run = True
            run_cleanup_if_needed("server_start")

        return self.get_response(request)
