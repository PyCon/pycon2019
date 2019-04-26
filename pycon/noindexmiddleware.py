class NoIndexMiddleware:

    def process_response(self, request, response):
        response['X-Robots-Tag'] = "noindex"
        return response
