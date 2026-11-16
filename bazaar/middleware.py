class ApiCsrfExemptMiddleware:
    """Skip the CSRF check for /api/ so a session cookie is enough."""

    def __init__(self, get_response):
        """Store the next middleware in the chain."""
        self.get_response = get_response

    def __call__(self, request):
        """Mark /api/ and /booking/ requests so Django does not require a CSRF token."""
        if request.path.startswith('/api/'):
            request._dont_enforce_csrf_checks = True
        return self.get_response(request)
