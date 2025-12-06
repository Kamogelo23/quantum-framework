#!/bin/bash

# Build and Push Script for Quantum Services
# This script builds Docker images and pushes them to Harbor registry

set -e

# Configuration
HARBOR_REGISTRY="${HARBOR_REGISTRY:-harbor.yourdomain.com}"
PROJECT="quantum"
VERSION="${VERSION:-latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}Quantum Build and Push Script${NC}"
echo -e "${GREEN}====================================${NC}"
echo ""

# Check if logged in to Harbor
echo -e "${YELLOW}Checking Harbor login...${NC}"
if ! docker info | grep -q "$HARBOR_REGISTRY"; then
    echo -e "${RED}Not logged in to Harbor. Please run:${NC}"
    echo "  docker login $HARBOR_REGISTRY"
    exit 1
fi

echo -e "${GREEN}✓ Logged in to Harbor${NC}"
echo ""

# Build and push backend
echo -e "${YELLOW}Building backend service...${NC}"
cd backend
docker build -t "$HARBOR_REGISTRY/$PROJECT/backend:$VERSION" .
docker push "$HARBOR_REGISTRY/$PROJECT/backend:$VERSION"
echo -e "${GREEN}✓ Backend pushed${NC}"
cd ..

# Build and push ML service
echo -e "${YELLOW}Building ML service...${NC}"
cd ml-service
docker build -t "$HARBOR_REGISTRY/$PROJECT/ml-service:$VERSION" .
docker push "$HARBOR_REGISTRY/$PROJECT/ml-service:$VERSION"
echo -e "${GREEN}✓ ML service pushed${NC}"
cd ..

# Build and push frontend
echo -e "${YELLOW}Building frontend...${NC}"
cd frontend
docker build -t "$HARBOR_REGISTRY/$PROJECT/frontend:$VERSION" .
docker push "$HARBOR_REGISTRY/$PROJECT/frontend:$VERSION"
echo -e "${GREEN}✓ Frontend pushed${NC}"
cd ..

echo ""
echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}All images pushed successfully!${NC}"
echo -e "${GREEN}====================================${NC}"
echo ""
echo "Images:"
echo "  - $HARBOR_REGISTRY/$PROJECT/backend:$VERSION"
echo "  - $HARBOR_REGISTRY/$PROJECT/ml-service:$VERSION"
echo "  - $HARBOR_REGISTRY/$PROJECT/frontend:$VERSION"
echo ""
echo "Next steps:"
echo "  1. Update k8s manifests with new image tags"
echo "  2. Deploy to Kubernetes: kubectl apply -f k8s/"
