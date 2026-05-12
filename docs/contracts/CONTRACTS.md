# AgriChain Carbon AI — Smart Contract Documentation

## Overview

The blockchain layer provides transparent, immutable verification of carbon assets through five interconnected smart contracts deployed on EVM-compatible chains (Polygon, Celo, Base).

---

## Contract Architecture

```
CarbonMarketplace
    ├── Uses CarbonCertificateNFT (for certificate ownership)
    ├── Uses CarbonCreditToken (for payments)
    ├── References FarmRegistry (for farm verification)
    └── Uses MultiSigVerification (for approvals)
```

---

## 1. CarbonCreditToken (ERC-20)

**Address**: Deployed separately per chain

**Purpose**: Fungible carbon credit token used for marketplace transactions.

### Tokenomics
- **Name**: AgriChain Carbon Credit
- **Symbol**: ACCC
- **Decimals**: 18
- **Total Supply**: Mintable/Burnable (not fixed)

### Roles

| Role | Description |
|---|---|
| `DEFAULT_ADMIN_ROLE` | Contract administration, pause/unpause |
| `MINTER_ROLE` | Mint new tokens |
| `BURNER_ROLE` | Burn tokens |

### Key Functions

```solidity
// Mint carbon credits after verification
function mint(address to, uint256 amount, bytes32 farmId) external onlyRole(MINTER_ROLE);

// Retire (burn) credits — irreversible
function retire(uint256 amount, bytes32 purpose) external;

// Emergency controls
function pause() external onlyRole(DEFAULT_ADMIN_ROLE);
function unpause() external onlyRole(DEFAULT_ADMIN_ROLE);
```

### Events
```solidity
event CarbonCreditsMinted(address indexed to, uint256 amount, bytes32 indexed farmId);
event CarbonCreditsRetired(address indexed from, uint256 amount, bytes32 indexed purpose);
```

---

## 2. CarbonCertificateNFT (ERC-721)

**Address**: Deployed separately per chain

**Purpose**: Non-fungible certificate representing a verified carbon offset, with full metadata and verification history.

### Certificate Structure

```solidity
struct Certificate {
    uint256 tokenId;
    address owner;
    bytes32 farmId;
    uint256 carbonTonnes;
    string methodology;
    uint256 timestamp;
    bool verified;
    address verifier;
}
```

### Roles

| Role | Description |
|---|---|
| `DEFAULT_ADMIN_ROLE` | Contract administration |
| `MINTER_ROLE` | Mint new certificates |
| `VERIFIER_ROLE` | Verify certificates |

### Key Functions

```solidity
// Mint new carbon certificate
function mintCertificate(
    address to,
    bytes32 farmId,
    uint256 carbonTonnes,
    string memory methodology,
    string memory tokenURI
) external onlyRole(MINTER_ROLE) returns (uint256);

// Verify certificate authenticity
function verifyCertificate(uint256 tokenId) external onlyRole(VERIFIER_ROLE);

// Query certificate details
function getCertificate(uint256 tokenId) external view returns (Certificate memory);
function getFarmCertificates(bytes32 farmId) external view returns (uint256[] memory);
```

### Events
```solidity
event CertificateMinted(uint256 indexed tokenId, address indexed owner, bytes32 indexed farmId, uint256 carbonTonnes);
event CertificateVerified(uint256 indexed tokenId, address indexed verifier);
```

---

## 3. FarmRegistry

**Address**: Deployed separately per chain

**Purpose**: On-chain registry of verified farms with immutable metadata and history.

### Farm Structure

```solidity
struct Farm {
    bytes32 farmId;
    address farmer;
    string metadataURI;
    uint256 areaHectares;
    string cropType;
    string country;
    bool verified;
    bool active;
    uint256 registeredAt;
}
```

### Roles

| Role | Description |
|---|---|
| `DEFAULT_ADMIN_ROLE` | Contract administration |
| `VERIFIER_ROLE` | Verify farm authenticity |
| `AUDITOR_ROLE` | Deactivate fraudulent farms |

### Key Functions

```solidity
// Register farm on-chain
function registerFarm(
    bytes32 farmId,
    string memory metadataURI,
    uint256 areaHectares,
    string memory cropType,
    string memory country
) external returns (bytes32);

// Verify farm
function verifyFarm(bytes32 farmId) external onlyRole(VERIFIER_ROLE);

// Deactivate farm (fraud)
function deactivateFarm(bytes32 farmId) external onlyRole(AUDITOR_ROLE);
```

---

## 4. CarbonMarketplace

**Address**: Deployed separately per chain

**Purpose**: Decentralized marketplace for listing and purchasing carbon credits.

### Listing Structure

```solidity
struct Listing {
    uint256 listingId;
    uint256 tokenId;
    address seller;
    uint256 pricePerTonne;
    uint256 totalTonnes;
    uint256 availableTonnes;
    bool active;
    uint256 createdAt;
}
```

### Key Functions

```solidity
// List carbon credits for sale
function createListing(
    uint256 tokenId,
    uint256 pricePerTonne,
    uint256 totalTonnes
) external returns (uint256);

// Purchase carbon credits
function purchaseCarbon(uint256 listingId, uint256 tonnes) external;

// Retire purchased credits
function retireCarbon(uint256 purchaseId, bytes32 purpose) external;
```

### Events
```solidity
event ListingCreated(uint256 indexed listingId, uint256 indexed tokenId, address indexed seller, uint256 pricePerTonne, uint256 totalTonnes);
event CarbonPurchased(uint256 indexed purchaseId, uint256 indexed listingId, address indexed buyer, uint256 tonnes, uint256 totalPrice);
event CarbonRetired(uint256 indexed purchaseId, address indexed retirer, bytes32 purpose);
```

---

## 5. MultiSigVerification

**Address**: Deployed separately per chain

**Purpose**: Multi-signature verification for critical operations requiring multiple auditors.

### Verification Request

```solidity
struct VerificationRequest {
    bytes32 requestId;
    bytes32 targetHash;
    uint256 requiredConfirmations;
    uint256 confirmationsCount;
    mapping(address => bool) confirmedBy;
    bool executed;
    uint256 createdAt;
}
```

### Key Functions

```solidity
// Create verification request
function createRequest(bytes32 targetHash, uint256 requiredConfirmations) external returns (bytes32);

// Confirm verification
function confirmRequest(bytes32 requestId) external onlyRole(VERIFIER_ROLE);

// Check if confirmed
function isConfirmed(bytes32 requestId, address verifier) external view returns (bool);
```

---

## Deployment

```bash
# Local deployment
npx hardhat run scripts/deploy.js --network hardhat

# Polygon Mumbai Testnet
npx hardhat run scripts/deploy.js --network polygon

# Celo Alfajores Testnet
npx hardhat run scripts/deploy.js --network celo

# Base Goerli Testnet
npx hardhat run scripts/deploy.js --network base
```

### Post-Deployment

1. Grant `MINTER_ROLE` on CarbonCreditToken to CarbonCertificateNFT
2. Grant `VERIFIER_ROLE` on CarbonCertificateNFT to auditor addresses
3. Set marketplace fee recipient
4. Verify contracts on block explorer

---

## Security Considerations

1. **Access Control**: All administrative functions protected by OpenZeppelin's `AccessControl`
2. **Reentrancy**: Marketplace purchases protected by `ReentrancyGuard`
3. **Pausability**: Emergency stop mechanism for all contracts
4. **Upgradeability**: Contracts designed for proxy pattern with OpenZeppelin Upgrades
5. **Events**: All state changes emit events for off-chain tracking
6. **Integer Safety**: Solidity 0.8.x has built-in overflow protection

---

## Testing

```bash
# Run all contract tests
npx hardhat test

# Run with gas reporting
REPORT_GAS=true npx hardhat test

# Run coverage
npx hardhat coverage
```

Test suite covers:
- Token minting and burning
- Certificate lifecycle (mint, verify, transfer)
- Farm registration and verification
- Marketplace listing, purchase, and retirement
- Multi-sig request and confirmation
- Access control restrictions
- Reentrancy protection
- Pause/unpause functionality
