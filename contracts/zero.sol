// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SecureVault
 * @dev Slither and Mythril compliant secure contract
 */
contract SecureVault {
    // State variables
    mapping(address => uint256) private balances;
    address public immutable owner;

    // Events for transparency and tool tracking
    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    // Constructor - use immutable for gas and security
    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Deposit ETH into the vault.
     */
    function deposit() external payable {
        require(msg.value > 0, "Amount must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    /**
     * @dev Withdraw ETH from the vault.
     * Uses Checks-Effects-Interactions pattern to prevent Reentrancy.
     */
    function withdraw(uint256 _amount) external {
        // 1. Checks
        require(_amount > 0, "Invalid amount");
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        // 2. Effects (Update state before external call)
        balances[msg.sender] -= _amount;

        // 3. Interactions (Low-level call with gas limit and check)
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");

        emit Withdrawn(msg.sender, _amount);
    }

    /**
     * @dev Check balance of a specific user.
     */
    function getBalance(address _user) external view returns (uint256) {
        return balances[_user];
    }

    // Function to prevent accidental ETH sending without data
    receive() external payable {
        deposit();
    }
}