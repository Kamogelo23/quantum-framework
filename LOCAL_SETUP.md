# 🚀 Run Quantum + Plannr Locally

## Quick Start (3 Steps)

### Step 1: Start Services (Docker)
```bash
# Start all backend services (PostgreSQL, Redis, Keycloak, etc.)
docker-compose up -d postgres redis keycloak
```

Wait ~30 seconds for services to be ready, then check:
```bash
docker-compose ps
```

All services should show "(healthy)" status.

### Step 2: Start Backend (Django)
```bash
cd backend

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Backend will start on: **http://localhost:8000**

Test it: http://localhost:8000/health
- Should return: `{"status": "healthy", ...}`

### Step 3: Start Frontend (Angular)
Open a **new terminal**:
```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run start
```

Frontend will start on: **http://localhost:4200**

---

## ✅ Test Plannr

1. Navigate to: **http://localhost:4200/plannr**
2. Paste a job description or upload a file
3. Upload your resume (PDF, DOCX, TXT)
4. Click "Generate Tailored Resume"
5. View extracted keywords (powered by Gemini AI ✨)
6. Download the generated PDF

---

## 🛠️ Troubleshooting

### "Port 5432 already in use"
PostgreSQL is already running on your machine. Either:
- Stop it: `net stop postgresql` (Windows)
- Or change port in docker-compose.yml: `"5433:5432"`

### "Connection refused" from backend
Services aren't ready yet. Wait 30 seconds and try again.

### Keycloak not accessible
First time takes ~1 minute to initialize. Check logs:
```bash
docker logs quantum-keycloak
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run start
```

---

## 📊 Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:4200 | - |
| **Backend API** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/api/docs | - |
| **Keycloak** | http://localhost:8080 | admin / admin |
| **RabbitMQ** | http://localhost:15672 | guest / guest |

---

## 🔄 Stop Everything

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

---

## 💡 Development Workflow

### Making Backend Changes:
1. Edit code in `backend/`
2. Django auto-reloads (Dev server running)
3. Refresh browser

### Making Frontend Changes:
1. Edit code in `frontend/src/`
2. Angular auto-reloads (webpack-dev-server)
3. Browser auto-refreshes

### Adding Django Models:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🆕 First Time Setup Checklist

- [x] Backend code created
- [x] Frontend code created
- [x] Gemini API configured
- [x] Docker Compose ready
- [ ] Docker services started
- [ ] Backend migrations run
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Test Plannr flow

---

## Next Steps

1. **Start services** (Step 1 above)
2. **Run backend** (Step 2)
3. **Run frontend** (Step 3)
4. **Test Plannr!** 🎉
