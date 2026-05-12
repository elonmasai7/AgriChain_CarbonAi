-- AgriChain Carbon AI - Seed Data
-- Provides realistic test data for demo purposes

BEGIN;

-- Seed admin user (password: admin123)
INSERT INTO users (id, email, username, hashed_password, full_name, role, is_active, country)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'admin@agrichain.com',
    'admin',
    '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5GzGq5GzGq5GzGq5G', -- admin123
    'System Administrator',
    'admin',
    TRUE,
    'Kenya'
) ON CONFLICT (email) DO NOTHING;

-- Seed farmers
INSERT INTO users (id, email, username, hashed_password, full_name, role, is_active, country)
VALUES
    ('b0000000-0000-0000-0000-000000000001', 'mary@example.com', 'mary_kamau', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5GzGq5GzGq5GzGq5G', 'Mary Kamau', 'farmer', TRUE, 'Kenya'),
    ('b0000000-0000-0000-0000-000000000002', 'john@example.com', 'john_otieno', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5GzGq5GzGq5GzGq5G', 'John Otieno', 'farmer', TRUE, 'Kenya'),
    ('b0000000-0000-0000-0000-000000000003', 'grace@example.com', 'grace_mukas', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5GzGq5GzGq5GzGq5G', 'Grace Mukashema', 'farmer', TRUE, 'Rwanda')
ON CONFLICT (email) DO NOTHING;

-- Seed buyers
INSERT INTO users (id, email, username, hashed_password, full_name, role, is_active, country)
VALUES
    ('c0000000-0000-0000-0000-000000000001', 'buyer@safaricom.co.ke', 'safaricom', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5GzGq5GzGq5GzGq5G', 'Safaricom PLC', 'buyer', TRUE, 'Kenya'),
    ('c0000000-0000-0000-0000-000000000002', 'esg@kcb.com', 'kcb_group', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5GzGq5GzGq5GzGq5G', 'KCB Group', 'buyer', TRUE, 'Kenya')
ON CONFLICT (email) DO NOTHING;

-- Seed auditor
INSERT INTO users (id, email, username, hashed_password, full_name, role, is_active, country)
VALUES (
    'd0000000-0000-0000-0000-000000000001',
    'auditor@verra.org',
    'verra_auditor',
    '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5GzGq5GzGq5GzGq5G',
    'Verra Certification Auditor',
    'auditor',
    TRUE,
    'Kenya'
) ON CONFLICT (email) DO NOTHING;

-- Seed farms
INSERT INTO farms (id, farmer_id, name, country, latitude, longitude, area_hectares, crop_types, irrigation_type, fertilizer_usage, soil_type, sustainability_practices, is_verified, status)
VALUES
    ('f1000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', 'Mary''s Green Farm', 'Kenya', -1.2921, 36.8219, 5.0, 'maize, beans, kale', 'drip', 'organic', 'loam', 'agroforestry, cover cropping, crop rotation', TRUE, 'verified'),
    ('f1000000-0000-0000-0000-000000000002', 'b0000000-0000-0000-0000-000000000002', 'Otieno Organic Acres', 'Kenya', -0.2867, 36.0723, 8.2, 'coffee, bananas, maize', 'sprinkler', 'compost', 'clay', 'mulching, intercropping, no-till farming', TRUE, 'verified'),
    ('f1000000-0000-0000-0000-000000000003', 'b0000000-0000-0000-0000-000000000003', 'Mukashema Terraces', 'Rwanda', -1.9441, 30.0619, 3.5, 'coffee, tea, potatoes', 'rainfed', 'organic', 'silt', 'terracing, agroforestry, compost', TRUE, 'verified');

-- Seed carbon scores
INSERT INTO carbon_scores (id, farm_id, farmer_id, carbon_offset_tonnes, sustainability_score, environmental_health_score, ai_confidence_level, ndvi_avg, biomass_estimate, soil_carbon_estimate, status)
VALUES
    ('s1000000-0000-0000-0000-000000000001', 'f1000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', 18.5, 82.3, 78.6, 0.91, 0.72, 46.2, 11.1, 'approved'),
    ('s1000000-0000-0000-0000-000000000002', 'f1000000-0000-0000-0000-000000000002', 'b0000000-0000-0000-0000-000000000002', 32.8, 78.5, 74.2, 0.88, 0.68, 82.0, 19.7, 'approved'),
    ('s1000000-0000-0000-0000-000000000003', 'f1000000-0000-0000-0000-000000000003', 'b0000000-0000-0000-0000-000000000003', 15.2, 88.1, 85.3, 0.93, 0.75, 38.0, 9.1, 'approved');

-- Seed satellite data
INSERT INTO satellite_data (farm_id, source, ndvi_value, evi_value, land_health_score, water_stress_index, vegetation_fraction, acquisition_date)
VALUES
    ('f1000000-0000-0000-0000-000000000001', 'sentinel-2', 0.72, 0.85, 78.5, 0.15, 0.68, NOW() - INTERVAL '7 days'),
    ('f1000000-0000-0000-0000-000000000001', 'sentinel-2', 0.68, 0.80, 75.2, 0.18, 0.65, NOW() - INTERVAL '37 days'),
    ('f1000000-0000-0000-0000-000000000001', 'sentinel-2', 0.65, 0.78, 72.8, 0.22, 0.62, NOW() - INTERVAL '67 days'),
    ('f1000000-0000-0000-0000-000000000002', 'sentinel-2', 0.68, 0.82, 74.6, 0.20, 0.64, NOW() - INTERVAL '5 days'),
    ('f1000000-0000-0000-0000-000000000003', 'sentinel-2', 0.75, 0.88, 85.3, 0.08, 0.72, NOW() - INTERVAL '3 days');

-- Seed carbon assets
INSERT INTO carbon_assets (token_id, farm_id, carbon_score_id, owner_address, carbon_tonnes, chain, status)
VALUES
    (1, 'f1000000-0000-0000-0000-000000000001', 's1000000-0000-0000-0000-000000000001', '0x1234567890abcdef1234567890abcdef12345678', 18.5, 'polygon', 'active'),
    (2, 'f1000000-0000-0000-0000-000000000002', 's1000000-0000-0000-0000-000000000002', '0x2345678901abcdef2345678901abcdef23456789', 32.8, 'polygon', 'active'),
    (3, 'f1000000-0000-0000-0000-000000000003', 's1000000-0000-0000-0000-000000000003', '0x3456789012abcdef3456789012abcdef34567890', 15.2, 'polygon', 'active');

-- Seed marketplace listings
INSERT INTO marketplace_listings (farm_id, carbon_asset_id, seller_id, price_per_tonne, total_tonnes, available_tonnes, currency, esg_score, verification_badge, status)
VALUES
    ('f1000000-0000-0000-0000-000000000001', (SELECT id FROM carbon_assets WHERE token_id = 1), 'b0000000-0000-0000-0000-000000000001', 18.50, 18.5, 18.5, 'USDC', 82.3, TRUE, 'active'),
    ('f1000000-0000-0000-0000-000000000002', (SELECT id FROM carbon_assets WHERE token_id = 2), 'b0000000-0000-0000-0000-000000000002', 22.00, 32.8, 32.8, 'USDC', 78.5, TRUE, 'active'),
    ('f1000000-0000-0000-0000-000000000003', (SELECT id FROM carbon_assets WHERE token_id = 3), 'b0000000-0000-0000-0000-000000000003', 15.00, 15.2, 15.2, 'USDC', 88.1, TRUE, 'active');

COMMIT;
