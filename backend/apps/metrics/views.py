"""
API views for metrics and dashboard endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Max, Min
from django.utils import timezone
from datetime import timedelta

from apps.monitoring.models import MonitoringData, MonitoringSource
from apps.ml.models import MLPrediction
from apps.authentication.permissions import IsViewer


class MetricsViewSet(viewsets.ViewSet):
    """
    API endpoints for metrics and dashboard data.
    
    Permissions:
    - All endpoints: Requires Viewer role or above
    """
    permission_classes = [IsViewer]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Get aggregated metrics for dashboard.
        
        GET /api/v1/metrics/dashboard
        """
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        last_hour = now - timedelta(hours=1)
        
        # Data ingestion stats
        total_data_points = MonitoringData.objects.count()
        data_points_24h = MonitoringData.objects.filter(
            timestamp__gte=last_24h
        ).count()
        data_points_1h = MonitoringData.objects.filter(
            timestamp__gte=last_hour
        ).count()
        
        # Active sources
        active_sources = MonitoringSource.objects.filter(
            is_active=True
        ).count()
        
        # ML predictions
        predictions_24h = MLPrediction.objects.filter(
            created_at__gte=last_24h
        ).count()
        
        # Top metrics by volume
        top_metrics = MonitoringData.objects.filter(
            timestamp__gte=last_24h
        ).values('metric_name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        return Response({
            'summary': {
                'total_data_points': total_data_points,
                'data_points_24h': data_points_24h,
                'data_points_1h': data_points_1h,
                'active_sources': active_sources,
                'predictions_24h': predictions_24h,
            },
            'top_metrics': list(top_metrics),
            'timestamp': now.isoformat()
        })
    
    @action(detail=False, methods=['get'])
    def timeseries(self, request):
        """
        Get time-series data for a specific metric.
        
        GET /api/v1/metrics/timeseries?metric_name=cpu_usage&source=server1&hours=24
        """
        metric_name = request.query_params.get('metric_name')
        source = request.query_params.get('source')
        hours = int(request.query_params.get('hours', 24))
        
        if not metric_name:
            return Response(
                {'error': 'metric_name parameter is required'},
                status=400
            )
        
        start_time = timezone.now() - timedelta(hours=hours)
        
        queryset = MonitoringData.objects.filter(
            metric_name=metric_name,
            timestamp__gte=start_time
        )
        
        if source:
            queryset = queryset.filter(source=source)
        
        # Get data points
        data_points = queryset.values('timestamp', 'metric_value', 'source').order_by('timestamp')
        
        return Response({
            'metric_name': metric_name,
            'data': list(data_points),
            'count': len(data_points)
        })
    
    @action(detail=False, methods=['get'])
    def aggregates(self, request):
        """
        Get aggregated statistics for a metric.
        
        GET /api/v1/metrics/aggregates?metric_name=cpu_usage&hours=24
        """
        metric_name = request.query_params.get('metric_name')
        hours = int(request.query_params.get('hours', 24))
        
        if not metric_name:
            return Response(
                {'error': 'metric_name parameter is required'},
                status=400
            )
        
        start_time = timezone.now() - timedelta(hours=hours)
        
        aggregates = MonitoringData.objects.filter(
            metric_name=metric_name,
            timestamp__gte=start_time
        ).aggregate(
            avg=Avg('metric_value'),
            min=Min('metric_value'),
            max=Max('metric_value'),
            count=Count('id')
        )
        
        return Response({
            'metric_name': metric_name,
            'time_range_hours': hours,
            'statistics': aggregates
        })
