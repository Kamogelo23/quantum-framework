"""
URL routing for ML endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MLViewSet

router = DefaultRouter()
router.register(r'ml', MLViewSet, basename='ml')

urlpatterns = [
    path('', include(router.urls)),
]
