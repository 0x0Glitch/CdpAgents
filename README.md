# Skywire Protocol

<img width="480" alt="image" src="https://github.com/user-attachments/assets/de39f7f6-59db-4623-a225-820301b37363" />


## What is Skywire?

Skywire is an innovative cross-chain interoperability protocol that enables seamless token transfers between different super chain blockchain networks like Base, Optimism, Unichain, etc. It provides a secure and efficient way to swap and bridge tokens across multiple blockchain ecosystems, making cross-chain transactions accessible and user-friendly by utilizing AI agents.

## What does Skywire do?

- **Cross-Chain Token Swaps**: Enables users to swap tokens between different super chain blockchain networks like Base, Optimism, Unichain, etc.
- **Token Bridging**: Facilitates the secure transfer of tokens from one super chain blockchain network to another
- **Automated Processing**: Uses AI agents to handle cross-chain transactions automatically
- **Smart Contract Integration**: Implements secure smart contracts with agent-only access for critical operations

## How does Skywire work?

<img width="652" alt="image" src="https://github.com/user-attachments/assets/ae49b2a7-89f3-460e-a48f-f002c080f546" />



Skywire operates through a sophisticated system of smart contracts and AI agents:

### Smart Contracts

- Deployed on multiple OP stack blockchain networks like Base, Optimism, Unichain, etc.
- Implement `onlyAgent` modifiers for secure operations
- Handle token minting and burning across chains
- Deployed on the address: `0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2` on base-sepolia, optimism-sepolia, zora and unichain

### Cross-Chain Communication

- Secure message passing between chains
- Verification of cross-chain transactions
- Atomic swaps for guaranteed transaction completion

### Token Management

- Cross-chain minting of equivalent tokens
- Secure burning of tokens on the source chain
- Maintaining token supply consistency across chains

## Working of the SuperERC20 Token Contracts

The SuperETH contract is an ERC-20 token that allows users to seamlessly wrap and unwrap ETH into SuperETH (sETH) at a 1:1 ratio. Users can deposit ETH into the contract to receive an equivalent amount of sETH, which can be used for on-chain transactions or transferred across supported chains. At any time, users can redeem or withdraw sETH to reclaim their ETH.

A key feature of this contract is cross-chain functionality, facilitated by an AI agent (a wallet with the same address on multiple chains). This agent is the only entity authorized to call `crosschainMint` and `crosschainBurn`, ensuring that SuperETH is only minted on the destination chain after an equivalent amount has been burned on the source chain. This approach eliminates reliance on third-party bridges, reducing costs, improving security, and enabling trustless, decentralized multi-chain ETH transfers.

## AI Agents Implementation

Skywire utilizes AI agents as trusted intermediaries for cross-chain operations:

### Agent Responsibilities

- Execute cross-chain mint functions
- Handle token burning operations
- Verify transaction validity
- Monitor network status

### Security Features

- `onlyAgent` modifier ensures only authorized agents can execute critical functions
- AI-powered validation of transactions
- Automated security checks and balances

### Custom AgentKit Actions

We've extended Coinbase's AgentKit framework with custom actions specifically for cross-chain operations. These actions are located in the `skywire_not/agentkit/examples/skywire-crosschain/` directory:

- `crosschain_burn.py`: Implements the action for burning tokens on the source chain
- `crosschain_mint.py`: Handles minting tokens on the destination chain
- `crosschain_transfer.py`: Orchestrates the entire cross-chain transfer process

These custom actions are registered in the agent's action registry, allowing it to understand and execute complex cross-chain operations based on natural language instructions.

### Chatbot Integration

The agent interface is powered by a modified version of the CDP-LangChainBot example from AgentKit. The implementation can be found in `skywire_not/agentkit/examples/cdp-langchainbot/chatbot.py`, which we've extended to handle cross-chain transfer requests and provide user-friendly responses about transaction status.

### Starting the Agent

To start the Skywire agent and enable cross-chain functionality, follow these steps:

1. Navigate to the AgentKit directory:

```bash
cd skywire_not/agentkit
```

2. Set up the environment variables by creating a `.env` file in the root directory with your API keys and RPC endpoints:

```bash
# Create .env file
touch .env
```

Add the following variables to your `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
BASE_SEPOLIA_RPC_URL=your_base_sepolia_rpc_url
OPTIMISM_SEPOLIA_RPC_URL=your_optimism_sepolia_rpc_url
ZORA_RPC_URL=your_zora_rpc_url
UNICHAIN_RPC_URL=your_unichain_rpc_url
AGENT_PRIVATE_KEY=your_agent_wallet_private_key
```

3. Install the required dependencies:

```bash
pip install -e .
pip install -r examples/requirements.txt
```

4. Start the Skywire agent:

```bash
# For the cross-chain agent with CLI interface
python -m examples.skywire-crosschain.agent

# OR for the chatbot interface
python -m examples.cdp-langchainbot.chatbot --skywire-agent
```

5. Once the agent is running, it will automatically monitor for cross-chain transfer requests and execute the necessary transactions. You can interact with it through the CLI or chatbot interface depending on which version you started.

## Architecture

Skywire consists of three main components:

### 1. Smart Contracts

The SuperERC20 token contracts are deployed on multiple networks with the following capabilities:
- Deposit/withdraw native chain tokens
- Cross-chain minting and burning via agent verification
- 1:1 token backing across all supported networks

**Deployment Address**: `0xf5dF4e1CFBB1091Db3dEB278A2fdf73242612e43`

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
- Python 3.9+ for running the agent
- OpenAI API key for agent functionality

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

To modify or extend the custom actions:

```bash
cd skywire_not/agentkit/examples/skywire-crosschain
# Edit the custom action files
```

### Frontend Development

The frontend is a React application using Vite, Tailwind CSS, and ethers.js:

```bash
cd skywire_not/frontend
npm install
npm run dev
```

## Future Goals

### Protocol Enhancement

- Support for additional blockchain networks
- Optimization of cross-chain transaction speeds
- Enhanced security measures

### AI Agent Improvements

- Advanced transaction validation algorithms
- Improved error handling and recovery
- Enhanced monitoring capabilities

### User Experience

- Simplified transaction interface
- Better transaction tracking
- Enhanced analytics and reporting

### Ecosystem Growth

- Integration with more DeFi protocols
- Partnership with major blockchain networks
- Community-driven development initiatives

## Security

Skywire employs several security measures:

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

