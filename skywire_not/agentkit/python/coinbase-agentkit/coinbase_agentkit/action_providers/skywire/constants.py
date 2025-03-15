"""Constants for the Skywire Protocol integration."""

from typing import Dict
from web3 import Web3

# Supported networks for the Skywire protocol
NETWORKS = ["base-sepolia", "optimism-sepolia"]

# Network configurations for supported chains
NETWORKS_CONFIG = {
    "base-sepolia": {
        "name": "Base Sepolia",
        "chain_id": 84532,
        "rpc_url": "https://sepolia.base.org",
    },
    "optimism-sepolia": {
        "name": "Optimism Sepolia",
        "chain_id": 11155420,
        "rpc_url": "https://sepolia.optimism.io",
    },
}

# Mapping of network IDs to chain IDs
CHAIN_IDS = {network: config["chain_id"] for network, config in NETWORKS_CONFIG.items()}

# Contract address for the Skywire Protocol SuperETH token on different networks
CONTRACT_ADDRESS = "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2"  # Same address across all networks

# Contract address for the Skywire Protocol
NEW_CONTRACT_ADDRESS = "0xE55A698143bbb447F09b2628aAfE04991B764067"

# AI Agent address with onlyAgent modifier access
AGENT_ADDRESS = "0x888dc43F8aF62eafb2B542e309B836CA9683E410"

# Agent address for secure operations
NEW_AGENT_ADDRESS = "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2"

# ABI for the SuperETH contract
SUPER_ERC20_ABI = [
  {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
  {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
  {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
  {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
  {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
  {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
  {"inputs": [], "name": "deposit", "outputs": [], "stateMutability": "payable", "type": "function"},
  {"inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "withdraw", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
  {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "crosschainMint", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
  {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "crosschainBurn", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
  {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "Deposited", "type": "event"},
  {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "Withdrawn", "type": "event"},
  {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "receiver", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "CrosschainMinted", "type": "event"},
  {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "CrosschainBurned", "type": "event"}
]

# ABI for the SuperERC20 contract
NEW_SUPER_ERC20_ABI = SUPER_ERC20_ABI
