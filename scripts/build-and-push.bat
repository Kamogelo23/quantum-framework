@echo off
REM Build and Push Script for Quantum Services (Windows)
REM This script builds Docker images and pushes them to Harbor registry

setlocal

REM Configuration
if "%HARBOR_REGISTRY%"=="" set HARBOR_REGISTRY=harbor.yourdomain.com
set PROJECT=quantum
if "%VERSION%"=="" set VERSION=latest

echo ====================================
echo Quantum Build and Push Script
echo ====================================
echo.

echo Checking Harbor login...
docker info | findstr "%HARBOR_REGISTRY%" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Not logged in to Harbor. Please run:
    echo   docker login %HARBOR_REGISTRY%
    exit /b 1
)

echo [OK] Logged in to Harbor
echo.

REM Build and push backend
echo Building backend service...
cd backend
docker build -t %HARBOR_REGISTRY%/%PROJECT%/backend:%VERSION% .
docker push %HARBOR_REGISTRY%/%PROJECT%/backend:%VERSION%
echo [OK] Backend pushed
cd ..

REM Build and push ML service
echo Building ML service...
cd ml-service
docker build -t %HARBOR_REGISTRY%/%PROJECT%/ml-service:%VERSION% .
docker push %HARBOR_REGISTRY%/%PROJECT%/ml-service:%VERSION%
echo [OK] ML service pushed
cd ..

REM Build and push frontend
echo Building frontend...
cd frontend
docker build -t %HARBOR_REGISTRY%/%PROJECT%/frontend:%VERSION% .
docker push %HARBOR_REGISTRY%/%PROJECT%/frontend:%VERSION%
echo [OK] Frontend pushed
cd ..

echo.
echo ====================================
echo All images pushed successfully!
echo ====================================
echo.
echo Images:
echo   - %HARBOR_REGISTRY%/%PROJECT%/backend:%VERSION%
echo   - %HARBOR_REGISTRY%/%PROJECT%/ml-service:%VERSION%
echo   - %HARBOR_REGISTRY%/%PROJECT%/frontend:%VERSION%
echo.
echo Next steps:
echo   1. Update k8s manifests with new image tags
echo   2. Deploy to Kubernetes: kubectl apply -f k8s/

endlocal
