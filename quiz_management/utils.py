"""
Custom utility functions for the quiz management system.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that provides consistent error responses.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data,
            'status_code': response.status_code
        }
        
        # Handle different types of errors
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['message'] = 'Bad Request'
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data['message'] = 'Unauthorized'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['message'] = 'Forbidden'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['message'] = 'Not Found'
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            custom_response_data['message'] = 'Method Not Allowed'
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            custom_response_data['message'] = 'Internal Server Error'
        
        response.data = custom_response_data
    
    return response


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Standardized success response format.
    """
    return Response({
        'error': False,
        'message': message,
        'data': data,
        'status_code': status_code
    }, status=status_code)


def error_response(message="An error occurred", details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Standardized error response format.
    """
    return Response({
        'error': True,
        'message': message,
        'details': details,
        'status_code': status_code
    }, status=status_code)