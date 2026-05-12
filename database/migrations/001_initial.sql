-- AgriChain Carbon AI - Initial Database Schema
-- PostgreSQL Migration

BEGIN;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'farmer',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    phone VARCHAR(50),
    country VARCHAR(100),
    wallet_address VARCHAR(255),
    profile_image VARCHAR(500),
    preferred_language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_country ON users(country);

-- Farms table
CREATE TABLE farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    country VARCHAR(100) NOT NULL,
    region VARCHAR(200),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    area_hectares DOUBLE PRECISION NOT NULL,
    crop_types TEXT,
    irrigation_type VARCHAR(100),
    fertilizer_usage VARCHAR(200),
    soil_type VARCHAR(100),
    sustainability_practices TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_date TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_farms_farmer_id ON farms(farmer_id);
CREATE INDEX idx_farms_country ON farms(country);
CREATE INDEX idx_farms_status ON farms(status);
CREATE INDEX idx_farms_verified ON farms(is_verified);
CREATE INDEX idx_farms_location ON farms(latitude, longitude);

-- Farm images
CREATE TABLE farm_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    image_type VARCHAR(50),
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_farm_images_farm_id ON farm_images(farm_id);

-- Carbon scores
CREATE TABLE carbon_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    farmer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    carbon_offset_tonnes DOUBLE PRECISION NOT NULL,
    sustainability_score DOUBLE PRECISION,
    environmental_health_score DOUBLE PRECISION,
    ai_confidence_level DOUBLE PRECISION,
    ndvi_avg DOUBLE PRECISION,
    biomass_estimate DOUBLE PRECISION,
    soil_carbon_estimate DOUBLE PRECISION,
    methodology_version VARCHAR(50),
    input_parameters TEXT,
    raw_ai_output TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_carbon_scores_farm_id ON carbon_scores(farm_id);
CREATE INDEX idx_carbon_scores_farmer_id ON carbon_scores(farmer_id);
CREATE INDEX idx_carbon_scores_status ON carbon_scores(status);
CREATE INDEX idx_carbon_scores_created ON carbon_scores(created_at DESC);

-- Satellite data
CREATE TABLE satellite_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    source VARCHAR(100),
    image_url VARCHAR(500),
    ndvi_value DOUBLE PRECISION,
    evi_value DOUBLE PRECISION,
    land_health_score DOUBLE PRECISION,
    water_stress_index DOUBLE PRECISION,
    vegetation_fraction DOUBLE PRECISION,
    acquisition_date TIMESTAMPTZ,
    processing_date TIMESTAMPTZ DEFAULT NOW(),
    raw_metadata TEXT
);

CREATE INDEX idx_satellite_farm_id ON satellite_data(farm_id);
CREATE INDEX idx_satellite_date ON satellite_data(acquisition_date DESC);

-- Sustainability reports
CREATE TABLE sustainability_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    report_type VARCHAR(100),
    report_data TEXT,
    recommendations TEXT,
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reports_farm_id ON sustainability_reports(farm_id);

-- Blockchain transactions
CREATE TABLE blockchain_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_hash VARCHAR(255) UNIQUE,
    contract_address VARCHAR(255),
    function_name VARCHAR(100),
    args TEXT,
    block_number INTEGER,
    status VARCHAR(50),
    gas_used INTEGER,
    chain VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tx_hash ON blockchain_transactions(transaction_hash);
CREATE INDEX idx_tx_chain ON blockchain_transactions(chain);

-- Carbon assets (on-chain certificates)
CREATE TABLE carbon_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    token_id INTEGER UNIQUE,
    farm_id UUID NOT NULL REFERENCES farms(id),
    carbon_score_id UUID NOT NULL REFERENCES carbon_scores(id),
    owner_address VARCHAR(255),
    certificate_uri VARCHAR(500),
    carbon_tonnes DOUBLE PRECISION,
    chain VARCHAR(50),
    contract_address VARCHAR(255),
    mint_tx_hash VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_assets_token ON carbon_assets(token_id);
CREATE INDEX idx_assets_status ON carbon_assets(status);

-- Marketplace listings
CREATE TABLE marketplace_listings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id),
    carbon_asset_id UUID NOT NULL REFERENCES carbon_assets(id),
    seller_id UUID NOT NULL REFERENCES users(id),
    price_per_tonne DOUBLE PRECISION NOT NULL,
    total_tonnes DOUBLE PRECISION NOT NULL,
    available_tonnes DOUBLE PRECISION NOT NULL,
    currency VARCHAR(10) DEFAULT 'USDC',
    status VARCHAR(50) DEFAULT 'active',
    esg_score DOUBLE PRECISION,
    verification_badge BOOLEAN DEFAULT FALSE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_listings_status ON marketplace_listings(status);
CREATE INDEX idx_listings_seller ON marketplace_listings(seller_id);
CREATE INDEX idx_listings_price ON marketplace_listings(price_per_tonne);
CREATE INDEX idx_listings_esg ON marketplace_listings(esg_score DESC);

-- Carbon purchases
CREATE TABLE carbon_purchases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    listing_id UUID NOT NULL REFERENCES marketplace_listings(id),
    buyer_id UUID NOT NULL REFERENCES users(id),
    tonnes_purchased DOUBLE PRECISION NOT NULL,
    total_price DOUBLE PRECISION NOT NULL,
    currency VARCHAR(10),
    transaction_hash VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    is_retired BOOLEAN DEFAULT FALSE,
    retired_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_purchases_buyer ON carbon_purchases(buyer_id);
CREATE INDEX idx_purchases_listing ON carbon_purchases(listing_id);
CREATE INDEX idx_purchases_retired ON carbon_purchases(is_retired);

-- Fraud alerts
CREATE TABLE fraud_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id),
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    fraud_score DOUBLE PRECISION NOT NULL,
    description TEXT,
    evidence TEXT,
    status VARCHAR(50) DEFAULT 'open',
    assigned_auditor_id UUID REFERENCES users(id),
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_farm ON fraud_alerts(farm_id);
CREATE INDEX idx_alerts_status ON fraud_alerts(status);
CREATE INDEX idx_alerts_severity ON fraud_alerts(severity);

-- Audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100),
    entity_id UUID,
    action VARCHAR(100),
    performed_by UUID REFERENCES users(id),
    details TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_performed ON audit_logs(performed_by);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);

-- Advisor messages
CREATE TABLE advisor_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    role VARCHAR(20),
    content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    message_type VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_advisor_user ON advisor_messages(user_id);
CREATE INDEX idx_advisor_created ON advisor_messages(created_at);

-- Advisor recommendations
CREATE TABLE advisor_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id),
    recommendation_type VARCHAR(100),
    title VARCHAR(255),
    description TEXT,
    priority VARCHAR(50),
    category VARCHAR(100),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_recs_farm ON advisor_recommendations(farm_id);
CREATE INDEX idx_recs_priority ON advisor_recommendations(priority);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_farms_updated_at
    BEFORE UPDATE ON farms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_listings_updated_at
    BEFORE UPDATE ON marketplace_listings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;
