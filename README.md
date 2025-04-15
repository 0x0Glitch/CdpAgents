## Skywire Protocol Overview
Skywire Protocol is an advanced cross-chain interoperability solution engineered to facilitate seamless token transfers between distinct super chain blockchain networks, including Base, Optimism, Unichain, among others. The protocol implements a secure and efficient architecture for token swapping and bridging across multiple blockchain ecosystems, employing artificial intelligence agents to ensure accessibility and user-friendliness.

## Core Functionality
The Skywire Protocol provides the following primary capabilities:

* **Cross-Chain Token Swaps**: Enables the exchange of tokens between different super chain blockchain networks
* **Token Bridging**: Facilitates secure token transfers across blockchain ecosystems
* **Automated Transaction Processing**: Utilizes AI agents for automatic cross-chain transaction management
* **Secure Smart Contract Implementation**: Deploys contracts with agent-only access for critical operations

## Technical Architecture
### System Components
Skywire's architecture consists of three principal components:

#### 1. Smart Contract Infrastructure
The protocol deploys SuperERC20 token contracts across multiple networks with the following capabilities:

* Native chain token deposit/withdrawal functionality
* Cross-chain minting and burning operations with agent verification
* Maintenance of 1:1 token backing across all supported networks

**Deployment Address**: `0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43`

#### 2. AI Agent System
Built upon Coinbase's AgentKit framework, the agent system manages:

* Cross-chain transaction orchestration with security verification
* Transaction confirmation and validation
* Network monitoring and exception handling

The system implements specialized custom actions for:

* Token burning on source chain
* Token minting on destination chain
* End-to-end cross-chain transfer orchestration

#### 3. User Interface
A React-based frontend interface providing:

* Network selection functionality for source and destination chains
* Multi-network token balance visualization
* Streamlined bridging process
* Transaction status monitoring
* Web3 wallet integration

### Operational Workflow
The protocol operates through a sophisticated system of smart contracts and AI agents:

#### Smart Contract Implementation
* Contracts are deployed across multiple OP stack blockchain networks
* Implementation of `onlyAgent` modifiers ensures operational security
* Contracts handle token minting and burning operations across chains

#### Cross-Chain Communication Protocol
* Secure inter-chain message transmission
* Cross-chain transaction verification
* Atomic swap implementation for transaction integrity

#### Token Management System
* Cross-chain minting of equivalent tokens
* Secure token burning on the source chain
* Cross-chain token supply consistency maintenance

### SuperERC20 Token Contract Functionality
The SuperETH contract functions as an ERC-20 token enabling users to wrap and unwrap ETH into SuperETH (sETH) at a 1:1 ratio. Users may deposit ETH to receive an equivalent sETH amount, which can be utilized for on-chain transactions or cross-chain transfers. Users retain the ability to redeem sETH for ETH at any time.

The contract's cross-chain functionality is facilitated by an AI agent (a wallet with identical addresses across multiple chains). This agent possesses exclusive authorization to execute `crosschainMint` and `crosschainBurn` functions, ensuring that SuperETH is minted on the destination chain only after an equivalent amount has been burned on the source chain. This approach eliminates third-party bridge dependence, thereby reducing costs, enhancing security, and enabling trustless, decentralized multi-chain ETH transfers.

## AI Agent Implementation

### Agent Responsibilities
* Execution of cross-chain minting functions
* Management of token burning operations
* Transaction validity verification
* Network status monitoring

### Security Features
* `onlyAgent` modifier implementation ensures authorized execution of critical functions
* AI-powered transaction validation
* Automated security verification systems

### Custom AgentKit Actions
The protocol extends Coinbase's AgentKit framework with custom actions specifically designed for cross-chain operations. These custom actions are registered in the agent's action registry, enabling natural language instruction processing for complex cross-chain operations, including:

* Source chain token burning
* Destination chain token minting
* Complete cross-chain transfer orchestration

### Chatbot Integration
The agent interface utilizes a modified version of the CDP-LangChainBot example from AgentKit. The implementation has been extended to process cross-chain transfer requests and provide user-friendly transaction status updates.

## Dual Agent System
The protocol implements a dual agent system to enhance cross-chain operations between different blockchain networks, comprising two specialized agents:

* **Base Agent (AiAgen1.py)**: Optimized for Base blockchain operations (chain ID: 84532)
* **Optimism Agent (AiAgent2.py)**: Optimized for Optimism blockchain operations (chain ID: 10)

Each agent is specifically configured for its respective blockchain network, with dedicated wallet providers and network-specific parameters. The agents are coordinated through a central API service providing:

* **Automatic Chain Routing**: Intelligent instruction routing based on content analysis
* **Manual Chain Selection**: Optional explicit chain specification
* **Asynchronous Processing**: Background task execution with monitoring capabilities
* **Process Management**: Automated agent process initialization and management

The dual agent architecture enables efficient cross-chain operations through:

* Chain-specific configuration maintenance
* Parallel operation processing across different chains
* Unified API interface provision for cross-chain interactions
* Transaction isolation between blockchain networks

This system is accessible via a RESTful API that processes natural language instructions and determines appropriate agent routing based on content analysis or explicit chain specification.

## Supported Networks
* Base Sepolia (`0x14913`)
* Optimism Sepolia (`0xA8F3C`)
* Zora (`0x7777777`)
* Unichain (`0x82`)

## Implementation Guidelines

### Prerequisites
* Node.js 18+ and npm
* MetaMask or compatible Web3 wallet
* Test ETH on supported networks
* Python 3.9+ for agent execution
* OpenAI API key for agent functionality

### Installation Procedure
1. Acquire the project:
```bash
# Download and extract the project
cd skywire
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Initialize the development server:
```bash
npm run dev
```

4. Access the application interface at `http://localhost:5173`

### Agent Initialization
To initialize the Skywire agent and enable cross-chain functionality:

1. Navigate to the AgentKit directory:
```bash
cd agentkit
```

2. Configure environment variables by creating a `.env` file with API keys and RPC endpoints:
```
OPENAI_API_KEY=your_openai_api_key
BASE_SEPOLIA_RPC_URL=your_base_sepolia_rpc_url
OPTIMISM_SEPOLIA_RPC_URL=your_optimism_sepolia_rpc_url
ZORA_RPC_URL=your_zora_rpc_url
UNICHAIN_RPC_URL=your_unichain_rpc_url
AGENT_PRIVATE_KEY=your_agent_wallet_private_key
```

3. Install dependencies:
```bash
pip install -e .
pip install -r examples/requirements.txt
```

4. Initialize the Skywire agent:
```bash
# For the cross-chain agent with CLI interface
python -m examples.skywire-crosschain.agent

# OR for the chatbot interface
python -m examples.cdp-langchainbot.chatbot --skywire-agent

# OR for the dual agent API service
python -m examples.langchain-cdp-chatbot.dual_agent_api
```

Upon initialization, the agent will monitor cross-chain transfer requests and execute necessary transactions. Interaction is possible through the CLI or chatbot interface depending on the initialized version.

### Bridge Utilization
1. Connect a wallet via the "Connect Wallet" button
2. Select source and destination networks
3. Specify the ETH amount for bridging
4. Provide recipient address (defaults to connected wallet)
5. Initiate the process by selecting "Bridge Your ETH"
6. Confirm the transaction through the wallet interface
7. The AI agent will automatically manage the cross-chain process

## Development

### Agent Development
The agent system utilizes Coinbase's AgentKit framework. For agent development:

```bash
cd agentkit
# Follow AgentKit README setup instructions
```

For custom action modification:

```bash
cd agentkit/examples/skywire-crosschain
# Modify the custom action files as required
```

### Dual Agent API Development
For dual agent API system development:

```bash
cd agentkit/python/examples/langchain-cdp-chatbot
# Install dependencies
pip install -r requirements-api.txt
# Initialize the API server
python dual_agent_api.py
```

The API server will initialize on `http://localhost:8000` with endpoints for:
* Blockchain agent instruction submission
* Task status monitoring
* Result retrieval

### Frontend Development
The frontend utilizes React with Vite, Tailwind CSS, and ethers.js:

```bash
cd frontend
npm install
npm run dev
```

## Strategic Roadmap

### Protocol Enhancement
* Extended blockchain network support
* Cross-chain transaction speed optimization
* Enhanced security implementation

### AI Agent Advancement
* Advanced transaction validation algorithm development
* Improved exception handling and recovery systems
* Enhanced monitoring capability implementation

### User Experience Refinement
* Interface simplification
* Enhanced transaction tracking
* Improved analytics and reporting systems

### Ecosystem Expansion
* DeFi protocol integration expansion
* Major blockchain network partnership development
* Community-driven development initiative implementation

## Security Measures
Skywire implements comprehensive security measures:

* `onlyAgent` modifiers restrict critical function access to authorized agents
* Transaction verification prevents unauthorized minting/burning operations
* Confirmation monitoring ensures transaction finality
* 1:1 token backing maintains asset integrity

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
* Developed with Coinbase AgentKit
* Leverages multi-chain Ethereum development capabilities
* Inspired by the vision of seamless blockchain ecosystem interoperability

## Custom Implementation Details

### Dual Agent System Implementation
The Skywire Protocol implements an advanced dual agent system enabling cross-chain operations between different blockchain networks:

#### Specialized Chain Agents
Located at `agentkit/python/examples/langchain-cdp-chatbot/`:
* **Base Agent (AiAgen1.py)**: Specialized for Base blockchain operations (chain ID: 84532)
* **Optimism Agent (AiAgent2.py)**: Specialized for Optimism blockchain operations (chain ID: 10)
* Each agent implements chain-specific configurations and wallet connections

#### Central API Service
Located at `agentkit/python/examples/langchain-cdp-chatbot/dual_agent_api.py`:
* Implements RESTful API for agent interaction
* Provides comprehensive task management, monitoring, and orchestration
* Intelligent instruction routing based on content analysis
* Asynchronous cross-chain operation processing

#### Cross-Chain Orchestration
* Coordinated token burning on source chain and minting on destination chain
* Cross-network transaction verification and confirmation
* Cross-chain state consistency maintenance

The dual agent architecture provides several advantages:
* **Enhanced Reliability**: Chain-specific configurations mitigate cross-chain errors
* **Parallel Processing**: Simultaneous operation execution across different chains
* **Specialized Functionality**: Chain-optimized agent configuration
* **Unified Interface**: Single API endpoint for all cross-chain operations

### Frontend Integration with Dual Agents
The frontend React application interfaces with the dual agent system through:

#### Web3Service API Client
Located at `frontend/src/services/web3Service.js`:
* JavaScript client implementation for dual agent API communication
* Cross-chain transfer request and status monitoring management
* Wallet connection, network switching, and token operation functionality

#### BridgeForm Component
Located at `frontend/src/components/Bridge/BridgeForm.jsx`:
* User interface for cross-chain transfer initiation
* Transfer progress monitoring through task status polling
* Error state and success feedback handling

### Key Implementation Features
* **Intelligent Chain Routing**: Automatic agent determination for instruction handling
* **Manual Chain Selection**: Optional explicit chain ID specification
* **Asynchronous Processing**: Background task execution with status tracking
* **Real-time Status Updates**: 5-second interval agent API status polling
* **Comprehensive Error Handling**: Network issue, transaction failure, and timeout condition management
* **Chain Auto-switching**: Automatic wallet network switching based on selected chains

This dual agent architecture effectively bridges disparate blockchain networks, creating a seamless AI-powered cross-chain transfer experience.

