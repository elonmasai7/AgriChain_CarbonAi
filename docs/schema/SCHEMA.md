# AgriChain Carbon AI — Database Schema

## Entity Relationship Overview

```
users 1───* farms
users 1───* carbon_scores
users 1───* marketplace_listings (as seller)
users 1───* carbon_purchases (as buyer)
users 1───* fraud_alerts (as assigned_auditor)
users 1───* advisor_messages

farms 1───* farm_images
farms 1───* carbon_scores
farms 1───* satellite_data
farms 1───* sustainability_reports
farms 1───* carbon_assets
farms 1───* marketplace_listings
farms 1───* fraud_alerts
farms 1───* advisor_recommendations

carbon_scores 1───* carbon_assets

carbon_assets 1───* marketplace_listings

marketplace_listings 1───* carbon_purchases
```

## Tables

### Users
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK, default uuid_generate_v4() | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| username | VARCHAR(100) | UNIQUE, NOT NULL | Display name |
| hashed_password | VARCHAR(255) | NOT NULL | bcrypt hash |
| full_name | VARCHAR(255) | NOT NULL | Real name |
| role | VARCHAR(50) | NOT NULL, DEFAULT 'farmer' | farmer/buyer/auditor/admin |
| is_active | BOOLEAN | DEFAULT TRUE | Account active |
| email_verified | BOOLEAN | DEFAULT FALSE | Email confirmed |
| phone | VARCHAR(50) | NULLABLE | Contact number |
| country | VARCHAR(100) | NULLABLE | Country of residence |
| wallet_address | VARCHAR(255) | NULLABLE | Blockchain wallet |
| profile_image | VARCHAR(500) | NULLABLE | Avatar URL |
| preferred_language | VARCHAR(10) | DEFAULT 'en' | en/sw/fr |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Record created |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Record updated |

**Indexes**: email, username, role, country

### Farms
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Unique identifier |
| farmer_id | UUID | FK → users.id, NOT NULL | Farm owner |
| name | VARCHAR(255) | NOT NULL | Farm name |
| description | TEXT | NULLABLE | Farm description |
| country | VARCHAR(100) | NOT NULL | Country |
| region | VARCHAR(200) | NULLABLE | Administrative region |
| latitude | DOUBLE PRECISION | NOT NULL | GPS latitude |
| longitude | DOUBLE PRECISION | NOT NULL | GPS longitude |
| area_hectares | DOUBLE PRECISION | NOT NULL | Size in hectares |
| crop_types | TEXT | NULLABLE | Crops grown |
| irrigation_type | VARCHAR(100) | NULLABLE | Irrigation method |
| fertilizer_usage | VARCHAR(200) | NULLABLE | Fertilizer type |
| soil_type | VARCHAR(100) | NULLABLE | Soil classification |
| sustainability_practices | TEXT | NULLABLE | Sustainable practices |
| is_verified | BOOLEAN | DEFAULT FALSE | Audit status |
| verification_date | TIMESTAMPTZ | NULLABLE | When verified |
| status | VARCHAR(50) | DEFAULT 'pending' | pending/verified/rejected |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes**: farmer_id, country, status, is_verified, (latitude, longitude)

### Carbon Scores
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | |
| farm_id | UUID | FK → farms.id | |
| farmer_id | UUID | FK → users.id | |
| carbon_offset_tonnes | DOUBLE PRECISION | NOT NULL | Estimated CO2e |
| sustainability_score | DOUBLE PRECISION | NULLABLE | 0-100 scale |
| environmental_health_score | DOUBLE PRECISION | NULLABLE | 0-100 scale |
| ai_confidence_level | DOUBLE PRECISION | NULLABLE | 0-1 confidence |
| ndvi_avg | DOUBLE PRECISION | NULLABLE | Mean NDVI |
| biomass_estimate | DOUBLE PRECISION | NULLABLE | Total biomass |
| soil_carbon_estimate | DOUBLE PRECISION | NULLABLE | Soil carbon |
| methodology_version | VARCHAR(50) | NULLABLE | Algorithm version |
| input_parameters | TEXT | NULLABLE | JSON input data |
| raw_ai_output | TEXT | NULLABLE | Full AI response |
| status | VARCHAR(50) | DEFAULT 'pending' | pending/approved/rejected |
| reviewed_by | UUID | FK → users.id | Auditor |
| reviewed_at | TIMESTAMPTZ | NULLABLE | Review timestamp |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes**: farm_id, farmer_id, status, created_at DESC

### Satellite Data
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | |
| farm_id | UUID | FK → farms.id | |
| source | VARCHAR(100) | NULLABLE | sentinel-2/landsat/modis |
| image_url | VARCHAR(500) | NULLABLE | Raster file URL |
| ndvi_value | DOUBLE PRECISION | NULLABLE | NDVI index |
| evi_value | DOUBLE PRECISION | NULLABLE | EVI index |
| land_health_score | DOUBLE PRECISION | NULLABLE | Composite score |
| water_stress_index | DOUBLE PRECISION | NULLABLE | Water stress |
| vegetation_fraction | DOUBLE PRECISION | NULLABLE | Cover fraction |
| acquisition_date | TIMESTAMPTZ | NULLABLE | Image capture date |
| processing_date | TIMESTAMPTZ | DEFAULT NOW() | |
| raw_metadata | TEXT | NULLABLE | Sensor metadata |

### Marketplace Listings
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | |
| farm_id | UUID | FK → farms.id | |
| carbon_asset_id | UUID | FK → carbon_assets.id | |
| seller_id | UUID | FK → users.id | |
| price_per_tonne | DOUBLE PRECISION | NOT NULL | USD per tCO2e |
| total_tonnes | DOUBLE PRECISION | NOT NULL | Total listed |
| available_tonnes | DOUBLE PRECISION | NOT NULL | Remaining |
| currency | VARCHAR(10) | DEFAULT 'USDC' | Payment token |
| status | VARCHAR(50) | DEFAULT 'active' | active/sold_out/cancelled |
| esg_score | DOUBLE PRECISION | NULLABLE | ESG rating |
| verification_badge | BOOLEAN | DEFAULT FALSE | Farm verified |
| description | TEXT | NULLABLE | Additional info |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

### Carbon Purchases
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | |
| listing_id | UUID | FK → marketplace_listings.id | |
| buyer_id | UUID | FK → users.id | |
| tonnes_purchased | DOUBLE PRECISION | NOT NULL | Amount bought |
| total_price | DOUBLE PRECISION | NOT NULL | Total paid |
| currency | VARCHAR(10) | NULLABLE | Payment token |
| transaction_hash | VARCHAR(255) | NULLABLE | Blockchain TX |
| status | VARCHAR(50) | DEFAULT 'pending' | pending/completed/failed |
| is_retired | BOOLEAN | DEFAULT FALSE | Credits retired |
| retired_at | TIMESTAMPTZ | NULLABLE | Retirement date |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

### Fraud Alerts
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | |
| farm_id | UUID | FK → farms.id | |
| alert_type | VARCHAR(100) | NOT NULL | Type of fraud |
| severity | VARCHAR(50) | NOT NULL | low/medium/high/critical |
| fraud_score | DOUBLE PRECISION | NOT NULL | 0-1 risk score |
| description | TEXT | NULLABLE | Alert details |
| evidence | TEXT | NULLABLE | Supporting data |
| status | VARCHAR(50) | DEFAULT 'open' | open/investigating/resolved |
| assigned_auditor_id | UUID | FK → users.id | Investigator |
| resolved_at | TIMESTAMPTZ | NULLABLE | Resolution time |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

### Audit Logs
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | |
| entity_type | VARCHAR(100) | NULLABLE | Affected table |
| entity_id | UUID | NULLABLE | Affected record |
| action | VARCHAR(100) | NULLABLE | Action performed |
| performed_by | UUID | FK → users.id | Who did it |
| details | TEXT | NULLABLE | Full details |
| ip_address | VARCHAR(50) | NULLABLE | Request origin |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

## Partitioning Strategy

For production at scale, partition large tables:

```sql
-- Partition carbon_scores by month
CREATE TABLE carbon_scores (
    LIKE carbon_scores_template
) PARTITION BY RANGE (created_at);

CREATE TABLE carbon_scores_2024_q1 PARTITION OF carbon_scores
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- Partition audit_logs by month (immutable, high volume)
CREATE TABLE audit_logs_2024_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## Migration Strategy

1. New migrations in `database/migrations/` with sequential numbering
2. Each migration is idempotent (uses `IF NOT EXISTS`)
3. Rollback scripts provided in `database/migrations/rollback/`
4. Migrations run automatically on container startup
5. Manual: `psql -U agrichain -d agrichain -f database/migrations/001_initial.sql`
