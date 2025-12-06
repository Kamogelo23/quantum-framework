"""
Custom permission classes for role-based access control.
"""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to admins.
    """
    message = 'Admin permission required.'
    
    def has_permission(self, request, view):
        return hasattr(request, 'is_admin') and request.is_admin


class IsDeveloper(permissions.BasePermission):
    """
    Permission class that allows access to developers and above.
    """
    message = 'Developer permission required.'
    
    def has_permission(self, request, view):
        return hasattr(request, 'is_developer') and request.is_developer


class IsAnalyst(permissions.BasePermission):
    """
    Permission class that allows access to analysts and above.
    """
    message = 'Analyst permission required.'
    
    def has_permission(self, request, view):
        return hasattr(request, 'is_analyst') and request.is_analyst


class IsViewer(permissions.BasePermission):
    """
    Permission class that allows access to viewers and above (all authenticated users).
    """
    message = 'Viewer permission required.'
    
    def has_permission(self, request, view):
        return hasattr(request, 'is_viewer') and request.is_viewer


class CanIngestData(permissions.BasePermission):
    """
    Permission for data ingestion - requires developer or admin.
    """
    message = 'Data ingestion requires developer or admin permission.'
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return hasattr(request, 'is_viewer') and request.is_viewer
        return hasattr(request, 'is_developer') and request.is_developer


class CanRunMLModels(permissions.BasePermission):
    """
    Permission for running ML models - requires analyst or above.
    """
    message = 'Running ML models requires analyst permission.'
    
    def has_permission(self, request, view):
        return hasattr(request, 'is_analyst') and request.is_analyst


class CanManageSystem(permissions.BasePermission):
    """
    Permission for system management - requires admin.
    """
    message = 'System management requires admin permission.'
    
    def has_permission(self, request, view):
        return hasattr(request, 'is_admin') and request.is_admin
