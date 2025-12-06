"""
API views for monitoring endpoints.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
import logging

from .models import MonitoringData, MonitoringSource
from .serializers import (
    MonitoringDataSerializer,
    MonitoringDataCreateSerializer,
    MonitoringSourceSerializer
)
from apps.authentication.permissions import CanIngestData, IsViewer, IsDeveloper

logger = logging.getLogger(__name__)


class MonitoringViewSet(viewsets.ModelViewSet):
    """
    API endpoints for monitoring data ingestion and retrieval.
    
    Permissions:
    - GET (list, retrieve, query): Requires Viewer role or above
    - POST (create, batch_ingest): Requires Developer role or above
    """
    queryset = MonitoringData.objects.all()
    serializer_class = MonitoringDataSerializer
    permission_classes = [CanIngestData]
    
    def get_permissions(self):
        """
        Override to set different permissions for different actions.
        """
        if self.action in ['list', 'retrieve', 'query', 'sources']:
            return [IsViewer()]
        return [IsDeveloper()]
    
    def create(self, request):
        """
        Ingest single monitoring data point.
        
        POST /api/v1/monitoring/ingest
        """
        serializer = MonitoringDataCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create monitoring data
        data = MonitoringData.objects.create(**serializer.validated_data)
        
        # Update source last_seen
        MonitoringSource.objects.update_or_create(
            name=data.source,
            defaults={'last_seen': timezone.now()}
        )
        
        logger.info(f"Ingested monitoring data: {data.source} - {data.metric_name}")
        
        return Response(
            {
                'status': 'success',
                'message': 'Monitoring data ingested successfully',
                'timestamp': data.timestamp,
                'id': data.id
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsDeveloper])
    def batch_ingest(self, request):
        """
        Ingest multiple monitoring data points in batch.
        
        POST /api/v1/monitoring/batch-ingest
        """
        if not isinstance(request.data, list):
            return Response(
                {'error': 'Expected a list of monitoring data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = MonitoringDataCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        
        # Bulk create monitoring data
        monitoring_data = [
            MonitoringData(**item)
            for item in serializer.validated_data
        ]
        created = MonitoringData.objects.bulk_create(monitoring_data)
        
        # Update sources
        sources = set(item['source'] for item in serializer.validated_data)
        for source_name in sources:
            MonitoringSource.objects.update_or_create(
                name=source_name,
                defaults={'last_seen': timezone.now()}
            )
        
        logger.info(f"Batch ingested {len(created)} monitoring data points")
        
        return Response(
            {
                'status': 'success',
                'message': f'Ingested {len(created)} monitoring data points',
                'count': len(created)
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsViewer])
    def query(self, request):
        """
        Query monitoring data with filters.
        
        GET /api/v1/monitoring/query?source=&metric_name=&start_time=&end_time=&limit=100
        """
        source = request.query_params.get('source')
        metric_name = request.query_params.get('metric_name')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        limit = int(request.query_params.get('limit', 100))
        
        # Build query
        queryset = self.get_queryset()
        
        if source:
            queryset = queryset.filter(source=source)
        
        if metric_name:
            queryset = queryset.filter(metric_name=metric_name)
        
        if start_time:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            queryset = queryset.filter(timestamp__gte=start_dt)
        
        if end_time:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            queryset = queryset.filter(timestamp__lte=end_dt)
        
        # Limit results
        queryset = queryset[:limit]
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'data': serializer.data,
            'count': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsViewer])
    def sources(self, request):
        """
        Get list of monitoring sources.
        
        GET /api/v1/monitoring/sources
        """
        sources = MonitoringSource.objects.filter(is_active=True)
        serializer = MonitoringSourceSerializer(sources, many=True)
        
        return Response({
            'sources': serializer.data
        })
