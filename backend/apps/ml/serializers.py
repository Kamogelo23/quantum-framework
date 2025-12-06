"""
Serializers for ML endpoints.
"""

from rest_framework import serializers
from .models import MLModel, MLPrediction


class PredictionRequestSerializer(serializers.Serializer):
    """
    Serializer for prediction requests.
    """
    model_name = serializers.CharField(max_length=255)
    features = serializers.ListField(child=serializers.FloatField())
    metadata = serializers.JSONField(default=dict, required=False)


class PredictionResponseSerializer(serializers.Serializer):
    """
    Serializer for prediction responses.
    """
    prediction = serializers.JSONField()
    confidence = serializers.FloatField(required=False, allow_null=True)
    model_version = serializers.CharField(max_length=50)
    timestamp = serializers.DateTimeField()


class AnomalyDetectionRequestSerializer(serializers.Serializer):
    """
    Serializer for anomaly detection requests.
    """
    data_points = serializers.ListField(child=serializers.JSONField())
    threshold = serializers.FloatField(default=0.95, required=False)


class AnomalyDetectionResponseSerializer(serializers.Serializer):
    """
    Serializer for anomaly detection responses.
    """
    anomalies = serializers.ListField(child=serializers.JSONField())
    anomaly_count = serializers.IntegerField()
    total_points = serializers.IntegerField()


class MLModelSerializer(serializers.ModelSerializer):
    """
    Serializer for ML model information.
    """
    class Meta:
        model = MLModel
        fields = ['id', 'name', 'version', 'model_type', 'description', 'is_active', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']
