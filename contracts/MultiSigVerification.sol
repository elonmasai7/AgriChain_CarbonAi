// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract MultiSigVerification is AccessControl {
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");

    struct VerificationRequest {
        bytes32 requestId;
        bytes32 targetHash;
        uint256 requiredConfirmations;
        uint256 confirmationsCount;
        mapping(address => bool) confirmedBy;
        bool executed;
        uint256 createdAt;
    }

    struct RequestView {
        bytes32 requestId;
        bytes32 targetHash;
        uint256 requiredConfirmations;
        uint256 confirmationsCount;
        bool executed;
        uint256 createdAt;
    }

    uint256 private _requestCount;
    mapping(bytes32 => VerificationRequest) private _requests;
    bytes32[] private _requestIds;

    event VerificationRequestCreated(bytes32 indexed requestId, bytes32 indexed targetHash, uint256 requiredConfirmations);
    event ConfirmationAdded(bytes32 indexed requestId, address indexed verifier);
    event VerificationExecuted(bytes32 indexed requestId, bytes32 indexed targetHash);

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
    }

    function createRequest(bytes32 targetHash, uint256 requiredConfirmations) external returns (bytes32) {
        require(requiredConfirmations > 0, "Must require at least 1 confirmation");
        require(requiredConfirmations <= getRoleMemberCount(VERIFIER_ROLE), "Not enough verifiers");

        _requestCount++;
        bytes32 requestId = keccak256(abi.encodePacked(targetHash, _requestCount, block.timestamp));

        VerificationRequest storage request = _requests[requestId];
        request.requestId = requestId;
        request.targetHash = targetHash;
        request.requiredConfirmations = requiredConfirmations;
        request.confirmationsCount = 0;
        request.executed = false;
        request.createdAt = block.timestamp;

        _requestIds.push(requestId);

        emit VerificationRequestCreated(requestId, targetHash, requiredConfirmations);
        return requestId;
    }

    function confirmRequest(bytes32 requestId) external onlyRole(VERIFIER_ROLE) {
        VerificationRequest storage request = _requests[requestId];
        require(!request.executed, "Already executed");
        require(request.createdAt != 0, "Request does not exist");
        require(!request.confirmedBy[msg.sender], "Already confirmed");

        request.confirmedBy[msg.sender] = true;
        request.confirmationsCount++;

        emit ConfirmationAdded(requestId, msg.sender);

        if (request.confirmationsCount >= request.requiredConfirmations) {
            request.executed = true;
            emit VerificationExecuted(requestId, request.targetHash);
        }
    }

    function isConfirmed(bytes32 requestId, address verifier) external view returns (bool) {
        return _requests[requestId].confirmedBy[verifier];
    }

    function getRequest(bytes32 requestId) external view returns (RequestView memory) {
        VerificationRequest storage request = _requests[requestId];
        return RequestView({
            requestId: request.requestId,
            targetHash: request.targetHash,
            requiredConfirmations: request.requiredConfirmations,
            confirmationsCount: request.confirmationsCount,
            executed: request.executed,
            createdAt: request.createdAt
        });
    }

    function getRequestCount() external view returns (uint256) {
        return _requestIds.length;
    }

    function addVerifier(address verifier) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(VERIFIER_ROLE, verifier);
    }

    function removeVerifier(address verifier) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(VERIFIER_ROLE, verifier);
    }
}
