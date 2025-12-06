"""
Custom exception handler for better error messages.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response format
        custom_response_data = {
            'error': {
                'message': str(exc),
                'detail': response.data,
                'status_code': response.status_code
            }
        }
        
        # Log the error
        logger.error(
            f'API Error: {exc.__class__.__name__} - {str(exc)}',
            exc_info=True,
            extra={'context': context}
        )
        
        response.data = custom_response_data
    
    return response
