"""
Group-based permission middleware for Keycloak groups.
Maps Keycloak groups to Django permissions.
"""

import logging
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class KeycloakGroupPermissionMiddleware:
    """
    Middleware that extracts Keycloak groups from the request
    and maps them to Django permissions.
    
    Group Hierarchy:
    - quantum-admins: Full system access
    - quantum-developers: Can manage monitoring, ML, ingest data
    - quantum-analysts: Can query data, run ML predictions
    - quantum-viewers: Read-only access
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request
        if hasattr(request, 'keycloak_groups'):
            self.process_groups(request)
        
        response = self.get_response(request)
        return response
    
    def process_groups(self, request):
        """
        Process Keycloak groups and set permission flags on request.
        
        Args:
            request: Django request object with keycloak_groups attribute
        """
        groups = request.keycloak_groups or []
        
        # Initialize permission flags
        request.is_admin = False
        request.is_developer = False
        request.is_analyst = False
        request.is_viewer = False
        
        # Map groups to permission flags
        for group in groups:
            # Remove leading slash if present (Keycloak sometimes includes it)
            group_name = group.lstrip('/')
            
            if group_name == 'quantum-admins':
                request.is_admin = True
                request.is_developer = True
                request.is_analyst = True
                request.is_viewer = True
            elif group_name == 'quantum-developers':
                request.is_developer = True
                request.is_analyst = True
                request.is_viewer = True
            elif group_name == 'quantum-analysts':
                request.is_analyst = True
                request.is_viewer = True
            elif group_name == 'quantum-viewers':
                request.is_viewer = True
        
        logger.debug(
            f'User {request.user.username} permissions: '
            f'admin={request.is_admin}, '
            f'developer={request.is_developer}, '
            f'analyst={request.is_analyst}, '
            f'viewer={request.is_viewer}'
        )
