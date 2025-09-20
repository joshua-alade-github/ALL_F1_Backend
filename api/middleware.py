from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class APIErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if request.path.startswith('/api/'):
            logger.error(f"API Error: {str(exception)}", exc_info=True)
            return JsonResponse({
                'error': 'An error occurred while fetching data. Please try again later.',
                'detail': str(exception) if settings.DEBUG else None
            }, status=500)
        return None