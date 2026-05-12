#!/bin/bash
# AgriChain Carbon AI - Production Deployment Script
set -e

ENV=${1:-production}
COMPOSE_FILE="deployment/docker-compose.yml"

echo "================================================"
echo "  AgriChain Carbon AI - Deployment"
echo "  Environment: $ENV"
echo "================================================"

# Load environment
if [ -f "backend/.env.$ENV" ]; then
    export $(cat backend/.env.$ENV | xargs)
elif [ -f "backend/.env" ]; then
    export $(cat backend/.env | xargs)
fi

# Build and deploy
echo "Building Docker images..."
docker-compose -f $COMPOSE_FILE build

echo "Stopping existing services..."
docker-compose -f $COMPOSE_FILE down || true

echo "Starting services..."
docker-compose -f $COMPOSE_FILE up -d

echo "Waiting for backend health check..."
for i in {1..30}; do
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        echo "Backend is healthy"
        break
    fi
    sleep 2
done

echo "Running database migrations..."
docker-compose -f $COMPOSE_FILE exec -T postgres psql -U agrichain -d agrichain -f /docker-entrypoint-initdb.d/001_initial.sql

echo ""
echo "================================================"
echo "  Deployment Complete!"
echo "================================================"
echo "Frontend:    http://localhost"
echo "API:         http://localhost:8000"
echo "API Docs:    http://localhost:8000/docs"
echo "AI Engine:   http://localhost:8001"
echo ""
echo "Monitor:     docker-compose -f $COMPOSE_FILE logs -f"
echo ""
