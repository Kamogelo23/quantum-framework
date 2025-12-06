"""
API views for ML endpoints.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import httpx
import logging
from asgiref.sync import async_to_sync

from .models import MLModel, MLPrediction
from .serializers import (
    PredictionRequestSerializer,
    PredictionResponseSerializer,
    AnomalyDetectionRequestSerializer,
    MLModelSerializer
)
from apps.authentication.permissions import CanRunMLModels, IsViewer, IsDeveloper
from quantum.celery import app as celery_app

logger = logging.getLogger(__name__)


class MLViewSet(viewsets.ViewSet):
    """
    API endpoints for ML model predictions and anomaly detection.
    
    Permissions:
    - GET (list models): Requires Viewer role or above
    - POST (predict, detect-anomalies): Requires Analyst role or above
    - POST (train): Requires Developer role or above
    """
    permission_classes = [CanRunMLModels]
    
    def get_permissions(self):
        """
        Override to set different permissions for different actions.
        """
        if self.action == 'list':
            return [IsViewer()]
        elif self.action == 'train':
            return [IsDeveloper()]
        return [CanRunMLModels()]
    
    def list(self, request):
        """
        List available ML models.
        
        GET /api/v1/ml/models
        """
        try:
            # Try to get from ML service
            response = httpx.get(
                f"{settings.ML_SERVICE_URL}/models",
                timeout=10.0
            )
            if response.status_code == 200:
                return Response(response.json())
        except Exception as e:
            logger.warning(f"ML service unavailable: {str(e)}")
        
        # Fallback to database models
        models = MLModel.objects.filter(is_active=True)
        serializer = MLModelSerializer(models, many=True)
        
        return Response({
            'models': serializer.data if serializer.data else [
                {
                    'name': 'anomaly-detector',
                    'version': '1.0.0',
                    'type': 'isolation-forest',
                    'status': 'configured'
                },
                {
                    'name': 'performance-predictor',
                    'version': '1.0.0',
                    'type': 'random-forest',
                    'status': 'configured'
                }
            ]
        })
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        """
        Get ML model prediction.
        
        POST /api/v1/ml/predict
        """
        serializer = PredictionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Forward request to ML service
            response = httpx.post(
                f"{settings.ML_SERVICE_URL}/predict",
                json=serializer.validated_data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            # Log prediction
            try:
                model = MLModel.objects.get(name=serializer.validated_data['model_name'])
                MLPrediction.objects.create(
                    model=model,
                    features=serializer.validated_data['features'],
                    prediction=result.get('prediction'),
                    confidence=result.get('confidence'),
                    metadata=serializer.validated_data.get('metadata', {})
                )
            except MLModel.DoesNotExist:
                logger.warning(f"Model {serializer.validated_data['model_name']} not in registry")
            
            return Response(result)
            
        except httpx.HTTPError as e:
            logger.error(f"ML service error: {str(e)}")
            return Response(
                {
                    'error': 'ML service unavailable',
                    'detail': str(e)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['post'], url_path='detect-anomalies')
    def detect_anomalies(self, request):
        """
        Detect anomalies in monitoring data.
        
        POST /api/v1/ml/detect-anomalies
        """
        serializer = AnomalyDetectionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Forward request to ML service
            response = httpx.post(
                f"{settings.ML_SERVICE_URL}/anomaly-detection",
                json=serializer.validated_data,
                timeout=60.0
            )
            response.raise_for_status()
            
            return Response(response.json())
            
        except httpx.HTTPError as e:
            logger.error(f"Anomaly detection error: {str(e)}")
            return Response(
                {
                    'error': 'Anomaly detection service unavailable',
                    'detail': str(e)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['post'], permission_classes=[IsDeveloper])
    def train(self, request):
        """
        Trigger model training in background.
        
        POST /api/v1/ml/train?model_name=anomaly-detector
        """
        model_name = request.query_params.get('model_name', 'anomaly-detector')
        
        # Trigger background training task
        task = train_model_task.delay(model_name)
        
        return Response({
            'status': 'training_started',
            'model_name': model_name,
            'task_id': task.id,
            'message': 'Model training initiated in background'
        })


@celery_app.task
def train_model_task(model_name: str):
    """
    Background task for model training.
    """
    logger.info(f"Starting training for model: {model_name}")
    
    try:
        # Trigger training in ML service
        response = httpx.post(
            f"{settings.ML_SERVICE_URL}/train",
            json={'model_name': model_name},
            timeout=300.0
        )
        response.raise_for_status()
        
        logger.info(f"Training completed for model: {model_name}")
        return {'status': 'completed', 'model_name': model_name}
        
    except Exception as e:
        logger.error(f"Training failed for model {model_name}: {str(e)}")
        return {'status': 'failed', 'model_name': model_name, 'error': str(e)}
