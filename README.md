# Skywire Protocol

<div align="center">
  <img src="./skywire_not/frontend/src/assets/logo-icon.svg" alt="skywire Logo" width="150"/>
  <h3>AI-Powered Cross-Chain Interoperability Protocol</h3>
</div>

## Overview

skywire is a cutting-edge cross-chain interoperability protocol designed to enable seamless token transfers between super chain networks. Built with AI-powered agents, skywire eliminates traditional bridging complexities to deliver fast, secure, and automated cross-chain transactions.

### Key Features

- **Cross-Chain Transfers**: Transfer tokens between Base, Optimism, Zora, and Unichain networks
- **AI-Powered Agents**: Automated transaction execution and verification
- **SuperERC20**: Custom token standard with 1:1 wrapping capability 
- **Agent Security**: Enhanced security through `onlyAgent` modifiers
- **Modern UI**: Intuitive React-based interface with a beautiful design

## Architecture

skywire consists of three main components:

### 1. Smart Contracts

The SuperERC20 token contracts are deployed on multiple networks with the following capabilities:
- Deposit/withdraw native chain tokens
- Cross-chain minting and burning via agent verification
- 1:1 token backing across all supported networks

**Deployment Address**: `0xE55A698143bbb447F09b2628aAfE04991B764067`

### 2. AI Agent System

Built on Coinbase's AgentKit framework, the agent system handles:
- Secure cross-chain transaction orchestration
- Transaction verification and confirmation
- Chain monitoring and error handling

The agent implements custom actions:
- `crosschain_burn`: Burns tokens on source chain
- `crosschain_mint`: Mints tokens on destination chain
- `crosschain_transfer`: Orchestrates complete cross-chain transfers

### 3. Frontend Interface

A React-based user interface that provides:
- Network selection for source and destination chains
- Token balance display across networks
- Intuitive bridging process
- Transaction status monitoring
- Integration with web3 wallets

## Supported Networks

- Base Sepolia (`0x14913`)
- Optimism Sepolia (`0xA8F3C`)
- Zora (`0x7777777`)
- Unichain (`0x82`)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- MetaMask or compatible Web3 wallet
- Test ETH on supported networks

### Installation

1. Download the project
```bash
# Download and extract the project
cd skywire
```

2. Install frontend dependencies
```bash
cd skywire_not/frontend
npm install
```

3. Start the development server
```bash
npm run dev
```

4. Access the application at `http://localhost:5173`

### Using the Bridge

1. Connect your wallet by clicking the "Connect Wallet" button
2. Select source and destination networks
3. Enter the amount of ETH to bridge
4. Provide the recipient address (defaults to your connected wallet)
5. Click "Bridge Your ETH"
6. Confirm the transaction in your wallet
7. The AI agent will automatically handle the cross-chain process

## Development

### Agent Development

The agent system is built on Coinbase's AgentKit framework. To work on the agent:

```bash
cd skywire_not/agentkit
# Follow the setup instructions in the AgentKit README
```

### Frontend Development

The frontend is a React application using Vite, Tailwind CSS, and ethers.js:

```bash
cd skywire_not/frontend
npm install
npm run dev
```

## Security

skywire employs several security measures:

- `onlyAgent` modifiers restrict critical functions to authorized agents
- Transaction verification prevents unauthorized minting/burning
- Confirmation monitoring ensures transaction finality
- 1:1 token backing maintains asset integrity

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Coinbase AgentKit
- Leverages the power of multi-chain Ethereum development
- Inspired by the vision of a seamless, borderless blockchain ecosystem
