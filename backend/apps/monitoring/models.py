"""
Database models for monitoring data.
"""

from django.db import models
from django.contrib.postgres.fields import JSONField


class MonitoringData(models.Model):
    """
    Time-series monitoring data from various sources.
    """
    timestamp = models.DateTimeField(db_index=True)
    source = models.CharField(max_length=255, db_index=True)
    metric_name = models.CharField(max_length=255, db_index=True)
    metric_value = models.FloatField()
    tags = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'monitoring_data'
        indexes = [
            models.Index(fields=['timestamp', 'source']),
            models.Index(fields=['timestamp', 'metric_name']),
            models.Index(fields=['source', 'metric_name']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.source} - {self.metric_name} @ {self.timestamp}"


class MonitoringSource(models.Model):
    """
    Registry of monitoring sources.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'monitoring_sources'
    
    def __str__(self):
        return self.name
