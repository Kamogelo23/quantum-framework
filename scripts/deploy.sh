#!/bin/bash

# Deployment script for Quantum to Kubernetes

set -e

NAMESPACE="quantum"
KUBECTL="kubectl"

echo "======================================"
echo "Deploying Quantum to Kubernetes"
echo "======================================"
echo ""

# Create namespace
echo "Creating namespace..."
$KUBECTL apply -f k8s/namespace.yaml

# Deploy PostgreSQL
echo "Deploying PostgreSQL..."
$KUBECTL apply -f k8s/postgres/statefulset.yaml

# Deploy Kafka and Zookeeper
echo "Deploying Kafka..."
$KUBECTL apply -f k8s/kafka/kafka.yaml

# Wait for databases to be ready
echo "Waiting for PostgreSQL to be ready..."
$KUBECTL wait --for=condition=ready pod -l app=quantum-postgres -n $NAMESPACE --timeout=300s

# Deploy backend configuration
echo "Deploying backend configuration..."
$KUBECTL apply -f k8s/backend/config.yaml

# Deploy ML service
echo "Deploying ML service..."
$KUBECTL apply -f k8s/ml-service/deployment.yaml

# Deploy backend
echo "Deploying backend..."
$KUBECTL apply -f k8s/backend/deployment.yaml

# Deploy Keycloak (if needed)
echo "Deploying Keycloak..."
$KUBECTL apply -f k8s/keycloak/deployment.yaml

# Deploy ingress
echo "Deploying ingress..."
$KUBECTL apply -f k8s/ingress/ingress.yaml

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""
echo "Check deployment status:"
echo "  kubectl get pods -n $NAMESPACE"
echo ""
echo "Check services:"
echo "  kubectl get svc -n $NAMESPACE"
echo ""
echo "Check ingress:"
echo "  kubectl get ingress -n $NAMESPACE"
