@echo off
echo ========================================
echo Quantum Framework - Local Startup
echo ========================================
echo.

echo [1/4] Starting Docker services...
docker-compose up -d postgres redis keycloak
echo Waiting for services to be ready (30 seconds)...
timeout /t 30 /nobreak

echo.
echo [2/4] Checking service health...
docker-compose ps

echo.
echo [3/4] Running backend migrations...
cd backend
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo Error: Migration failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Services are ready!
echo ========================================
echo Next steps:
echo   1. Start backend:  python manage.py runserver
echo   2. In new terminal, start frontend:  npm run start
echo   3. Visit: http://localhost:4200/plannr
echo ========================================
echo.
echo Press any key to start backend server...
pause

echo Starting Django development server...
python manage.py runserver
