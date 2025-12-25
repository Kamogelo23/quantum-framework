"""
URL configuration for Quantum project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


def health_check(request):
    """Health check endpoint for container orchestration"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'quantum-backend',
        'version': '1.0.0'
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health_check),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    # PLannr Routes (Specific match first)
    path('api/v1/plannr/', include('apps.plannr.urls')),

    # Other API Endpoints (Generic match last)
    path('api/v1/', include('apps.monitoring.urls')),
    path('api/v1/', include('apps.ml.urls')),
    path('api/v1/', include('apps.metrics.urls')),
]

# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
