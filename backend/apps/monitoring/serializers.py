"""
Serializers for monitoring data validation and serialization.
"""

from rest_framework import serializers
from .models import MonitoringData, MonitoringSource


class MonitoringDataSerializer(serializers.ModelSerializer):
    """
    Serializer for monitoring data ingestion and retrieval.
    """
    class Meta:
        model = MonitoringData
        fields = ['id', 'timestamp', 'source', 'metric_name', 'metric_value', 'tags', 'created_at']
        read_only_fields = ['id', 'created_at']


class MonitoringDataCreateSerializer(serializers.Serializer):
    """
    Serializer for creating monitoring data (without ID).
    """
    timestamp = serializers.DateTimeField()
    source = serializers.CharField(max_length=255)
    metric_name = serializers.CharField(max_length=255)
    metric_value = serializers.FloatField()
    tags = serializers.JSONField(default=dict, required=False)


class MonitoringSourceSerializer(serializers.ModelSerializer):
    """
    Serializer for monitoring sources.
    """
    class Meta:
        model = MonitoringSource
        fields = ['id', 'name', 'description', 'is_active', 'last_seen', 'metadata', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
