# AgriChain Carbon AI — Security Audit Checklist

## Authentication

- [ ] JWT tokens use strong secret key (>256 bits)
- [ ] Access tokens expire within 30 minutes
- [ ] Refresh tokens expire within 7 days
- [ ] Password hashing uses bcrypt with cost factor 12
- [ ] Rate limiting on login endpoint (5 attempts/minute)
- [ ] Account lockout after 10 failed attempts
- [ ] No password in API responses
- [ ] Token refresh invalidates old tokens

## Authorization

- [ ] RBAC implemented for all 4 roles
- [ ] Farmers can only access own farms
- [ ] Auditors cannot create or modify farm data
- [ ] Admin actions logged to audit trail
- [ ] Cross-tenant data isolation verified
- [ ] API endpoint authorization tested

## API Security

- [ ] CORS configured for specific origins (not wildcard in production)
- [ ] All endpoints rate limited (60 req/min default)
- [ ] Request body size limited (10MB max)
- [ ] SQL injection protection via ORM parameterized queries
- [ ] Input sanitization for all string inputs
- [ ] Content-Type validation enforced
- [ ] API versioning for backward compatibility

## Data Security

- [ ] Database credentials not in code (env vars)
- [ ] Sensitive data encrypted at rest
- [ ] File upload validation (type, size, content)
- [ ] Realistic test data contains no PII
- [ ] Audit logs immutable (append-only)
- [ ] Database backups encrypted
- [ ] Connection pooling with SSL

## Smart Contract Security

- [ ] OpenZeppelin audited base contracts used
- [ ] ReentrancyGuard on marketplace purchase
- [ ] AccessControl on all admin functions
- [ ] Pausable for emergency stop
- [ ] Integer overflow protection (Solidity 0.8.x)
- [ ] No selfdestruct or delegatecall
- [ ] Events emitted for all state changes
- [ ] Upgradeable proxy pattern for future fixes

## Infrastructure Security

- [ ] HTTPS enforced (HSTS header set)
- [ ] Docker containers run as non-root
- [ ] Secrets not in Docker images
- [ ] Network segmentation (internal/external)
- [ ] WAF rules configured for common attacks
- [ ] Security headers set (CSP, X-Frame-Options, etc.)
- [ ] Monitoring and alerting configured
- [ ] Regular dependency scanning

## Penetration Testing Checklist

- [ ] SQL injection attempts on all endpoints
- [ ] XSS attempts on all input fields
- [ ] CSRF token validation tested
- [ ] JWT tampering tested
- [ ] Role escalation attempts
- [ ] IDOR (Insecure Direct Object Reference) tested
- [ ] Rate limiting bypass attempted
- [ ] File upload vulnerability tested
- [ ] Block reentrancy on marketplace
- [ ] Smart contract edge cases tested
