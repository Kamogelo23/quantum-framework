# Keycloak Setup Guide

Complete guide for setting up and configuring Keycloak for the Quantum platform with group-based role mapping.

## Quick Start (Docker Compose)

The easiest way to get started is using docker-compose:

```bash
# Start all services including Keycloak
docker-compose up -d

# Wait for Keycloak to start (about 30 seconds)
docker-compose logs -f keycloak
```

Keycloak will be available at **http://localhost:8080**

## Default Credentials

**Admin Console:**
- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

## Automatic Realm Import

The `quantum` realm is automatically imported on first startup with:

### Pre-configured Clients

1. **quantum-backend** (Confidential Client)
   - Client ID: `quantum-backend`
   - Client Secret: `quantum-backend-secret-change-in-production`
   - Used by Django backend for API authentication

2. **quantum-frontend** (Public Client)
   - Client ID: `quantum-frontend`
   - PKCE enabled for security
   - Used by Angular frontend

### Pre-configured Groups

| Group | Permissions | Description |
|-------|-------------|-------------|
| **quantum-admins** | Full Access | System administrators with all permissions |
| **quantum-developers** | Manage + Ingest | Can manage monitoring, ML models, ingest data |
| **quantum-analysts** | Query + ML | Can query data and run ML predictions |
| **quantum-viewers** | Read-Only | View-only access to all data |

### Test Users

| Username | Password | Group | Use Case |
|----------|----------|-------|----------|
| `admin` | `admin123` | quantum-admins | Full system access |
| `developer` | `developer123` | quantum-developers | Development testing |
| `analyst` | `analyst123` | quantum-analysts | Analytics testing |
| `viewer` | `viewer123` | quantum-viewers | Read-only testing |

⚠️ **Security Note**: All test user passwords are set to `temporary: true` and must be changed on first login.

## Testing Authentication

### 1. Get Access Token (Password Grant)

```bash
curl -X POST http://localhost:8080/realms/quantum/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=quantum-backend" \
  -d "client_secret=quantum-backend-secret-change-in-production" \
  -d "username=developer" \
  -d "password=developer123" \
  -d "grant_type=password"
```

Response will include:
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "expires_in": 300,
  "token_type": "Bearer"
}
```

### 2. Decode Token to View Groups

Visit **https://jwt.io** and paste the `access_token` to see:

```json
{
  "groups": [
    "/quantum-developers"
  ],
  "preferred_username": "developer",
  "email": "developer@quantum.local"
}
```

### 3. Test API with Token

```bash
# Replace YOUR_TOKEN with the access_token from step 1
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/monitoring/sources
```

## Manual Configuration (If Needed)

If automatic import fails, follow these steps:

### Step 1: Create Realm

1. Login to Keycloak admin console
2. Click dropdown next to "master" realm
3. Click "Create Realm"
4. Name: `quantum`
5. Click "Create"

### Step 2: Create Groups

1. Navigate to **Groups** in left menu
2. Click "Create group" for each:
   - `quantum-admins`
   - `quantum-developers`
   - `quantum-analysts`
   - `quantum-viewers`

### Step 3: Configure Backend Client

1. Navigate to **Clients**
2. Click "Create client"
3. General Settings:
   - Client ID: `quantum-backend`
   - Client Protocol: `openid-connect`
   - Click "Next"
4. Capability config:
   - ✅ Client authentication: ON
   - ✅ Authorization: OFF
   - ✅ Authentication flow: Standard flow, Direct access grants
   - Click "Next", then "Save"
5. Get Client Secret:
   - Navigate to **Credentials** tab
   - Copy the "Client secret"
   - Update in `.env`: `KEYCLOAK_CLIENT_SECRET=<copied-secret>`

### Step 4: Add Group Mapper

1. Still in `quantum-backend` client
2. Navigate to **Client scopes** tab
3. Click on `quantum-backend-dedicated`
4. Click **Add mapper** → **By configuration**
5. Select "Group Membership"
6. Configure:
   - Name: `groups`
   - Token Claim Name: `groups`
   - Full group path: OFF
   - Add to ID token: ON
   - Add to access token: ON
   - Add to userinfo: ON
7. Click "Save"

### Step 5: Configure Frontend Client

1. Navigate to **Clients**
2. Click "Create client"
3. General Settings:
   - Client ID: `quantum-frontend`
   - Click "Next"
4. Capability config:
   - ✅ Client authentication: OFF (Public client)
   - ✅ Standard flow: ON
   - Click "Save"
5. Settings tab:
   - Valid redirect URIs: `http://localhost:4200/*`
   - Valid post logout redirect URIs: `http://localhost:4200/*`
   - Web origins: `http://localhost:4200`
6. Advanced Settings:
   - Proof Key for Code Exchange Code Challenge Method: `S256`
7. Save

### Step 6: Create Users

1. Navigate to **Users**
2. Click "Add user"
3. Fill in details (example for developer):
   - Username: `developer`
   - Email: `developer@quantum.local`
   - First name: `Developer`
   - Last name: `User`
   - ✅ Email verified: ON
   - Click "Create"
4. Set password:
   - Navigate to **Credentials** tab
   - Click "Set password"
   - Password: `developer123`
   - Temporary: ON (forces password change on first login)
   - Click "Save"
5. Assign to group:
   - Navigate to **Groups** tab
   - Click "Join Group"
   - Select `quantum-developers`
   - Click "Join"

Repeat for other test users (admin, analyst, viewer).

## Production Deployment

### 1. Generate Secure Client Secret

```bash
openssl rand -base64 32
```

Update in both:
- Keycloak client configuration
- Django `.env` file: `KEYCLOAK_CLIENT_SECRET=<generated-secret>`

### 2. Update Redirect URIs

Replace `localhost` with your actual domain:
- `https://api.quantum.yourdomain.com/*`
- `https://quantum.yourdomain.com/*`

### 3. Enable HTTPS

Update realm settings:
- **SSL required**: `all requests`

### 4. Configure Email

For password reset functionality:
1. Navigate to **Realm settings** → **Email**
2. Configure SMTP settings
3. Test connection

### 5. Remove Test Users

Delete all test users and create real users:
1. Navigate to **Users**
2. Delete: admin, developer, analyst, viewer
3. Create real user accounts

## Troubleshooting

### Keycloak Won't Start

```bash
# Check logs
docker-compose logs keycloak

# Ensure PostgreSQL is healthy
docker-compose ps postgres

# Restart Keycloak
docker-compose restart keycloak
```

### "Invalid token" Error

- Check token expiration (default: 5 minutes)
- Verify `KEYCLOAK_SERVER_URL` matches actual URL
- Ensure client secret matches in both Keycloak and Django

### Groups Not in Token

1. Verify  group mapper is configured
2. Check user is actually in group
3. Decode JWT at jwt.io to verify groups claim

### Cannot Login with Test User

- Password may have expired
- Check user is enabled in Keycloak
- Verify group assignment

## Next Steps

1. ✅ Start Keycloak with docker-compose
2. ✅ Access admin console at http://localhost:8080
3. ✅ Verify realm `quantum` exists
4. ✅ Test login with `developer` / `developer123`
5. ✅ Get token and test API access
6. ✅ Verify groups in JWT token

Need help? Check the main README.md or open an issue!
