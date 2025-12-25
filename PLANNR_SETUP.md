# Plannr Setup Guide

## Environment Configuration

### 1. Create `.env` file

Copy `.env.example` to `.env` in the `backend/` directory:

```bash
cp .env.example .env
```

### 2. Add Claude API Configuration

Add the following lines to your `.env` file:

```env
# Plannr - Claude API Configuration
CLAUDE_API_KEY=your-actual-claude-api-key-here
CLAUDE_API_URL=https://api.anthropic.com/v1/messages
```

> **Note**: Replace `your-actual-claude-api-key-here` with your actual Claude API key from Anthropic.

### 3. Update Host Configuration for Local Development

If running locally (not in Docker), update these values in `.env`:

```env
DB_HOST=localhost
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672/
KEYCLOAK_SERVER_URL=http://localhost:8080
ML_SERVICE_URL=http://localhost:8001
```

## Database Migration

Run the following commands to create the database tables:

```bash
cd backend
python manage.py migrate
```

## Testing Plannr

### 1. Start Required Services

Make sure you have the following services running:
- PostgreSQL database
- Redis
- Keycloak (for authentication)

### 2. Run the Django Development Server

```bash
python manage.py runserver
```

### 3. Test the API Endpoints

**Upload Job Description:**
```bash
curl -X POST http://localhost:8000/api/v1/plannr/job-description/ \
  -F "content=Senior Python Developer with Django experience"
```

**Upload Resume:**
```bash
curl -X POST http://localhost:8000/api/v1/plannr/resume/ \
  -F "file=@/path/to/resume.pdf"
```

**Extract Keywords:**
```bash
curl -X POST http://localhost:8000/api/v1/plannr/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1}'
```

**Generate Tailored Resume:**
```bash
curl -X POST http://localhost:8000/api/v1/plannr/tailor/ \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1, "resume_id": 1, "keywords": ["Python", "Django", "REST API"]}'
```

**Download Generated Resume:**
```bash
curl http://localhost:8000/api/v1/plannr/download/1/
```

## Frontend Testing

### 1. Start the Angular Development Server

```bash
cd frontend
npm install
npm run start
```

### 2. Access Plannr

Navigate to: `http://localhost:4200/plannr`

### 3. Test the Flow

1. Paste or upload a job description
2. Upload your resume
3. Click "Generate Tailored Resume"
4. View extracted keywords
5. Download the generated PDF

## Docker Setup for LaTeX Compilation

The Plannr service uses a Docker container to compile LaTeX to PDF. Ensure Docker is installed and running:

```bash
docker pull blang/latex:ctanfull
```

## Troubleshooting

### Claude API Errors

If you get API errors:
1. Verify your `CLAUDE_API_KEY` is correct
2. Check the `CLAUDE_API_URL` endpoint
3. Ensure you have API credits/quota available

### LaTeX Compilation Errors

If PDF generation fails:
1. Ensure Docker is running
2. Check Docker image is pulled: `docker images | grep latex`
3. Check Docker container logs

### Authentication Issues

If auth guard is still redirecting:
1. Clear browser cache/cookies
2. Ensure Keycloak is running on port 8080
3. Check frontend `auth.service.ts` console logs
4. Verify `isInitialized$` observable is emitting `true`

## Next Steps

- Add your actual Claude API key to `.env`
- Customize the ModernCV LaTeX template in `backend/apps/plannr/templates/`
- Add file storage configuration (local or S3)
- Set up Celery for async processing
- Configure document upload limits in Django settings
