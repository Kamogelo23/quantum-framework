# Quick Start Guide

Get Quantum up and running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- 8GB RAM available
- Ports 4200, 8000, 8080, 5432, 6379, 5672 available

## 1. Clone & Start

```bash
cd "c:\Users\KamogeloMahoma\New folder (2)\quantum-framework"

# Start all services
docker-compose up -d

# Wait for services to be ready (about 2 minutes)
docker-compose logs -f backend
```

## 2. Import Keycloak Realm

### Option A: Automatic (Linux/Mac)
```bash
./scripts/init-keycloak.sh
```

### Option B: Manual Import
1. Wait 30 seconds for Keycloak to start
2. Visit http://localhost:8080
3. Login: `admin` / `admin`
4. Click "Create Realm" → "Browse"
5. Select `config/keycloak/quantum-realm.json`
6. Click "Create"

## 3. Run Database Migrations

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## 4. Test Authentication

### Get Access Token
```bash
curl -X POST http://localhost:8080/realms/quantum/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=quantum-backend" \
  -d "client_secret=quantum-backend-secret-change-in-production" \
  -d "username=developer" \
  -d "password=developer123" \
  -d "grant_type=password"
```

### Test API
```bash
# Replace YOUR_TOKEN with access_token from above
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/monitoring/sources
```

## 5. Access Services

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/admin
- **Keycloak**: http://localhost:8080

## Test Users

| Username | Password | Group | Access Level |
|----------|----------|-------|--------------|
| admin | admin123 | quantum-admins | Full access |
| developer | developer123 | quantum-developers | Manage + Ingest |
| analyst | analyst123 | quantum-analysts | Query + ML |
| viewer | viewer123 | quantum-viewers | Read-only |

⚠️ All passwords are temporary and must be changed on first login!

## Next Steps

1. ✅ Test authentication with different user roles
2. ✅ Ingest some test data via API
3. ✅ Run ML predictions
4. ✅ View real-time dashboard
5. ✅ Deploy to Oracle Cloud (see deployment/oci/SIGNUP_GUIDE.md)

## Troubleshooting

**Services won't start:**
```bash
docker-compose down
docker-compose up -d
docker-compose logs
```

**Reset everything:**
```bash
docker-compose down -v
docker-compose up -d
```

**Check service health:**
```bash
docker-compose ps
curl http://localhost:8000/health
```

Happy coding! 🚀
