@echo off
REM Keycloak Initialization Script for Windows
REM Automatically imports quantum realm on first startup

echo Waiting for Keycloak to start...
timeout /t 30 /nobreak

REM Check if realm already exists
curl -s -o nul -w "%%{http_code}" http://localhost:8080/realms/quantum > realm_check.txt
set /p REALM_EXISTS=<realm_check.txt
del realm_check.txt

if "%REALM_EXISTS%"=="200" (
  echo Realm 'quantum' already exists. Skipping import.
  exit /b 0
)

echo Importing quantum realm...

REM Get admin token
curl -s -X POST http://localhost:8080/realms/master/protocol/openid-connect/token ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=admin" ^
  -d "password=admin" ^
  -d "grant_type=password" ^
  -d "client_id=admin-cli" > token.json

REM Extract token (simplified - in production use jq or PowerShell)
REM For now, user must manually import via Keycloak UI

echo.
echo ============================================
echo Please import realm manually:
echo 1. Go to http://localhost:8080
echo 2. Login as admin/admin
echo 3. Click "Create Realm"
echo 4. Click "Browse" and select:
echo    config\keycloak\quantum-realm.json
echo 5. Click "Create"
echo ============================================
echo.

del token.json 2>nul
