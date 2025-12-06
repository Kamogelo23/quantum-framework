# Oracle Cloud Infrastructure (OCI) Free Tier Setup Guide

Complete guide for setting up Oracle Cloud Free Tier and deploying the Quantum platform.

## Why Oracle Cloud Free Tier?

✅ **Always Free Resources:**
- 4 ARM-based Ampere A1 cores (or 2 AMD x64 cores)
- 24GB RAM
- 200GB block storage
- 10TB/month outbound data transfer
- **Forever free, no credit card expiration!**

## Step-by-Step Signup

### 1. Create Oracle Cloud Account

1. **Visit** https://www.oracle.com/cloud/free/
2. Click **"Start for free"**
3. Fill in account details:
   - Country/Territory
   - Email address
   - Verify email (check inbox)
4. Create account:
   - Account name (e.g., "quantum-platform")
   - Home region (choose closest to you - **cannot be changed later!**)
   - Cloud account name (e.g., "quantumcloud")
5. **Payment verification** (required but won't be charged):
   - Add credit/debit card
   - $1 temporary hold (refunded)
   - Or add promo code if youhave one
6. Complete registration

### 2. Access Console

1. Go to https://cloud.oracle.com
2. Login with your email and password
3. You'll see the OCI Console dashboard

## Deploy Quantum on OCI Free Tier

### Option 1: Single VM with Docker Compose (Easiest)

#### Step 1: Create Virtual Machine

1. In OCI Console, navigate to **Compute** → **Instances**
2. Click **"Create Instance"**
3. Configure:
   - **Name**: `quantum-server`
   - **Image**: Ubuntu 22.04
   - **Shape**: Click "Change shape"
     - Series: Ampere
     - Shape: VM.Standard.A1.Flex
     - OCPUs: 4 (maximum free tier)
     - Memory: 24 GB (maximum free tier)
   - **Network**: Use default VCN (or create new)
   - **Add SSH keys**: Upload your public key or generate new
   - Click **"Create"**

#### Step 2: Configure Security List

1. Navigate to **Networking** → **Virtual Cloud Networks**
2. Click your VCN → **Security Lists** → **Default Security List**
3. Click **"Add Ingress Rules"** for each port:

| Description | Source CIDR | IP Protocol | Destination Port |
|-------------|-------------|-------------|------------------|
| HTTP | 0.0.0.0/0 | TCP | 80 |
| HTTPS | 0.0.0.0/0 | TCP | 443 |
| Keycloak | 0.0.0.0/0 | TCP | 8080 |
| Backend API | 0.0.0.0/0 | TCP | 8000 |
| Frontend | 0.0.0.0/0 | TCP | 4200 |

⚠️ **Security Note**: For production, restrict source CIDR to your IP or use a load balancer.

#### Step 3: Configure Firewall on VM

SSH into your VM and run:

```bash
# Get public IP from OCI console
ssh -i ~/.ssh/your-key.pem ubuntu@<PUBLIC_IP>

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Open firewall ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8080/tcp  # Keycloak
sudo ufw allow 8000/tcp  # Backend
sudo ufw allow 4200/tcp  # Frontend
sudo ufw enable
```

#### Step 4: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again
exit
```

#### Step 5: Deploy Quantum

```bash
# SSH back in
ssh -i ~/.ssh/your-key.pem ubuntu@<PUBLIC_IP>

# Clone repository (or upload via SCP)
git clone https://github.com/yourusername/quantum-framework.git
cd quantum-framework

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

#### Step 6: Access Services

Replace `<PUBLIC_IP>` with your VM's public IP:

- **Frontend**: http://\<PUBLIC_IP\>:4200
- **Backend API**: http://\<PUBLIC_IP\>:8000
- **API Docs**: http://\<PUBLIC_IP\>:8000/api/docs
- **Keycloak**: http://\<PUBLIC_IP\>:8080

### Option 2: Kubernetes with K3s (Advanced)

For production-grade deployment with auto-scaling:

```bash
# Install K3s (lightweight Kubernetes)
curl -sfL https://get.k3s.io | sh -

# Wait for K3s to start
sudo systemctl status k3s

# Get kubeconfig
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER ~/.kube/config

# Verify
kubectl get nodes

# Deploy Quantum
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/postgres/statefulset.yaml
kubectl apply -f k8s/backend/config.yaml
kubectl apply -f k8s/backend/deployment.yaml
kubectl apply -f k8s/keycloak/deployment.yaml
kubectl apply -f k8s/ingress/ingress.yaml

# Check deployment
kubectl get pods -n quantum
```

## Cost Management

### Staying Within Free Tier

✅ **Always Free Services** (no expiration):
- 2 VM instances (Ampere A1 with 4 OCPUs + 24GB RAM total)
- 2 Block Volumes (200GB total)
- 10GB Object Storage
- Load Balancer (10 Mbps)

⚠️ **Be Careful With**:
- Additional VMs beyond free tier
- x86 VMs (only AMD free tier is 2 VCPUs)
- Backup storage
- Data transfer > 10TB/month

### Monitoring Costs

1. Navigate to **Billing & Cost Management**
2. Set up **Budget Alerts**:
   - Budget: $1/month
   - Alert at: 80%, 100%

## DNS Configuration (Optional)

### Using OCI DNS

1. Navigate to **Networking** → **DNS Management**
2. Create zone: `quantum.yourdomain.com`
3. Add A records:
   - `quantum.yourdomain.com` → `<PUBLIC_IP>`
   - `api.quantum.yourdomain.com` → `<PUBLIC_IP>`
   - `auth.quantum.yourdomain.com` → `<PUBLIC_IP>`

### Using Cloudflare (Free)

1. Add your domain to Cloudflare
2. Create A records pointing to your OCI public IP
3. Enable **Proxy** for free SSL/TLS

## SSL/TLS Setup

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d quantum.yourdomain.com

# Auto-renewal is configured automatically
sudo systemctl status certbot.timer
```

## Backup Strategy

### Automated Backups

```bash
# Create backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f /home/ubuntu/quantum-framework/docker-compose.yml exec -T postgres \
  pg_dump -U quantum quantum > /home/ubuntu/backups/quantum_$DATE.sql
# Keep only last 7 days
find /home/ubuntu/backups -name "*.sql" -mtime +7 -delete
EOF

chmod +x ~/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/backup.sh") | crontab -
```

## Troubleshooting

### VM Out of Memory

```bash
# Check memory usage
free -h

# Add swap (if not present)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Cannot Access Services

```bash
# Check if ports are open
sudo netstat -tlnp | grep -E '(8000|8080|4200)'

# Check Docker
docker-compose ps
docker-compose logs backend

# Check firewall
sudo ufw status
```

### Services Slow

1. Check resource usage: `htop`
2. Reduce Docker services:
   ```bash
   # Run only essential services
   docker-compose up -d postgres redis backend keycloak
   ```

## Next Steps

1. ✅ Sign up for Oracle Cloud Free Tier
2. ✅ Create Ubuntu VM with maximum resources (4 OCPUs, 24GB RAM)
3. ✅ Configure security lists and firewall
4. ✅ Install Docker and Docker Compose
5. ✅ Deploy Quantum with `docker-compose up -d`
6. ✅ Configure DNS (optional)
7. ✅ Set up SSL with Let's Encrypt (optional)
8. ✅ Configure automated backups

**Resources:**
- OCI Documentation: https://docs.oracle.com/en-us/iaas/
- Free Tier FAQ: https://www.oracle.com/cloud/free/faq.html
- Community Forum: https://cloudcustomerconnect.oracle.com/

Need help? Open an issue on GitHub!
