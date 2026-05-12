// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract FarmRegistry is AccessControl, Pausable {
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");
    bytes32 public constant AUDITOR_ROLE = keccak256("AUDITOR_ROLE");

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

    mapping(bytes32 => Farm) public farms;
    mapping(address => bytes32[]) public farmerFarms;
    bytes32[] public allFarmIds;

    event FarmRegistered(bytes32 indexed farmId, address indexed farmer, uint256 areaHectares);
    event FarmVerified(bytes32 indexed farmId, address indexed verifier);
    event FarmUpdated(bytes32 indexed farmId, string metadataURI);
    event FarmDeactivated(bytes32 indexed farmId);

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
        _grantRole(AUDITOR_ROLE, msg.sender);
    }

    function registerFarm(
        bytes32 farmId,
        string memory metadataURI,
        uint256 areaHectares,
        string memory cropType,
        string memory country
    ) external whenNotPaused returns (bytes32) {
        require(farms[farmId].registeredAt == 0, "Farm already registered");
        require(areaHectares > 0, "Area must be positive");

        farms[farmId] = Farm({
            farmId: farmId,
            farmer: msg.sender,
            metadataURI: metadataURI,
            areaHectares: areaHectares,
            cropType: cropType,
            country: country,
            verified: false,
            active: true,
            registeredAt: block.timestamp
        });

        farmerFarms[msg.sender].push(farmId);
        allFarmIds.push(farmId);

        emit FarmRegistered(farmId, msg.sender, areaHectares);
        return farmId;
    }

    function verifyFarm(bytes32 farmId) external onlyRole(VERIFIER_ROLE) {
        require(farms[farmId].registeredAt != 0, "Farm not found");
        require(!farms[farmId].verified, "Already verified");

        farms[farmId].verified = true;
        emit FarmVerified(farmId, msg.sender);
    }

    function updateFarmMetadata(bytes32 farmId, string memory metadataURI) external {
        require(farms[farmId].farmer == msg.sender, "Not farm owner");
        require(farms[farmId].active, "Farm is deactivated");

        farms[farmId].metadataURI = metadataURI;
        emit FarmUpdated(farmId, metadataURI);
    }

    function deactivateFarm(bytes32 farmId) external onlyRole(AUDITOR_ROLE) {
        require(farms[farmId].registeredAt != 0, "Farm not found");
        farms[farmId].active = false;
        emit FarmDeactivated(farmId);
    }

    function getFarmerFarms(address farmer) external view returns (bytes32[] memory) {
        return farmerFarms[farmer];
    }

    function getFarm(bytes32 farmId) external view returns (Farm memory) {
        require(farms[farmId].registeredAt != 0, "Farm not found");
        return farms[farmId];
    }

    function getTotalFarms() external view returns (uint256) {
        return allFarmIds.length;
    }

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
