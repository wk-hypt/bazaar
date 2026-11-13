class ApiCsrfExemptMiddleware:
    """Skip CSRF for API clients that log in with a session cookie."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/') or request.path.startswith('/booking/'):
            request._dont_enforce_csrf_checks = True
        return self.get_response(request)
