# AgriChain Carbon AI

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688)](https://fastapi.tiangolo.com)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.19-363636)](https://soliditylang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Enterprise Climate-Finance Platform** — Empowering African farmers to earn blockchain-based carbon credits through sustainable agriculture.

AgriChain Carbon AI is a production-grade platform that integrates **artificial intelligence**, **satellite intelligence**, **weather analytics**, and **blockchain verification** to estimate carbon sequestration and mint tokenized carbon assets. Organizations can purchase verified carbon credits through a transparent, decentralized marketplace.

---

## Mission

> *"To democratize carbon credit markets for African smallholder farmers by providing AI-powered verification, blockchain transparency, and a global marketplace — turning sustainable farming into a verifiable financial asset."*

---

## Features

### 1. Farmer Management System
- Secure farmer registration and authentication
- GPS farm mapping and profile management
- Crop, soil, and irrigation data management
- Sustainability practice tracking
- Image uploads with EXIF validation

### 2. AI Carbon Estimation Engine
- Multi-factor carbon sequestration modeling
- Crop-specific emission factors (IPCC methodology)
- Soil type, irrigation, and fertilizer impact analysis
- Sustainability practice scoring (agroforestry, cover crops, no-till)
- AI confidence scoring with explainable outputs

### 3. Satellite Intelligence Module
- NDVI (Normalized Difference Vegetation Index) analysis
- Land health scoring and vegetation trend detection
- Water stress index estimation
- Deforestation risk monitoring
- Historical vegetation time-series analysis

### 4. Blockchain Verification System
- ERC-721 Carbon Certificate NFTs
- ERC-20 Carbon Credit Tokens (ACCC)
- Multi-signature verification workflow
- Immutable on-chain audit trail
- Polygon / Celo / Base network support

### 5. Carbon Marketplace
- Real-time carbon credit listings
- ESG scoring and farm verification badges
- Credit purchasing with blockchain confirmation
- Credit retirement with immutable records
- Advanced filtering (price, tonnes, ESG score)

### 6. AI Sustainability Advisor
- Multilingual support (English, Swahili, French)
- Climate adaptation recommendations
- Water conservation advice
- Soil optimization guidance
- Crop rotation suggestions
- SMS-compatible and low-bandwidth modes

### 7. Fraud Detection Engine
- Duplicate farm detection (GPS proximity)
- Unrealistic carbon estimate validation
- Image manipulation detection
- Automated fraud risk scoring
- Auditor review queue with case management

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Static)                      │
│                HTML5 · CSS3 · Vanilla JS                     │
│          Farmer Dashboard · Marketplace · Advisor            │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS
┌────────────────────▼────────────────────────────────────────┐
│                    API GATEWAY (Nginx)                       │
│               Load Balancing · SSL · Rate Limiting           │
└──────┬──────────────────────┬────────────────────┬──────────┘
       │                      │                    │
┌──────▼──────┐     ┌────────▼───────┐    ┌───────▼─────────┐
│  FastAPI    │     │   AI Engine    │    │   Web3.py       │
│  Backend    │     │  PyTorch/Sklearn│   │  Blockchain     │
│             │     │                 │    │  Interface      │
└──────┬──────┘     └────────┬───────┘    └───────┬─────────┘
       │                     │                    │
┌──────▼──────────────────────▼────────────────────▼─────────┐
│                      DATA LAYER                             │
│         PostgreSQL · Redis · IPFS · File Storage            │
└─────────────────────────────────────────────────────────────┘
```

### AI Pipeline

```
Satellite Imagery ──┐
Weather Data ───────┤
Farm Data ──────────┤──► Feature Engineering ──► Carbon Estimator ──► Score
Soil Data ──────────┤                               │
Crop Data ──────────┘                               ▼
                                              Fraud Detector
                                                    │
                                                    ▼
                                            Sustainability
                                               Advisor
```

### Blockchain Workflow

```
Farmer ──► Register Farm ──► AI Analysis ──► Carbon Score
                                                   │
                                                   ▼
                                          Multi-Sig Verification
                                                   │
                                                   ▼
                                          Mint Certificate (ERC-721)
                                                   │
                                                   ▼
                                          List on Marketplace
                                                   │
                                                   ▼
                                          Buyer Purchases ──► Credits Retired
```

---

## Tech Stack

### Frontend (Zero Dependencies)
| Technology | Purpose |
|---|---|
| HTML5 | Semantic structure, accessibility |
| CSS3 | Grid, Flexbox, animations, responsive design |
| Vanilla JavaScript | All interactivity, API calls, charts |
| SVG | Graphics, icons, data visualization |

### Backend
| Technology | Purpose |
|---|---|
| Python 3.11+ | Core language |
| FastAPI | High-performance async API framework |
| SQLAlchemy 2.0 | ORM with repository pattern |
| PostgreSQL 15 | Primary database |
| Redis | Caching, session store |
| Gunicorn + Uvicorn | Production ASGI server |

### AI/ML
| Technology | Purpose |
|---|---|
| Scikit-learn | Carbon estimation model |
| NumPy/Pandas | Data processing |
| GeoPandas | Geospatial analysis |
| Rasterio | Satellite raster processing |
| OpenCV | Image analysis |

### Blockchain
| Technology | Purpose |
|---|---|
| Solidity 0.8.19 | Smart contracts |
| OpenZeppelin | audited contract base classes |
| Web3.py | Python blockchain interface |
| Hardhat | Contract development & testing |
| ERC-721 | Carbon certificate NFTs |
| ERC-20 | Carbon credit fungible tokens |

---

## Installation Guide

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Redis 7 (optional)
- Docker & Docker Compose (optional)

### Quick Start (Local)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/agrichain-carbon-ai.git
cd agrichain-carbon-ai

# 2. Run setup script
chmod +x scripts/setup/setup.sh
./scripts/setup/setup.sh

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# 5. In another terminal, start AI engine
cd ai-engine
uvicorn main:app --reload --port 8001

# 6. Open frontend
open frontend/index.html
```

### Docker Setup

```bash
# Build and run all services
docker-compose -f deployment/docker-compose.yml up --build

# Services:
#   Backend API:  http://localhost:8000
#   AI Engine:    http://localhost:8001
#   Frontend:     http://localhost:80
#   PostgreSQL:   localhost:5432
#   Redis:        localhost:6379
```

### Database Setup

```bash
# Create database
createdb agrichain

# Run migrations
psql -U agrichain -d agrichain -f database/migrations/001_initial.sql

# Seed test data
psql -U agrichain -d agrichain -f database/seeds/001_seed_data.sql
```

---

## Deployment Guide

### Production Deployment

```bash
# Set environment
export ENV=production

# Deploy with Docker
bash scripts/deployment/deploy.sh production

# Or manual deployment:
# 1. Build frontend assets
# 2. Configure nginx (see deployment/nginx/)
# 3. Start PostgreSQL and Redis
# 4. Run database migrations
# 5. Start backend with gunicorn
# 6. Start AI engine with uvicorn
# 7. Configure monitoring (see deployment/monitoring/)
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://agrichain:agrichain@localhost:5432/agrichain` |
| `SECRET_KEY` | JWT signing secret | Required |
| `POLYGON_RPC_URL` | Polygon RPC endpoint | Infura project required |
| `CELO_RPC_URL` | Celo RPC endpoint | Optional |
| `BASE_RPC_URL` | Base RPC endpoint | Optional |
| `SATELLITE_API_KEY` | NASA EarthData token | Optional |
| `OPENWEATHER_API_KEY` | OpenWeather API key | Optional |
| `SENTRY_DSN` | Error tracking | Optional |

---

## Security Design

### Authentication
- **JWT-based authentication** with access/refresh token pairs
- OAuth2 password flow for first-party clients
- Token expiration: 30 min (access), 7 days (refresh)
- Secure HTTP-only cookie option for production
- Rate limiting: 60 requests/minute per IP

### Authorization
- **Role-Based Access Control (RBAC)** with 4 roles:
  - `farmer` — farm management, carbon estimates
  - `buyer` — marketplace purchases, credit retirement
  - `auditor` — AI review, fraud investigation
  - `admin` — platform configuration, user management

### Data Security
- **CSRF protection** via origin and referer validation
- **SQL injection prevention** via SQLAlchemy parameterized queries
- Input sanitization middleware
- Secure file upload validation (type, size, content)
- Password hashing with bcrypt (12 rounds)

### Blockchain Security
- Smart contracts use OpenZeppelin audited base classes
- Multi-signature verification for carbon asset minting
- Access control modifiers on all administrative functions
- ReentrancyGuard on marketplace purchase function
- Pausable contracts for emergency stops

### API Security
- HTTPS enforced in production via nginx
- Security headers (CSP, HSTS, X-Frame-Options)
- CORS configured for specific origins
- Request size limits (10MB max upload)
- SlowAPI rate limiting

---

## AI Methodology

### Carbon Estimation Model

The carbon estimator uses a **random forest regression model** with 10 features:

1. **Area (hectares)** — farm size
2. **Latitude/Longitude** — climate zone adjustment
3. **Crop type** — IPCC emission factors per crop:
   - Coffee: 4.5 tCO₂e/ha/yr
   - Cocoa: 5.0 tCO₂e/ha/yr
   - Maize: 3.2 tCO₂e/ha/yr
   - Mixed/Diverse: 4.0 tCO₂e/ha/yr
4. **Soil type** — carbon retention capacity
5. **Irrigation** — water management efficiency
6. **Fertilizer** — organic vs synthetic impact
7. **Sustainability practices** — agroforestry, no-till, cover crops
8. **Historical rainfall** — biomass productivity
9. **Temperature** — respiration rates

Formula: `Carbon(t) = Base_Rate × Area × Soil_Factor × Irrigation_Factor × Fertilizer_Factor × Practice_Bonus × Climate_Factor`

### Satellite Analysis

The satellite intelligence module computes:

- **NDVI**: `(NIR - Red) / (NIR + Red)` — vegetation health indicator
- **EVI**: Enhanced Vegetation Index with atmospheric correction
- **Land Health Index**: Composite of NDVI, EVI, and soil moisture
- **Water Stress Index**: Function of NDVI, temperature, and precipitation
- **Biomass Estimation**: `NDVI × 20 × Area`

### Anomaly Detection

The fraud detection engine flags:

- GPS coordinates within 100m of existing farms
- Carbon rates exceeding 3× expected maximum
- Farm areas > 10,000 hectares
- Image files < 1KB or with modified metadata
- Inconsistent historical data patterns

---

## Smart Contract Design

### Contracts Architecture

```
CarbonMarketplace
    ├── CarbonCreditToken (ERC-20)
    ├── CarbonCertificateNFT (ERC-721)
    ├── FarmRegistry
    └── MultiSigVerification
```

### CarbonCreditToken (ERC-20)
- **Symbol**: ACCC
- **Name**: AgriChain Carbon Credit
- **Roles**: MINTER_ROLE, BURNER_ROLE, DEFAULT_ADMIN_ROLE
- **Functions**: mint, retire, pause, unpause

### CarbonCertificateNFT (ERC-721)
- **Features**: URI storage, enumerable, access control, pausable
- **Certificate fields**: farmId, carbonTonnes, methodology, verified, timestamp
- **Roles**: MINTER_ROLE, VERIFIER_ROLE

### FarmRegistry
- On-chain farm registration with metadata URI
- Farmer-to-farm mapping
- Verifier role for farm verification
- Auditor role for farm deactivation

### CarbonMarketplace
- Listing creation, price updates, cancellation
- Carbon purchase with ERC-20 payment
- Credit retirement tracking
- Purchase history per listing

### MultiSigVerification
- N-of-M verifier confirmation system
- Create request, confirm, auto-execute
- Configurable confirmation thresholds

---

## Marketplace Flow

### Buyer Lifecycle

```
1. Browse ──► Filter by ESG, price, tonnes, verification badge
2. Review ──► View farm details, carbon score, blockchain certificate
3. Purchase ──► Select tonnes, confirm price, execute transaction
4. Verify ──► View on-chain transaction hash
5. Retire ──► Retire credits for ESG reporting (irreversible)
```

### Carbon Purchase Process

```
Buyer selects listing
        │
        ▼
Check availability
        │
        ▼
Calculate total: tonnes × price_per_tonne
        │
        ▼
ERC-20 transfer approval
        │
        ▼
Transfer payment to seller
        │
        ▼
Update available tonnes
        │
        ▼
Record on-chain immutable ledger
        │
        ▼
Issue purchase certificate
```

### Asset Retirement Workflow
```
Owner selects purchased credits
        │
        ▼
Confirm retirement (irreversible)
        │
        ▼
Burn tokens (CarbonCreditToken.retire())
        │
        ▼
Record retirement on sustainability report
        │
        ▼
Generate ESG compliance certificate
```

---

## API Documentation

### Authentication
| Endpoint | Method | Description |
|---|---|---|
| `/api/auth/register` | POST | Create account |
| `/api/auth/login` | POST | Sign in |
| `/api/auth/refresh` | POST | Refresh tokens |
| `/api/auth/me` | GET | Current profile |

### Farms
| Endpoint | Method | Description |
|---|---|---|
| `/api/farms` | GET | List farms |
| `/api/farms` | POST | Register farm |
| `/api/farms/{id}` | GET | Farm details |
| `/api/farms/{id}` | PATCH | Update farm |
| `/api/farms/{id}/images` | POST | Upload image |

### Carbon
| Endpoint | Method | Description |
|---|---|---|
| `/api/carbon/estimate` | POST | Estimate carbon |
| `/api/carbon/scores/{id}` | GET | Get score |
| `/api/carbon/farms/{id}` | GET | Farm scores |
| `/api/carbon/my-scores` | GET | My scores |
| `/api/carbon/total` | GET | Total carbon |

### Marketplace
| Endpoint | Method | Description |
|---|---|---|
| `/api/marketplace/listings` | GET | List credits |
| `/api/marketplace/listings` | POST | Create listing |
| `/api/marketplace/purchase` | POST | Purchase |
| `/api/marketplace/retire/{id}` | POST | Retire |

Full API documentation available at `/docs` when running the backend.

---

## Directory Structure

```
agrichain-carbon-ai/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # Route handlers
│   │   ├── core/              # Config, database, security
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── repositories/      # Data access layer
│   │   └── middleware/        # Security middleware
│   └── tests/
├── frontend/                   # Static frontend
│   ├── css/
│   ├── js/
│   └── *.html                 # Pages
├── contracts/                  # Solidity smart contracts
│   ├── contracts/
│   ├── test/
│   └── scripts/
├── ai-engine/                  # AI/ML services
│   ├── models/
│   ├── services/
│   └── data/
├── database/
│   ├── migrations/
│   └── seeds/
├── deployment/                 # Docker, nginx, monitoring
│   ├── docker/
│   ├── nginx/
│   └── monitoring/
├── scripts/
│   ├── setup/
│   └── deployment/
├── docs/                       # Documentation
│   ├── api/
│   ├── schema/
│   ├── contracts/
│   ├── ai/
│   ├── security/
│   └── deployment/
└── tests/
    ├── backend/
    ├── contracts/
    └── ai/
```

---

## Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Contract tests
cd contracts
npx hardhat test

# AI engine tests
cd ai-engine
pytest tests/ -v

# All tests
pytest backend/tests/ ai-engine/tests/ -v
```

---

## Sustainability Impact

### Farmer Empowerment
- **Revenue**: Farmers earn $15-30 per tonne of CO₂ sequestered
- **Knowledge**: AI-driven sustainability recommendations
- **Recognition**: Verified on-chain credentials for sustainable practices
- **Market access**: Direct connection to global carbon buyers

### Environmental Benefits
- **Carbon sequestration**: Promotes practices that remove CO₂ from atmosphere
- **Biodiversity**: Agroforestry and cover cropping support ecosystems
- **Water conservation**: Efficient irrigation recommendations
- **Soil health**: Reduced tillage and organic fertilizer promotion

### ESG Transparency
- **Immutable records**: All transactions recorded on blockchain
- **Verified claims**: Multi-signature verification process
- **Public audit**: Certificate metadata accessible on-chain
- **Fraud prevention**: AI-powered anomaly detection

### Climate Innovation
- **AI + Blockchain**: Novel integration for environmental verification
- **Satellite verification**: Remote sensing complements on-ground data
- **Multi-chain**: Deployable on Polygon, Celo, and Base
- **Offline-first**: Designed for low-connectivity rural environments

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

## Team

Built for the **AgriChain Climate Innovation Hackathon** — a solution designed to be production-ready, investor-presentable, and globally competitive.

*"Turning sustainable agriculture into verifiable financial assets — for African farmers, by African engineers."*
