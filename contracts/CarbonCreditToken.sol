// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract CarbonCreditToken is ERC20, ERC20Burnable, AccessControl, Pausable {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant BURNER_ROLE = keccak256("BURNER_ROLE");

    event CarbonCreditsMinted(address indexed to, uint256 amount, bytes32 indexed farmId);
    event CarbonCreditsRetired(address indexed from, uint256 amount, bytes32 indexed purpose);

    constructor() ERC20("AgriChain Carbon Credit", "ACCC") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    function mint(address to, uint256 amount, bytes32 farmId) external onlyRole(MINTER_ROLE) whenNotPaused {
        _mint(to, amount);
        emit CarbonCreditsMinted(to, amount, farmId);
    }

    function retire(uint256 amount, bytes32 purpose) external {
        _burn(msg.sender, amount);
        emit CarbonCreditsRetired(msg.sender, amount, purpose);
    }

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }

    function addMinter(address minter) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(MINTER_ROLE, minter);
    }

    function removeMinter(address minter) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(MINTER_ROLE, minter);
    }
}
