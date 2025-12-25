# Quantum Framework + Plannr - Cloud Deployment Guide

## 🔑 Getting a Claude API Key

### Option 1: Anthropic Console (Recommended)
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-...`)
6. Add to your `.env` file:
   ```env
   CLAUDE_API_KEY=sk-ant-api03-...your-key-here
   CLAUDE_API_URL=https://api.anthropic.com/v1/messages
   ```

**Pricing**: 
- Pay-as-you-go: ~$3/million input tokens, ~$15/million output tokens (Claude 3.5 Sonnet)
- $5 free credits for new accounts

### Option 2: Alternative AI APIs (Free Tiers)
- **Google AI Studio**: Free Gemini API key ([aistudio.google.com](https://aistudio.google.com))
- **OpenRouter**: Aggregate multiple AI models ([openrouter.ai](https://openrouter.ai))

---

## ☁️ Free Cloud Services for Deployment

### 1. Application Hosting (Backend + Frontend)

#### **Railway.app** ⭐ (Recommended for Quantum)
- **Free Tier**: $5 credit/month, unused credits roll over
- **Pros**: PostgreSQL, Redis, easy Docker deployment, automatic HTTPS
- **Setup**: Connect GitHub → Deploy
- **Good for**: Backend (Django), PostgreSQL, Redis, Frontend (static)
- **URL**: [railway.app](https://railway.app)

#### **Render.com** ⭐
- **Free Tier**: Unlimited services, 750 hours/month
- **Pros**: Auto-deploy from Git, PostgreSQL included, background workers
- **Cons**: Services sleep after 15min inactivity (restarts in ~30s)
- **Good for**: Backend, PostgreSQL, static frontend
- **URL**: [render.com](https://render.com)

#### **Fly.io**
- **Free Tier**: 3 shared VMs (256MB RAM each), 3GB storage
- **Pros**: Global CDN, Docker-native, PostgreSQL free tier
- **Good for**: Backend, Keycloak, Frontend
- **URL**: [fly.io](https://fly.io)

#### **Vercel** (Frontend Only)
- **Free Tier**: Unlimited deployments, 100GB bandwidth/month
- **Pros**: Optimized for Angular/React, automatic HTTPS, global CDN
- **Good for**: Angular frontend only
- **URL**: [vercel.com](https://vercel.com)

### 2. Database Services (PostgreSQL)

#### **Supabase** ⭐ (Recommended)
- **Free Tier**: 500MB database, 2GB file storage, 50k monthly active users
- **Pros**: PostgreSQL + Auth + Storage + Real-time subscriptions
- **Cons**: Pauses after 7 days inactivity (auto-resumes on connection)
- **URL**: [supabase.com](https://supabase.com)

#### **Neon** ⭐
- **Free Tier**: 1 project, 10 branches, 3GB storage
- **Pros**: Serverless PostgreSQL, instant branching, no sleep time
- **URL**: [neon.tech](https://neon.tech)

#### **ElephantSQL**
- **Free Tier**: 20MB storage (Tiny Turtle plan)
- **Pros**: Managed PostgreSQL, automatic backups
- **Cons**: Very limited storage
- **URL**: [elephantsql.com](https://elephantsql.com)

#### **Railway PostgreSQL** (if using Railway for backend)
- **Free**: Included in Railway $5/month credit
- **Pros**: Same network as your app, fast connections

### 3. Redis / Caching

#### **Upstash Redis** ⭐ (Recommended)
- **Free Tier**: 10,000 commands/day, 256MB storage
- **Pros**: Serverless, REST API, global replication
- **URL**: [upstash.com](https://upstash.com)

#### **Redis Cloud**
- **Free Tier**: 30MB RAM, 30 connections
- **Pros**: Managed by Redis Labs
- **URL**: [redis.com/cloud](https://redis.com/try-free)

#### **Railway Redis** (if using Railway)
- **Free**: Included in Railway credit

### 4. Message Queue (RabbitMQ / Celery Broker)

#### **CloudAMQP** ⭐
- **Free Tier**: "Little Lemur" - 1M messages/month
- **Pros**: Hosted RabbitMQ, management UI
- **URL**: [cloudamqp.com](https://cloudamqp.com)

#### **Upstash for Celery** (Alternative)
- Use Upstash Redis as Celery broker instead of RabbitMQ
- More generous free tier than CloudAMQP

### 5. Authentication (Keycloak)

#### **Self-Hosted on Railway/Render**
- Deploy Keycloak Docker image
- Use free PostgreSQL from same provider
- **Note**: Keycloak is RAM-heavy (~512MB minimum)

#### **Alternative: Supabase Auth**
- Replace Keycloak with Supabase's built-in authentication
- Free tier includes unlimited users
- Would require refactoring auth implementation

### 6. Object Storage (for uploaded files)

#### **Cloudflare R2** ⭐ (Recommended)
- **Free Tier**: 10GB storage, 1M Class A requests/month
- **Pros**: S3-compatible, no egress fees, fast CDN
- **URL**: [cloudflare.com/products/r2](https://developers.cloudflare.com/r2)

#### **Supabase Storage** (if using Supabase)
- **Free Tier**: 2GB storage included
- **Pros**: Integrated with Supabase Auth

#### **Backblaze B2**
- **Free Tier**: 10GB storage, 1GB download/day
- **Pros**: S3-compatible, very cheap paid tier

---

## 📊 Recommended Free Stack for Quantum + Plannr

### Option A: All-in-One (Simplest)
- **Backend**: Railway (Django, Celery workers)
- **Database**: Railway PostgreSQL
- **Redis**: Railway Redis
- **Message Queue**: CloudAMQP (RabbitMQ)
- **Frontend**: Vercel (Angular)
- **Auth**: Railway Keycloak
- **Storage**: Cloudflare R2
- **Cost**: ~$0-5/month (mostly free, Railway credit)

### Option B: Maximum Free Resources
- **Backend**: Render (Django)
- **Database**: Supabase (PostgreSQL)
- **Redis**: Upstash
- **Message Queue**: Upstash Redis (Celery broker)
- **Frontend**: Vercel (Angular)
- **Auth**: Supabase Auth (replace Keycloak)
- **Storage**: Supabase Storage
- **Cost**: $0/month (100% free)

### Option C: Fly.io Stack
- **Everything**: Fly.io (3 free VMs)
  - VM 1: Backend + Celery
  - VM 2: PostgreSQL + Redis
  - VM 3: Frontend (Nginx)
- **Message Queue**: CloudAMQP
- **Storage**: Cloudflare R2
- **Cost**: $0/month

---

## 🚀 Quick Start: Deploy to Railway (Recommended)

### 1. Sign up for Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login
```

### 2. Create Services
```bash
# From project root
railway init

# Add PostgreSQL
railway add postgresql

# Add Redis
railway add redis

# Deploy backend
cd backend
railway up

# Deploy frontend
cd ../frontend
railway up
```

### 3. Set Environment Variables
In Railway dashboard, add:
- `CLAUDE_API_KEY`
- `DATABASE_URL` (auto-set by PostgreSQL service)
- `REDIS_URL` (auto-set by Redis service)
- All other env vars from `.env.example`

### 4. Run Migrations
```bash
railway run python manage.py migrate
```

---

## 📝 Notes

- **Railway**: Best balance of free tier and ease of use
- **Render**: Great if you need more compute time (750 hrs vs Railway's $5 credit)
- **Fly.io**: Best for global deployment, more complex setup
- **Supabase**: Great if you want to replace Keycloak with simpler auth

For production, consider paid tiers for guaranteed uptime and resources.
