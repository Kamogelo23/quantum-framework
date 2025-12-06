"""
API v1 Router
Combines all API endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import monitoring, ml, metrics

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    monitoring.router,
    prefix="/monitoring",
    tags=["monitoring"]
)

api_router.include_router(
    ml.router,
    prefix="/ml",
    tags=["machine-learning"]
)

api_router.include_router(
    metrics.router,
    prefix="/metrics",
    tags=["metrics"]
)
