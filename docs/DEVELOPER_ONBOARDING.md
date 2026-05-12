# AgriChain Carbon AI — Developer Onboarding Guide

## Welcome

This guide will help you get up to speed with the AgriChain Carbon AI codebase. The platform is built with **zero JavaScript frameworks** on the frontend and follows **clean architecture** principles throughout.

## Project Overview

### Tech Stack
- **Frontend**: Pure HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python FastAPI, SQLAlchemy, PostgreSQL
- **AI/ML**: Scikit-learn, NumPy, GeoPandas
- **Blockchain**: Solidity, OpenZeppelin, Web3.py
- **Infrastructure**: Docker, Nginx, Gunicorn

### Architecture Principles

1. **Clean Architecture**: API → Service → Repository → Model
2. **No Circular Dependencies**: Layers only depend inward
3. **Stateless Backend**: Horizontally scalable
4. **Offline-First Frontend**: Works in low-connectivity environments

## Repository Structure

```
agrichain-carbon-ai/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/       # Route handlers (controllers)
│   │   ├── services/  # Business logic
│   │   ├── repositories/ # Data access
│   │   ├── models/    # SQLAlchemy ORM models
│   │   └── schemas/   # Pydantic request/response schemas
│   └── tests/         # Backend tests
│
├── frontend/          # Static HTML/CSS/JS
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript modules
│   └── *.html         # Pages
│
├── contracts/         # Solidity smart contracts
├── ai-engine/         # Python AI/ML services
├── database/          # SQL migrations and seeds
├── deployment/        # Docker, nginx, monitoring
├── docs/              # Documentation
└── scripts/           # Setup and deployment scripts
```

## Development Setup

### Prerequisites
```bash
# Required
python3 --version     # 3.11+
node --version        # 18+
docker --version      # 24+
psql --version       # 15+

# Install system deps (Ubuntu/Debian)
sudo apt-get install python3-dev libpq-dev gdal-bin
```

### First-Time Setup

```bash
# 1. Clone and enter project
git clone <repo-url>
cd agrichain-carbon-ai

# 2. Run automated setup
chmod +x scripts/setup/setup.sh
./scripts/setup/setup.sh

# 3. Activate Python environment
source .venv/bin/activate

# 4. Start PostgreSQL (Docker or local)
docker run -d --name agrichain-postgres \
    -e POSTGRES_DB=agrichain \
    -e POSTGRES_USER=agrichain \
    -e POSTGRES_PASSWORD=agrichain \
    -p 5432:5432 postgres:15-alpine

# 5. Run migrations
psql -U agrichain -d agrichain -f database/migrations/001_initial.sql

# 6. Start backend
cd backend && uvicorn app.main:app --reload --port 8000

# 7. Start AI engine (new terminal)
cd ai-engine && uvicorn main:app --reload --port 8001

# 8. Open frontend
open frontend/index.html
```

## Coding Standards

### Python
```python
# Follow PEP 8
# Use type hints everywhere
# Docstrings for public functions

def calculate_carbon_offset(area: float, crop_type: str) -> float:
    """Calculate carbon offset in tCO2e."""
    rates = {"maize": 3.2, "coffee": 4.5}
    return area * rates.get(crop_type, 2.5)
```

### JavaScript (Vanilla)
```javascript
// No frameworks, no imports
// Use descriptive function names
// Handle errors gracefully

async function loadFarmData(farmId) {
    try {
        const data = await api.get(`/farms/${farmId}`);
        renderFarmCard(data);
    } catch (error) {
        showError('Failed to load farm data');
    }
}
```

### CSS
```css
/* Use CSS custom properties */
/* Mobile-first responsive */
/* No preprocessors */

.farm-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}
```

## API Conventions

- All endpoints prefixed with `/api`
- Authentication via Bearer JWT tokens
- Responses always JSON
- Errors follow `{"detail": "message"}` format
- Pagination via `page` and `per_page` query params

## Testing

```bash
# Backend tests
cd backend && pytest tests/ -v --cov=app

# Contract tests
cd contracts && npx hardhat test

# AI engine tests
cd ai-engine && python -m pytest tests/ -v

# Run all
pytest backend/tests/ ai-engine/tests/ -v
```

## Common Tasks

### Adding a New API Endpoint

1. Define Pydantic schema in `backend/app/schemas/`
2. Create repository method in `backend/app/repositories/`
3. Add business logic in `backend/app/services/`
4. Create route in `backend/app/api/`
5. Register router in `backend/app/main.py`
6. Write tests in `backend/tests/`

### Adding a New Database Table

1. Create SQLAlchemy model in `backend/app/models/`
2. Add migration in `database/migrations/`
3. Create repository in `backend/app/repositories/`
4. Update seed data in `database/seeds/`

### Adding a New Frontend Page

1. Create HTML file in `frontend/`
2. Add CSS in `frontend/css/styles.css`
3. Add JavaScript in `frontend/js/`
4. Link from navigation sidebar

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add carbon estimate export"

# Push and create PR
git push origin feature/my-feature
# Create PR via GitHub interface
```

### Commit Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code restructuring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

## Troubleshooting

### Database Connection Failed
```bash
# Is PostgreSQL running?
pg_isready
# Start if needed: sudo service postgresql start
```

### Port Already in Use
```bash
# Find process on port 8000
lsof -i :8000
kill -9 <PID>
```

### Module Not Found
```bash
# Activate virtual environment
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Getting Help

- Check `docs/` directory for detailed documentation
- Review existing code for patterns
- Ask in team channels

---

*"Building the infrastructure for climate finance worldwide."*
