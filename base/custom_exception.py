from rest_framework.views import exception_handler
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler for modifying the response based on custom requirements.

    """

    # Call REST framework's default exception handler,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now modify the response based on custom requirements.
    if response is not None:
        error_detail = "Something went wrong."
        if 'non_field_errors' in response.data:
            error_detail = response.data.get('non_field_errors', [])[0]
        elif 'detail' in response.data:
            error_detail = response.data['detail']
        else:
            return response  # No modification needed if there's no 'non_field_errors' or 'detail'

        code = getattr(error_detail, 'code', None)

        try:
            if code is not None:
                response.status_code = int(code)
        except ValueError:
            response.status_code = 400

        response.data = {
            'success': False,
            'message': str(error_detail),
        }

    return response


def custom404(request, exception=None):
    """
    Custom 404 view for handling not found resources.

    This view returns a JSON response with a 404 status code and a custom error message.
    """

    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })
