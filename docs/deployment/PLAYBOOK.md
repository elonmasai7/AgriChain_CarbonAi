# AgriChain Carbon AI — Deployment Playbook

## Production Architecture

```
Internet
    │
    ▼
Cloudflare (DNS, DDoS, CDN)
    │
    ▼
Nginx (SSL termination, reverse proxy, load balancing)
    │
    ├── Frontend Static (S3/CDN)
    │
    ├── Backend API (Auto-scaling group, 4+ instances)
    │   └── PostgreSQL RDS (Multi-AZ, read replica)
    │   └── Redis ElastiCache (Cluster mode)
    │
    ├── AI Engine (Spot instances, GPU optional)
    │
    └── Monitoring (CloudWatch/Prometheus + Grafana)
```

## AWS Deployment

### Prerequisites
```bash
# Install AWS CLI
# Configure: aws configure
# Create ECR repository
# Create ECS cluster
```

### Deploy Infrastructure

```bash
# Create ECS service
aws ecs create-service \
    --cluster agrichain-production \
    --service-name agrichain-backend \
    --task-definition agrichain-backend:1 \
    --desired-count 4 \
    --launch-type FARGATE

# Create RDS PostgreSQL
aws rds create-db-instance \
    --db-instance-identifier agrichain-db \
    --db-instance-class db.t3.large \
    --engine postgres \
    --master-username agrichain \
    --master-user-password <secure-password>

# Create ElastiCache Redis
aws elasticache create-cache-cluster \
    --cache-cluster-id agrichain-redis \
    --cache-node-type cache.t3.medium \
    --engine redis
```

## Monitoring Setup

### Prometheus Metrics
```yaml
# Backend metrics (auto-exported)
agrichain_requests_total{method, endpoint, status}
agrichain_request_duration_seconds
agrichain_active_users
agrichain_carbon_estimated_total
agrichain_fraud_alerts_total
agrichain_blockchain_tx_total
```

### Grafana Dashboards
- **System Health**: CPU, memory, disk, network
- **API Performance**: Request rate, latency, error rate
- **Business Metrics**: Carbon estimated, marketplace volume, users
- **Blockchain**: Transaction count, gas costs, contract events

### Alerts
```yaml
critical:
  - API error rate > 5% for 5 minutes
  - P99 latency > 2s for 5 minutes
  - Disk usage > 85%
  - Database connection pool exhausted
  - Smart contract deployment failure

warning:
  - CPU > 70% for 15 minutes
  - Memory > 80% for 15 minutes
  - Fraud detection rate spike > 200%
  - SSL certificate expires < 30 days
```

## CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/tests/
      - run: cd contracts && npm install && npx hardhat test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build -f deployment/Dockerfile -t backend .
      - run: docker push <ecr>/agrichain-backend:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: aws ecs update-service --cluster agrichain --service backend --force-new-deployment
```

## Backup Strategy

### Database
- Automated daily snapshots (RDS automated)
- Point-in-time recovery enabled (35 day retention)
- Weekly manual exports to S3
- Cross-region backup for disaster recovery

### File Storage
- S3 with versioning enabled
- Cross-region replication
- 30-day lifecycle to Glacier for archive

### Emergency Recovery

```bash
# 1. Restore database from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier agrichain-restored \
    --db-snapshot-identifier agrichain-snapshot-latest

# 2. Promote restored instance
aws rds promote-read-replica \
    --db-instance-identifier agrichain-restored

# 3. Update DNS
# Route53 CNAME to new instance

# 4. Verify data integrity
# Run validation queries
```

## Rollback Procedure

```bash
# 1. Revert backend to previous Docker image
aws ecs update-service \
    --cluster agrichain \
    --service backend \
    --task-definition agrichain-backend:previous

# 2. Revert database if needed
# Use RDS point-in-time recovery

# 3. Verify health
curl https://api.agrichain.io/health

# 4. Monitor for 30 minutes
# Check error rates, latency, user reports
```

## Performance Tuning

### PostgreSQL
```sql
-- Recommended settings
shared_buffers = '2GB'
effective_cache_size = '6GB'
maintenance_work_mem = '512MB'
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = '64MB'
```

### Gunicorn
```ini
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'
max_requests = 1000
max_requests_jitter = 100
timeout = 120
```

### Nginx
```nginx
worker_processes auto;
worker_connections 1024;
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

## Security Checklist (Production)

- [ ] SSL certificate installed and auto-renewing
- [ ] WAF rules active (SQLi, XSS, RFI)
- [ ] DDoS protection enabled
- [ ] Security headers verified
- [ ] Database in VPC, no public access
- [ ] Secrets in AWS Secrets Manager
- [ ] IAM roles with least privilege
- [ ] CloudTrail enabled
- [ ] GuardDuty active
- [ ] Regular security scanning scheduled
