# Harbor Container Registry Setup

## Overview
Harbor is an open-source container registry that secures artifacts with policies and role-based access control.

## Installation

### Prerequisites
- Kubernetes cluster with Helm 3+
- kubectl configured
- Domain name for Harbor

### Install Harbor using Helm

```bash
# Add Harbor Helm repository
helm repo add harbor https://helm.goharbor.io
helm repo update

# Create namespace
kubectl create namespace harbor

# Install Harbor
helm install harbor harbor/harbor \
  --namespace harbor \
  --set expose.type=ingress \
  --set expose.ingress.hosts.core=harbor.yourdomain.com \
  --set externalURL=https://harbor.yourdomain.com \
  --set harborAdminPassword=CHANGE_ME \
  --set persistence.enabled=true \
  --set persistence.persistentVolumeClaim.registry.size=100Gi
```

## Configuration for Quantum

### 1. Create Quantum Project

1. Login to Harbor UI: `https://harbor.yourdomain.com`
2. Username: `admin`, Password: (set during installation)
3. Create a new project named `quantum`
4. Set project to **Private**

### 2. Create Robot Account

1. Go to quantum project → Robot Accounts
2. Create new robot account: `quantum-deployer`
3. Grant permissions:
   - Pull repository
   - Push repository
4. Save the token securely

### 3. Configure Kubernetes Secret

```bash
# Create docker registry secret
kubectl create secret docker-registry harbor-secret \
  --namespace=quantum \
  --docker-server=harbor.yourdomain.com \
  --docker-username=robot\$quantum-deployer \
  --docker-password=YOUR_ROBOT_TOKEN \
  --docker-email=admin@quantum.local
```

### 4. Update Deployments

Add to deployment specs:

```yaml
spec:
  template:
    spec:
      imagePullSecrets:
      - name: harbor-secret
```

## Docker Login

```bash
# Login to Harbor from Docker CLI
docker login harbor.yourdomain.com
Username: robot$quantum-deployer
Password: YOUR_ROBOT_TOKEN
```

## Image Naming Convention

```
harbor.yourdomain.com/quantum/[service]:[tag]

Examples:
- harbor.yourdomain.com/quantum/backend:v1.0.0
- harbor.yourdomain.com/quantum/frontend:v1.0.0
- harbor.yourdomain.com/quantum/ml-service:v1.0.0
```

## Build and Push Script

See `scripts/build-and-push.sh` for automated image building and pushing.

## Vulnerability Scanning

Harbor automatically scans images for vulnerabilities. Configure scanning policies:

1. Go to Interrogation Services
2. Enable automatic scanning on push
3. Set vulnerability threshold
4. Enable image signing (optional)

## Replication (Optional)

For high availability, configure replication to backup registry:

1. Go to Registries → New Endpoint
2. Add backup Harbor instance
3. Create replication rule

## Maintenance

### Garbage Collection

Enable automatic garbage collection to clean up unused images:

1. Go to Configuration → Garbage Collection
2. Set schedule (e.g., weekly)
3. Enable

### Backup

Backup Harbor data:

```bash
# Backup Harbor database
kubectl exec -n harbor harbor-database-0 -- \
  pg_dump -U postgres harbor > harbor-backup-$(date +%Y%m%d).sql
```

## Troubleshooting

### Cannot pull images

Check:
1. Image name is correct
2. Robot account has pull permission
3. Kubernetes secret is created
4. imagePullSecrets is configured

### Push fails

Check:
1. You are logged in: `docker login harbor.yourdomain.com`
2. Project exists
3. Robot account has push permission
