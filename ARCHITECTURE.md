# Quantum Framework Architecture

## System Overview

Quantum is a microservices-based AI monitoring platform designed for scalability, reliability, and real-time performance.

## Design Principles

1. **Cloud-Native First**: Designed to run on Kubernetes from day one
2. **Containerized Everything**: All components are containerized for portability
3. **Event-Driven Architecture**: Kafka enables async processing and scalability
4. **ML at the Core**: Machine learning integrated throughout the pipeline
5. **Security by Design**: Keycloak SSO and Harbor vulnerability scanning

## Component Architecture

### Frontend Layer
- **Technology**: Angular 17 with standalone components
- **Communication**: REST API + WebSocket for real-time updates
- **Authentication**: Keycloak Angular integration with PKCE flow
- **Design**: Glassmorphism with gradient backgrounds

### API Gateway
- **Technology**: FastAPI (Python)
- **Features**: 
  - Auto-generated OpenAPI/Swagger docs
  - Async request handling
  - JWT token validation
  - Rate limiting (planned)
  - Request/response logging

### Services Layer

#### Monitoring Service
- Ingests metrics from various sources
- Stores in PostgreSQL with time-series optimization
- Publishes events to Kafka for downstream processing

#### ML Service
- TensorFlow/scikit-learn models
- Anomaly detection using Isolation Forest
- Predictive analytics (planned)
- Model serving via REST API

### Data Layer

#### PostgreSQL
- Primary data store
- Monitoring metrics
- User data
- ML training data

#### Redis
- Session storage
- Cache layer
- Pub/sub for WebSocket

#### Kafka
- Event streaming
- Decouples services
- Replay capability
- Multiple consumer groups

### Authentication & Authorization

#### Keycloak
- OpenID Connect provider
- Role-based access control (RBAC)
- SSO integration
- Token management

## Data Flow

```
Monitoring Source → Backend API → Kafka → ML Service
                         ↓                      ↓
                    PostgreSQL            Anomaly Detected
                         ↓                      ↓
                    Dashboard ← WebSocket ← Backend
```

## Deployment Architecture

### Local Development
- Docker Compose orchestrates all services
- Hot reload for faster development
- Shared volumes for code mounting

### Production (Kubernetes)
- Multiple replicas for high availability
- StatefulSets for databases
- Persistent volumes for data
- Ingress for external access
- Secrets management
- Resource limits and requests

## Scalability Considerations

1. **Horizontal Scaling**: All stateless services can scale horizontally
2. **Database**: PostgreSQL can be replaced with distributed SQL (CockroachDB)
3. **Kafka**: Can add more brokers for higher throughput
4. **ML Service**: Can scale independently based on prediction load

## Security Architecture

1. **Network**: All internal services communicate via ClusterIP
2. **Secrets**: Kubernetes Secrets for sensitive data
3. **Authentication**: All endpoints require JWT token
4. **Authorization**: Keycloak roles enforced at API level
5. **Registry**: Harbor scans all images for vulnerabilities
6. **HTTPS**: TLS termination at Ingress level

## Monitoring & Observability

1. **Metrics**: Prometheus format exposed by all services
2. **Logs**: Structured JSON logging
3. **Tracing**: OpenTelemetry integration (planned)
4. **Health Checks**: Liveness and readiness probes

## Future Enhancements

1. **Service Mesh**: Istio for advanced traffic management
2. **GitOps**: ArgoCD for declarative deployments
3. **Auto-scaling**: HPA based on custom metrics
4. **Multi-cluster**: Federation for disaster recovery
5. **Advanced ML**: Deep learning models for time-series prediction
