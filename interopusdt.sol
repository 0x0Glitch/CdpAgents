// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../lib/openzeppelin-contracts/contracts/access/Ownable.sol";
import "../lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";
//implements the erc7802compliance-should have an crosschainmint and crosschainburn function
//will create an standard for the crosschain transactions
//this will be used by the AI agent to mint and burn the superusdt
//the owner of the contract will not be able to mint and burn the superusdt
//to reduce the centralisation risk involved with the owner
//only ai agent will be able to mint and burn the superusdt
//the user can deposit usdt and receive superusdt in return
//the user can withdraw the usdt by burning the superusdt
//the ai agent can mint and burn the superusdt across chains

interface IERC7802 {
    function crosschainMint(address to, uint256 amount) external;
    function crosschainBurn(address from, uint256 amount) external;
}

contract SuperUSDT is ERC20, IERC7802, Ownable {
    address public immutable aiAgent;
    IERC20 public immutable usdt;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event CrosschainMinted(address indexed receiver, uint256 amount);
    event CrosschainBurned(address indexed from, uint256 amount);

    constructor(address _aiAgent, address _owner, address _usdt) ERC20("SuperUSDT", "sUSDT") Ownable(_owner) {
        aiAgent = _aiAgent;
        usdt = IERC20(_usdt);
    }

    function deposit(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        require(usdt.transferFrom(msg.sender, address(this), amount), "USDT transfer failed");

        _mint(msg.sender, amount);
        emit Deposited(msg.sender, amount);
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        require(balanceOf(msg.sender) >= amount, "Insufficient sUSDT balance");
        require(usdt.balanceOf(address(this)) >= amount, "Insufficient reserves");

        _burn(msg.sender, amount);
        require(usdt.transfer(msg.sender, amount), "USDT transfer failed");

        emit Withdrawn(msg.sender, amount);
    }

    function crosschainMint(address to, uint256 amount) external override {
        require(msg.sender == aiAgent, "Unauthorized: Only AI agent can mint");
        _mint(to, amount);
        emit CrosschainMinted(to, amount);
    }
    //only agent will be able to call these functions
    //except deposit
    //whoever send usdt to the contract will receive equal amount of the superUSDT
    //@dev User deposits USDT and receives SuperUSDT (1:1 ratio)
    function crosschainBurn(address from, uint256 amount) external override {
        require(msg.sender == aiAgent, "Unauthorized: Only AI agent can burn");
        require(balanceOf(from) >= amount, "Insufficient balance");

        _burn(from, amount);
        emit CrosschainBurned(from, amount);
    }
}