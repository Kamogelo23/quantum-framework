"""
Database models for ML service.
"""

from django.db import models


class MLModel(models.Model):
    """
    Registry of ML models.
    """
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=50)
    model_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ml_models'
        unique_together = ['name', 'version']
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class MLPrediction(models.Model):
    """
    Log of ML predictions.
    """
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='predictions')
    features = models.JSONField()
    prediction = models.JSONField()
    confidence = models.FloatField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ml_predictions'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['model', 'created_at']),
        ]
    
    def __str__(self):
        return f"Prediction by {self.model.name} @ {self.created_at}"
