#!/bin/bash
# AgriChain Carbon AI - Setup Script
set -e

echo "================================================"
echo "  AgriChain Carbon AI - Setup Script"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓ $1 found${NC}"
        return 0
    else
        echo -e "${RED}✗ $1 not found${NC}"
        return 1
    fi
}

check_command python3
check_command pip3
check_command node
check_command npm
check_command docker
check_command docker-compose

echo ""

# Setup Python virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Setup smart contract dependencies
echo -e "${YELLOW}Setting up smart contract dependencies...${NC}"
cd contracts
npm install
cd ..
echo -e "${GREEN}✓ Contract dependencies installed${NC}"

# Setup environment file
if [ ! -f backend/.env ]; then
    echo -e "${YELLOW}Creating environment file...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Setup database
echo -e "${YELLOW}Setting up database...${NC}"
if docker ps | grep -q agrichain-postgres; then
    echo -e "${GREEN}✓ Database already running${NC}"
else
    echo -e "${YELLOW}Starting PostgreSQL with Docker...${NC}"
    docker run -d --name agrichain-postgres \
        -e POSTGRES_DB=agrichain \
        -e POSTGRES_USER=agrichain \
        -e POSTGRES_PASSWORD=agrichain \
        -p 5432:5432 \
        postgres:15-alpine
    sleep 3
    echo -e "${GREEN}✓ Database started${NC}"
fi

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
PGPASSWORD=agrichain psql -h localhost -U agrichain -d agrichain -f database/migrations/001_initial.sql 2>/dev/null || true

# Seed data
echo -e "${YELLOW}Seeding test data...${NC}"
PGPASSWORD=agrichain psql -h localhost -U agrichain -d agrichain -f database/seeds/001_seed_data.sql 2>/dev/null || true

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Start the backend:"
echo "  source .venv/bin/activate"
echo "  cd backend && uvicorn app.main:app --reload"
echo ""
echo "Start the AI Engine:"
echo "  cd ai-engine && uvicorn main:app --port 8001 --reload"
echo ""
echo "Start with Docker:"
echo "  docker-compose -f deployment/docker-compose.yml up"
echo ""
echo "Open Frontend:"
echo "  open frontend/index.html"
echo ""
