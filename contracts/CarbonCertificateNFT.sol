// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract CarbonCertificateNFT is ERC721URIStorage, ERC721Enumerable, AccessControl, Pausable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");

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

    mapping(uint256 => Certificate) public certificates;
    mapping(bytes32 => uint256[]) public farmCertificates;

    event CertificateMinted(uint256 indexed tokenId, address indexed owner, bytes32 indexed farmId, uint256 carbonTonnes);
    event CertificateVerified(uint256 indexed tokenId, address indexed verifier);
    event CertificateTransferred(uint256 indexed tokenId, address from, address to);

    constructor() ERC721("AgriChain Carbon Certificate", "ACCC-NFT") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
    }

    function mintCertificate(
        address to,
        bytes32 farmId,
        uint256 carbonTonnes,
        string memory methodology,
        string memory tokenURI
    ) external onlyRole(MINTER_ROLE) whenNotPaused returns (uint256) {
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _safeMint(to, newTokenId);
        _setTokenURI(newTokenId, tokenURI);

        certificates[newTokenId] = Certificate({
            tokenId: newTokenId,
            owner: to,
            farmId: farmId,
            carbonTonnes: carbonTonnes,
            methodology: methodology,
            timestamp: block.timestamp,
            verified: false,
            verifier: address(0)
        });

        farmCertificates[farmId].push(newTokenId);

        emit CertificateMinted(newTokenId, to, farmId, carbonTonnes);
        return newTokenId;
    }

    function verifyCertificate(uint256 tokenId) external onlyRole(VERIFIER_ROLE) {
        require(_exists(tokenId), "Certificate does not exist");
        require(!certificates[tokenId].verified, "Already verified");

        certificates[tokenId].verified = true;
        certificates[tokenId].verifier = msg.sender;

        emit CertificateVerified(tokenId, msg.sender);
    }

    function getCertificate(uint256 tokenId) external view returns (Certificate memory) {
        require(_exists(tokenId), "Certificate does not exist");
        return certificates[tokenId];
    }

    function getFarmCertificates(bytes32 farmId) external view returns (uint256[] memory) {
        return farmCertificates[farmId];
    }

    function totalSupply() external view returns (uint256) {
        return _tokenIds.current();
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721Enumerable, AccessControl) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
