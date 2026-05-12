// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./CarbonCertificateNFT.sol";

contract CarbonMarketplace is AccessControl, ReentrancyGuard, Pausable {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    CarbonCertificateNFT public certificateNFT;
    IERC20 public paymentToken;

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

    struct Purchase {
        uint256 purchaseId;
        uint256 listingId;
        address buyer;
        uint256 tonnes;
        uint256 totalPrice;
        uint256 timestamp;
        bool retired;
    }

    uint256 private _listingIds;
    uint256 private _purchaseIds;

    mapping(uint256 => Listing) public listings;
    mapping(uint256 => Purchase) public purchases;
    mapping(uint256 => uint256[]) public listingPurchases;

    event ListingCreated(uint256 indexed listingId, uint256 indexed tokenId, address indexed seller, uint256 pricePerTonne, uint256 totalTonnes);
    event ListingUpdated(uint256 indexed listingId, uint256 pricePerTonne);
    event ListingCancelled(uint256 indexed listingId);
    event CarbonPurchased(uint256 indexed purchaseId, uint256 indexed listingId, address indexed buyer, uint256 tonnes, uint256 totalPrice);
    event CarbonRetired(uint256 indexed purchaseId, address indexed retirer, bytes32 purpose);

    constructor(address _certificateNFT, address _paymentToken) {
        certificateNFT = CarbonCertificateNFT(_certificateNFT);
        paymentToken = IERC20(_paymentToken);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
    }

    function createListing(
        uint256 tokenId,
        uint256 pricePerTonne,
        uint256 totalTonnes
    ) external whenNotPaused returns (uint256) {
        require(certificateNFT.ownerOf(tokenId) == msg.sender, "Not certificate owner");
        require(totalTonnes > 0, "Must list positive amount");
        require(pricePerTonne > 0, "Price must be positive");

        _listingIds++;
        uint256 listingId = _listingIds;

        listings[listingId] = Listing({
            listingId: listingId,
            tokenId: tokenId,
            seller: msg.sender,
            pricePerTonne: pricePerTonne,
            totalTonnes: totalTonnes,
            availableTonnes: totalTonnes,
            active: true,
            createdAt: block.timestamp
        });

        emit ListingCreated(listingId, tokenId, msg.sender, pricePerTonne, totalTonnes);
        return listingId;
    }

    function purchaseCarbon(uint256 listingId, uint256 tonnes) external nonReentrant whenNotPaused {
        Listing storage listing = listings[listingId];
        require(listing.active, "Listing is not active");
        require(tonnes > 0 && tonnes <= listing.availableTonnes, "Invalid tonne amount");

        uint256 totalPrice = listing.pricePerTonne * tonnes;

        require(
            paymentToken.transferFrom(msg.sender, listing.seller, totalPrice),
            "Payment transfer failed"
        );

        _purchaseIds++;
        uint256 purchaseId = _purchaseIds;

        purchases[purchaseId] = Purchase({
            purchaseId: purchaseId,
            listingId: listingId,
            buyer: msg.sender,
            tonnes: tonnes,
            totalPrice: totalPrice,
            timestamp: block.timestamp,
            retired: false
        });

        listingPurchases[listingId].push(purchaseId);
        listing.availableTonnes -= tonnes;

        if (listing.availableTonnes == 0) {
            listing.active = false;
        }

        emit CarbonPurchased(purchaseId, listingId, msg.sender, tonnes, totalPrice);
    }

    function retireCarbon(uint256 purchaseId, bytes32 purpose) external {
        Purchase storage purchase = purchases[purchaseId];
        require(purchase.buyer == msg.sender, "Not purchase owner");
        require(!purchase.retired, "Already retired");

        purchase.retired = true;
        emit CarbonRetired(purchaseId, msg.sender, purpose);
    }

    function cancelListing(uint256 listingId) external {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender || hasRole(ADMIN_ROLE, msg.sender), "Not authorized");
        require(listing.active, "Already inactive");

        listing.active = false;
        emit ListingCancelled(listingId);
    }

    function updateListingPrice(uint256 listingId, uint256 newPrice) external {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not listing owner");
        require(listing.active, "Listing not active");
        require(newPrice > 0, "Price must be positive");

        listing.pricePerTonne = newPrice;
        emit ListingUpdated(listingId, newPrice);
    }

    function getListing(uint256 listingId) external view returns (Listing memory) {
        return listings[listingId];
    }

    function getListingPurchases(uint256 listingId) external view returns (uint256[] memory) {
        return listingPurchases[listingId];
    }

    function getTotalListings() external view returns (uint256) {
        return _listingIds;
    }

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
