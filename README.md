# Skywire Protocol



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
- Deployed on the address: `0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43` on base-sepolia, optimism-sepolia, zora and unichain

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

### Dual Agent System

We've developed a dual agent system to enhance cross-chain operations between different blockchain networks. This system consists of two specialized agents:

- **Base Agent (`AiAgen1.py`)**: Specialized for Base blockchain operations (chain ID: 84532)
- **Optimism Agent (`AiAgent2.py`)**: Specialized for Optimism blockchain operations (chain ID: 10)

Each agent is individually tuned for its respective blockchain network, with dedicated wallet providers and network-specific configurations. The agents are coordinated by a central API service implemented in `dual_agent_api.py` that provides:

- **Automatic Chain Routing**: Intelligently routes instructions to the appropriate agent based on content analysis
- **Manual Chain Selection**: Allows explicit specification of which chain to use for an instruction
- **Asynchronous Processing**: Tasks run in the background and can be monitored via API
- **Process Management**: Automatically starts and manages the agent processes as needed

The dual agent architecture enables more efficient cross-chain operations by:
1. Maintaining specialized configurations for each chain
2. Enabling parallel processing of operations on different chains
3. Providing a unified API interface for cross-chain interactions
4. Ensuring transaction isolation between different blockchain networks

This system can be accessed through a RESTful API that accepts natural language instructions and automatically determines which agent should handle the request based on the content or explicit chain specification.

### Starting the Agent

To start the Skywire agent and enable cross-chain functionality, follow these steps:

1. Navigate to the AgentKit directory:

```bash
cd skywire_not/agentkit
```

2. Set up the environment variables by creating a `.env` file in the root directory with your API keys and RPC endpoints:


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

# OR for the dual agent API service
python -m examples.langchain-cdp-chatbot.dual_agent_api
```

5. Once the agent is running, it will automatically monitor for cross-chain transfer requests and execute the necessary transactions. You can interact with it through the CLI or chatbot interface depending on which version you started.

## Architecture

### Flow Diagram

In this flow:
1. The user interacts with the Freya Frontend
2. They can either perform a simple swap or bridge tokens cross-chain
3. For cross-chain bridging, the process involves:
   - First swapping to SuperETH (sETH) on the source chain
   - The AI Agent handling the cross-chain transfer process
   - Burning sETH on the source chain
   - Minting sETH on the destination chain

Skywire consists of three main components:

### 1. Smart Contracts

The SuperERC20 token contracts are deployed on multiple networks with the following capabilities:
- Deposit/withdraw native chain tokens
- Cross-chain minting and burning via agent verification
- 1:1 token backing across all supported networks

**Deployment Address**: `0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43`

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

### Dual Agent API Development

To work on the dual agent API system:

```bash
cd skywire_not/contract-calling/agentkit/python/examples/langchain-cdp-chatbot
# Install dependencies
pip install -r requirements-api.txt
# Start the API server
python dual_agent_api.py
```

The API server will start on http://localhost:8000 and provide endpoints for:
- Submitting instructions to either blockchain agent
- Monitoring task status
- Retrieving task results

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

## Custom Implementation

### Dual Agent System Implementation

I have designed and implemented a sophisticated dual agent system to enable cross-chain operations between different blockchain networks. This system is one of the key innovations of the Skywire Protocol:

1. **Specialized Chain Agents**: Located at `agentkit/python/examples/langchain-cdp-chatbot/`
   - **Base Agent (`AiAgen1.py`)**: Specialized agent configured for Base blockchain operations (chain ID: 84532)
   - **Optimism Agent (`AiAgent2.py`)**: Specialized agent configured for Optimism blockchain operations (chain ID: 10)
   - Each agent has chain-specific configurations and wallet connections

2. **Central API Service**: Located at `agentkit/python/examples/langchain-cdp-chatbot/dual_agent_api.py`
   - Implements a RESTful API for interacting with both agents
   - Provides task management, monitoring, and process orchestration
   - Implements intelligent instruction routing based on content analysis
   - Enables asynchronous processing of cross-chain operations

3. **Cross-Chain Orchestration**: 
   - Coordinate burning tokens on source chain and minting on destination chain
   - Ensure transaction verification and confirmation across networks
   - Maintain consistent state between different blockchain networks

The dual agent architecture provides several key advantages:
- **Enhanced Reliability**: Chain-specific configurations prevent cross-chain errors
- **Parallel Processing**: Operations on different chains can run simultaneously
- **Specialized Functionality**: Each agent can be optimized for its target chain
- **Unified Interface**: A single API endpoint handles all cross-chain operations

My implementation also includes the frontend integration with this dual agent system:

### Frontend Integration with Dual Agents

The frontend React application communicates with the dual agent system through:

1. **Web3Service API Client**: Located at `frontend/src/services/web3Service.js`
   - Implements a JavaScript client that communicates with the dual agent API
   - Manages cross-chain transfer requests and status monitoring
   - Includes functions for wallet connection, network switching, and token operations

2. **BridgeForm Component**: Located at `frontend/src/components/Bridge/BridgeForm.jsx`
   - Provides the user interface for initiating cross-chain transfers
   - Implements task status polling to monitor transfer progress
   - Handles error states and success feedback

### Key Features of My Implementation

- **Intelligent Chain Routing**: Automatically determines which agent should handle each instruction
- **Manual Chain Selection**: Allows explicit specification of the chain ID for an instruction
- **Asynchronous Processing**: Tasks run in the background with status tracking
- **Real-time Status Updates**: The frontend polls the agent API for status updates every 5 seconds
- **Error Handling**: Robust error handling for network issues, transaction failures, and timeout conditions
- **Chain Auto-switching**: Automatic wallet network switching based on the selected source and target chains

This dual agent architecture bridges the gap between different blockchain networks, creating a seamless cross-chain transfer experience powered by AI.

