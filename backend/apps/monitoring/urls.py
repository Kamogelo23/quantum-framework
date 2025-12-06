"""
URL routing for monitoring endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonitoringViewSet

router = DefaultRouter()
router.register(r'monitoring', MonitoringViewSet, basename='monitoring')

urlpatterns = [
    path('', include(router.urls)),
]
