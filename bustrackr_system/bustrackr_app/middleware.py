from django.utils.deprecation import MiddlewareMixin

class NoCacheForAuthMiddleware(MiddlewareMixin):
    """
    Add strict no-cache headers for HTML responses.
    This prevents browsers from showing cached authenticated pages after logout.
    """
    def process_response(self, request, response):
        content_type = response.get('Content-Type', '')
        # Only add headers to HTML responses
        if content_type and 'text/html' in content_type:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
