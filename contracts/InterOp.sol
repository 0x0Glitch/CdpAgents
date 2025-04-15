// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../lib/openzeppelin-contracts/contracts/access/Ownable.sol";
import "../lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";

interface IERC7802 {
    function crosschainMint(address to, uint256 amount) external;
    function crosschainBurn(address from, uint256 amount) external;
}

contract SuperUSDC is ERC20, IERC7802, Ownable {
    address public immutable aiAgent;
    IERC20 public immutable usdc;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event CrosschainMinted(address indexed receiver, uint256 amount);
    event CrosschainBurned(address indexed from, uint256 amount);

    constructor(address _aiAgent, address _owner, address _usdc) ERC20("SuperUSDC", "sUSDC") Ownable(_owner) {
        aiAgent = _aiAgent;
        usdc = IERC20(_usdc);
    }

    function deposit(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        require(usdc.transferFrom(msg.sender, address(this), amount), "USDC transfer failed");

        _mint(msg.sender, amount);
        emit Deposited(msg.sender, amount);
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        require(balanceOf(msg.sender) >= amount, "Insufficient sUSDC balance");
        require(usdc.balanceOf(address(this)) >= amount, "Insufficient reserves");

        _burn(msg.sender, amount);
        require(usdc.transfer(msg.sender, amount), "USDC transfer failed");

        emit Withdrawn(msg.sender, amount);
    }

    function crosschainMint(address to, uint256 amount) external override {
        require(msg.sender == aiAgent, "Unauthorized: Only AI agent can mint");
        _mint(to, amount);
        emit CrosschainMinted(to, amount);
    }

    function crosschainBurn(address from, uint256 amount) external override {
        require(msg.sender == aiAgent, "Unauthorized: Only AI agent can burn");
        require(balanceOf(from) >= amount, "Insufficient balance");

        _burn(from, amount);
        emit CrosschainBurned(from, amount);
    }
}