# Quantum ⚛️

**AI-Powered Monitoring Platform with Machine Learning Integration**

Quantum is a cloud-native, containerized monitoring platform that leverages artificial intelligence and machine learning for intelligent system monitoring, anomaly detection, and predictive analytics.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Quantum Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Angular    │───▶│  FastAPI     │───▶│  ML Service  │      │
│  │   Frontend   │    │   Backend    │    │  (TensorFlow)│      │
│  │  (WebSocket) │◀───│              │◀───│              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                    │              │
│         │                    │                    │              │
│         ▼                    ▼                    ▼              │
│  ┌──────────────────────────────────────────────────────┐      │
│  │                 Keycloak (Auth)                       │      │
│  └──────────────────────────────────────────────────────┘      │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐            │
│         ▼                    ▼                    ▼            │
│  ┌───────────┐        ┌──────────┐        ┌──────────┐        │
│  │PostgreSQL │        │  Redis   │        │  Kafka   │        │
│  │(Database) │        │ (Cache)  │        │(Streaming)│        │
│  └───────────┘        └──────────┘        └──────────┘        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
           Deployed on Kubernetes with Harbor Registry
```

## ✨ Features

- 🎯 **Real-time Monitoring**: Monitor infrastructure, applications, network, and business metrics
- 🤖 **ML-Powered Analytics**: Anomaly detection, predictive analytics, and classification
- 📊 **Interactive Dashboards**: Real-time WebSocket dashboards with stunning visualizations
- 🔐 **Enterprise Auth**: Keycloak integration with SSO and role-based access control
- 📈 **Event Streaming**: Kafka integration for scalable data pipeline
- 🐳 **Cloud-Native**: Fully containerized with Kubernetes orchestration
- 🔒 **Secure**: Harbor container registry with vulnerability scanning

## 📋 Tech Stack

### Frontend
- **Angular 17** - Modern web framework with standalone components
- **Socket.IO** - Real-time WebSocket communication
- **Chart.js** - Data visualization
- **Keycloak Angular** - Authentication integration

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - ORM for database operations
- **Celery** - Distributed task queue
- **Prometheus** - Metrics and monitoring
- **Python-Keycloak** - Authentication

### ML/AI
- **TensorFlow** - Deep learning framework
- **scikit-learn** - Machine learning library
- **MLflow** - Model tracking and serving
- **Isolation Forest** - Anomaly detection

### Infrastructure
- **PostgreSQL** - Relational database
- **Redis** - Caching and session storage
- **Kafka** - Event streaming platform
- **RabbitMQ** - Message broker
- **Keycloak** - Identity and access management
- **Harbor** - Container registry
- **Kubernetes** - Container orchestration

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for frontend development)
- Python 3.11+ (for backend development)
- kubectl (for Kubernetes deployment)
- Helm 3+ (optional, for Harbor installation)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/quantum-framework.git
cd quantum-framework
```

2. **Start all services with Docker Compose**
```bash
docker-compose up -d
```

3. **Access the services**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs
   - ML Service: http://localhost:8001
   - Keycloak: http://localhost:8080
   - RabbitMQ Management: http://localhost:15672

4. **Default Credentials**
   - Keycloak Admin: `admin` / `admin`
   - RabbitMQ: `guest` / `guest`

### Development Setup

#### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run development server
python main.py
```

#### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start
```

#### ML Service Development

```bash
cd ml-service

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train sample model
python training/train_anomaly_detector.py

# Run ML server
python serving/model_server.py
```

## 🐳 Docker Deployment

### Build Images

**Linux/Mac:**
```bash
./scripts/build-and-push.sh
```

**Windows:**
```cmd
scripts\build-and-push.bat
```

### Configure Harbor

1. Set up Harbor registry (see `config/harbor/HARBOR_SETUP.md`)
2. Update image registry in scripts:
```bash
export HARBOR_REGISTRY=harbor.yourdomain.com
export VERSION=v1.0.0
```

### Push to Harbor

```bash
# Login to Harbor
docker login harbor.yourdomain.com

# Build and push
./scripts/build-and-push.sh
```

## ☸️ Kubernetes Deployment

### 1. Prerequisites

- Kubernetes cluster (1.25+)
- kubectl configured
- Harbor registry setup

### 2. Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 3. Configure Secrets

Update secrets in `k8s/backend/config.yaml` and `k8s/postgres/statefulset.yaml`:

```yaml
# Update these values:
- database-url: postgresql://quantum:YOUR_PASSWORD@quantum-postgres:5432/quantum
- keycloak-client-secret: YOUR_CLIENT_SECRET
- secret-key: GENERATE_RANDOM_SECRET
- postgres-password: YOUR_PASSWORD
```

### 4. Deploy Services

```bash
# Deploy all services
./scripts/deploy.sh

# Or deploy individually
kubectl apply -f k8s/postgres/statefulset.yaml
kubectl apply -f k8s/kafka/kafka.yaml
kubectl apply -f k8s/backend/config.yaml
kubectl apply -f k8s/ml-service/deployment.yaml
kubectl apply -f k8s/backend/deployment.yaml
kubectl apply -f k8s/keycloak/deployment.yaml
kubectl apply -f k8s/ingress/ingress.yaml
```

### 5. Verify Deployment

```bash
# Check pods
kubectl get pods -n quantum

# Check services
kubectl get svc -n quantum

# Check ingress
kubectl get ingress -n quantum

# View logs
kubectl logs -f deployment/quantum-backend -n quantum
```

### 6. Configure Keycloak

1. Import realm configuration:
```bash
kubectl exec -it deployment/quantum-keycloak -n quantum -- \
  /opt/keycloak/bin/kc.sh import --file /config/quantum-realm.json
```

2. Or manually create realm in UI at `https://auth.quantum.yourdomain.com`

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
DATABASE_URL=postgresql://quantum:quantum@postgres:5432/quantum
REDIS_URL=redis://redis:6379/0
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KEYCLOAK_SERVER_URL=http://keycloak:8080
KEYCLOAK_REALM=quantum
KEYCLOAK_CLIENT_ID=quantum-backend
KEYCLOAK_CLIENT_SECRET=your-secret
ML_SERVICE_URL=http://ml-service:8001
```

#### Frontend (environment.ts)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',
  wsUrl: 'http://localhost:8000',
  keycloakUrl: 'http://localhost:8080',
  keycloakRealm: 'quantum',
  keycloakClientId: 'quantum-frontend'
};
```

## 📖 API Documentation

Once the backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key Endpoints

- `POST /api/v1/monitoring/ingest` - Ingest monitoring data
- `GET /api/v1/monitoring/query` - Query monitoring data
- `POST /api/v1/ml/predict` - Get ML predictions
- `POST /api/v1/ml/detect-anomalies` - Detect anomalies
- `GET /api/v1/metrics/dashboard` - Dashboard metrics

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Monitoring & Observability

### Metrics

Prometheus metrics available at:
- Backend: http://localhost:8000/metrics
- ML Service: http://localhost:8001/metrics

### Logging

View logs:
```bash
# Backend logs
docker-compose logs -f backend

# ML service logs
docker-compose logs -f ml-service

# Kubernetes logs
kubectl logs -f deployment/quantum-backend -n quantum
```

## 🔐 Security

- All passwords stored in Kubernetes Secrets
- JWT-based authentication with Keycloak
- HTTPS enforced in production (configure TLS certificates)
- Harbor vulnerability scanning enabled
- Security headers configured in Nginx
- RBAC configured in Keycloak

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Backend won't start
- Check database connection: `docker logs quantum-postgres`
- Verify environment variables in `.env`
- Ensure PostgreSQL is running

### Frontend build fails
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 20+)

### ML Service errors
- Verify models directory exists: `ml-service/models/`
- Train initial model: `python ml-service/training/train_anomaly_detector.py`

### Kubernetes pods pending
- Check PVC status: `kubectl get pvc -n quantum`
- Verify secrets: `kubectl get secrets -n quantum`
- Check resource quotas

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Contact: support@quantum.local

---

**Built with ⚛️ by the Quantum Team**
