# AgriChain Carbon AI — API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require a Bearer token.

```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### POST /auth/register
Create a new user account.

```json
{
  "email": "farmer@example.com",
  "username": "farmer1",
  "password": "securepass123",
  "full_name": "Farmer Name",
  "role": "farmer",
  "country": "Kenya"
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "email": "farmer@example.com",
  "username": "farmer1",
  "full_name": "Farmer Name",
  "role": "farmer",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### POST /auth/login
Authenticate and receive tokens.

```json
{
  "username": "farmer1",
  "password": "securepass123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### POST /auth/refresh
Refresh expired access token.

```json
{
  "refresh_token": "eyJ..."
}
```

### GET /auth/me
Get current user profile.

---

## Farm Endpoints

### GET /farms
List farms (paginated).

Query params: `page=1&per_page=20&verified=true`

### POST /farms
Register a new farm.

```json
{
  "name": "My Farm",
  "country": "Kenya",
  "latitude": -1.2921,
  "longitude": 36.8219,
  "area_hectares": 5.0,
  "crop_types": "maize, beans",
  "irrigation_type": "drip",
  "soil_type": "loam",
  "sustainability_practices": "agroforestry, cover cropping"
}
```

---

## Carbon Endpoints

### POST /carbon/estimate
Generate carbon sequestration estimate.

```json
{
  "farm_id": "uuid",
  "force_recalculate": false
}
```

**Response**:
```json
{
  "id": "uuid",
  "carbon_offset_tonnes": 18.5,
  "sustainability_score": 82.3,
  "environmental_health_score": 78.6,
  "ai_confidence_level": 0.91,
  "ndvi_avg": 0.72,
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /carbon/scores/{score_id}
Get specific carbon score.

### GET /carbon/farms/{farm_id}
Get all scores for a farm.

### GET /carbon/my-scores
Get current user's scores.

---

## Marketplace Endpoints

### GET /marketplace/listings
Browse available carbon credits.

Query params: `min_tonnes=10&max_price=25&min_esg_score=70&verified_only=true&sort_by=created_at&sort_order=desc&page=1&per_page=20`

**Response**:
```json
{
  "listings": [
    {
      "id": "uuid",
      "farm_name": "Mary's Green Farm",
      "price_per_tonne": 18.50,
      "total_tonnes": 18.5,
      "available_tonnes": 18.5,
      "esg_score": 82.3,
      "verification_badge": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 3,
  "page": 1,
  "per_page": 20
}
```

### POST /marketplace/purchase
Purchase carbon credits.

```json
{
  "listing_id": "uuid",
  "tonnes": 10.0
}
```

### POST /marketplace/retire/{purchase_id}
Retire purchased credits (irreversible).

---

## Satellite Endpoints

### GET /satellite/analyze/{farm_id}
Analyze farm vegetation health.

**Response**:
```json
{
  "farm_id": "uuid",
  "ndvi_current": 0.72,
  "ndvi_change": 0.05,
  "land_health": 78.5,
  "vegetation_trend": "improving",
  "water_stress": 0.15,
  "analysis_date": "2024-01-01T00:00:00Z"
}
```

### GET /satellite/ndvi/{farm_id}
Get NDVI time-series data.

---

## Advisor Endpoints

### POST /advisor/chat
Send message to AI advisor.

```json
{
  "content": "How can I improve soil health?",
  "language": "en"
}
```

### GET /advisor/recommendations/{farm_id}
Get personalized recommendations.

---

## Blockchain Endpoints

### POST /blockchain/mint/{score_id}
Mint carbon credit as NFT.

Query param: `chain=polygon`

### GET /blockchain/verify/{tx_hash}
Verify transaction on-chain.

### GET /blockchain/certificate/{token_id}
Get certificate metadata.

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

HTTP Status Codes:
- 200: Success
- 400: Bad request
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 422: Validation error
- 429: Rate limit exceeded
- 500: Internal server error
