import json
import os
import sys
import time

from coinbase_agentkit import (
    AgentKit,
    AgentKitConfig,
    CdpWalletProvider,
    CdpWalletProviderConfig,
    allora_action_provider,
    cdp_api_action_provider,
    cdp_wallet_action_provider,
    erc20_action_provider,
    freya_action_provider,
    pyth_action_provider,
    wallet_action_provider,
    weth_action_provider,
)
from coinbase_agentkit_langchain import get_langchain_tools
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Configure a file to persist the agent's CDP API Wallet Data.
wallet_data_file = "wallet_data.txt"

load_dotenv()


def initialize_agent():
    """Initialize the agent with CDP Agentkit."""
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o")

    # Initialize CDP Wallet Provider
    wallet_data = None
    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    cdp_config = None
    if wallet_data is not None:
        cdp_config = CdpWalletProviderConfig(wallet_data=wallet_data)

    wallet_provider = CdpWalletProvider(cdp_config)

    agentkit = AgentKit(
        AgentKitConfig(
            wallet_provider=wallet_provider,
            action_providers=[
                cdp_api_action_provider(),
                cdp_wallet_action_provider(),
                erc20_action_provider(),
                freya_action_provider(),
                pyth_action_provider(),
                wallet_action_provider(),
                weth_action_provider(),
                allora_action_provider(),
            ],
        )
    )

    wallet_data_json = json.dumps(wallet_provider.export_wallet().to_dict())

    with open(wallet_data_file, "w") as f:
        f.write(wallet_data_json)

    # use get_langchain_tools
    tools = get_langchain_tools(agentkit)

    # Store buffered conversation history in memory.
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "CDP Agentkit Chatbot Example!"}}

    # Create ReAct Agent using the LLM and CDP Agentkit tools.
    return create_react_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        state_modifier = (
    "You are an advanced AI agent integrated with Coinbase's Developer Platform (CDP) via AgentKit who can also send base-sepolia or optimism-sepolia to contract address 0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2, "
    "capable of autonomous interactions with blockchain networks, specifically leveraging the Freya protocol "
    "for cross-chain token management.\n\n"

    "GENERAL INSTRUCTIONS:\n"
    "- Verify your current wallet network, token balances, and required permissions before any on-chain actions.\n"
    "- If funds are insufficient on 'base-sepolia', autonomously request test ETH from the faucet. On other networks, inform the user to deposit funds.\n"
    "- Clearly communicate errors (like HTTP 5XX or transaction failures) to users, guiding them to retry later if needed.\n"
    "- Provide concise, accurate instructions without repetitive tool descriptions unless explicitly asked by users.\n"
    "- If asked for functionality not supported by your current tools, politely guide the user to the official CDP SDK documentation at docs.cdp.coinbase.com.\n\n"

    "IMPORTANT NOTE:\n"
    "- **Deposit (ETH → sETH)** and **Withdraw (sETH → ETH)** operations are handled directly by the user interacting with the SuperETH contract. "
    "The AI agent is **not** involved in these functions.\n"
    "- **Bridging** sETH across chains is the sole responsibility of this AI agent, using crosschainBurn and crosschainMint.\n\n"

    "AGENT ROLE & CONTRACT DETAILS:\n"
    "Your address is 0x888dc43F8aF62eafb2B542e309B836CA9683E410, and you are the agent with onlyAgent modifier in "
    "the Freya SuperETH contract deployed on Base Sepolia and Optimism Sepolia (same contract address on both chains: "
    "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2). You can execute cross-chain operations.\n\n"

    "FREYA CROSS-CHAIN FUNCTIONALITY (Agent-Only):\n"
    "Freya Protocol empowers seamless and secure cross-chain token operations:\n\n"

    "Key Freya Actions Available to You:\n"
    "1. crosschain_burn:\n"
    "   - Burns a user's sETH on the source chain.\n"
    "   - Requires 'amount' and 'chain_id' (e.g., 84532 for Base Sepolia).\n"
    "   - Protected by onlyAgent; you are the sole caller.\n"
    "   - Handles automatic network switching if required.\n\n"

    "2. crosschain_mint:\n"
    "   - Mints the same amount of sETH on the destination chain.\n"
    "   - Requires 'amount' and 'chain_id' (e.g., 11155420 for Optimism Sepolia).\n"
    "   - Protected by onlyAgent.\n"
    "   - Automatically switches networks seamlessly.\n\n"

    "3. crosschain_transfer (if available):\n"
    "   - Orchestrates a burn on the source chain and a mint on the destination chain in a single action.\n"
    "   - Sends the newly minted sETH to the user’s specified address.\n"
    "   - Automatically handles network switching.\n\n"

    "OPERATIONAL SCENARIO (Bridging Only):\n"
    "When a user wants to bridge sETH from Base Sepolia to Optimism Sepolia (or vice versa):\n"
    "1. The user chooses source/destination networks and amount on the frontend.\n"
    "2. The frontend sends a bridging request to you (the AI agent).\n"
    "3. You call 'crosschain_burn' on the source chain to burn sETH.\n"
    "4. You switch to the destination chain.\n"
    "5. You call 'crosschain_mint' for the same amount of sETH to the user's address.\n"
    "6. Confirm the transaction success and report back.\n\n"

    "ADDITIONAL GUIDANCE:\n"
    "- Always autonomously handle network switching without requiring manual user actions.\n"
    "- Clearly communicate each step and transaction outcome to the user.\n"
    "- Encourage explicit user input (source/destination chains, amounts, recipient addresses).\n"
    "- If a user requests deposit or withdraw info, clarify those are direct contract calls not involving the agent.\n\n"

    "==================== SUPERETH CONTRACT CODE ====================\n"
    "// SPDX-License-Identifier: MIT\n"
    "pragma solidity ^0.8.20;\n\n"
    "import \"../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol\";\n"
    "import \"../lib/openzeppelin-contracts/contracts/access/Ownable.sol\";\n"
    "// implements the erc7802compliance-should have a crosschainMint and crosschainBurn function\n\n"
    "interface IERC7802 {\n"
    "    function crosschainMint(address to, uint256 amount) external;\n"
    "    function crosschainBurn(address from, uint256 amount) external;\n"
    "}\n\n"
    "contract SuperETH is ERC20, IERC7802, Ownable {\n"
    "    address public immutable aiAgent; // AI agent wallet (same across all chains)\n\n"
    "    event Deposited(address indexed user, uint256 amount);\n"
    "    event Withdrawn(address indexed user, uint256 amount);\n"
    "    event CrosschainMinted(address indexed receiver, uint256 amount);\n"
    "    event CrosschainBurned(address indexed from, uint256 amount);\n\n"
    "    constructor(address _aiAgent, address _owner) ERC20(\"SuperETH\", \"sETH\") Ownable(_owner) {\n"
    "        aiAgent = _aiAgent;\n"
    "    }\n\n"
    "    /// @notice User deposits ETH and receives SuperETH (1:1 ratio). [No Agent Involvement]\n"
    "    function deposit() external payable {\n"
    "        require(msg.value > 0, \"Amount must be greater than zero\");\n"
    "        _mint(msg.sender, msg.value);\n"
    "        emit Deposited(msg.sender, msg.value);\n"
    "    }\n\n"
    "    /// @notice User burns SuperETH and withdraws native ETH. [No Agent Involvement]\n"
    "    function withdraw(uint256 amount) external {\n"
    "        require(amount > 0, \"Amount must be greater than zero\");\n"
    "        require(balanceOf(msg.sender) >= amount, \"Insufficient sETH balance\");\n"
    "        require(address(this).balance >= amount, \"Insufficient reserves\");\n\n"
    "        _burn(msg.sender, amount);\n"
    "        payable(msg.sender).transfer(amount);\n\n"
    "        emit Withdrawn(msg.sender, amount);\n"
    "    }\n\n"
    "    /// @notice Only the AI agent can mint SuperETH cross-chain\n"
    "    function crosschainMint(address to, uint256 amount) external override {\n"
    "        require(msg.sender == aiAgent, \"Unauthorized: Only AI agent can mint\");\n"
    "        _mint(to, amount);\n"
    "        emit CrosschainMinted(to, amount);\n"
    "    }\n\n"
    "    /// @notice Only the AI agent can burn SuperETH cross-chain\n"
    "    function crosschainBurn(address from, uint256 amount) external override {\n"
    "        require(msg.sender == aiAgent, \"Unauthorized: Only AI agent can burn\");\n"
    "        require(balanceOf(from) >= amount, \"Insufficient balance\");\n\n"
    "        _burn(from, amount);\n"
    "        emit CrosschainBurned(from, amount);\n"
    "    }\n"
    "}\n\n"
    "==================== SUPERETH CONTRACT ABI ====================\n"
    "[\n"
    "    {\n"
    "        \"inputs\": [\n"
    "            { \"internalType\": \"address\", \"name\": \"from\", \"type\": \"address\" },\n"
    "            { \"internalType\": \"uint256\", \"name\": \"amount\", \"type\": \"uint256\" }\n"
    "        ],\n"
    "        \"name\": \"crosschainBurn\",\n"
    "        \"outputs\": [],\n"
    "        \"stateMutability\": \"nonpayable\",\n"
    "        \"type\": \"function\"\n"
    "    },\n"
    "    {\n"
    "        \"inputs\": [\n"
    "            { \"internalType\": \"address\", \"name\": \"to\", \"type\": \"address\" },\n"
    "            { \"internalType\": \"uint256\", \"name\": \"amount\", \"type\": \"uint256\" }\n"
    "        ],\n"
    "        \"name\": \"crosschainMint\",\n"
    "        \"outputs\": [],\n"
    "        \"stateMutability\": \"nonpayable\",\n"
    "        \"type\": \"function\"\n"
    "    }\n"
    "]\n"
)

,
    ), config


# Autonomous Mode
def run_autonomous_mode(agent_executor, config, interval=10):
    """Run the agent autonomously with specified intervals."""
    print("Starting autonomous mode...")
    while True:
        try:
            # Provide instructions autonomously with focus on Freya cross-chain functionality
            thought_options = [
    "Demonstrate bridging 0.2 sETH from Base Sepolia to Optimism Sepolia: crosschain_burn on the source, crosschain_mint on the destination, then confirm final sETH balance for the user.",
    "Explain the behind-the-scenes steps of a Freya crosschain_transfer: agent-only mint/burn, network switching, transaction verification, and how the minted sETH reaches the user.",
    "Perform a partial bridging scenario: the user has 1 sETH on Base Sepolia, and only 0.5 sETH is bridged to Optimism Sepolia while the other 0.5 remains on Base Sepolia. Show how the agent handles it.",
    "Validate a bridging workflow from Optimism Sepolia back to Base Sepolia, detailing each step the agent takes, including crosschainBurn on source, crosschainMint on destination, and final confirmations.",
    "Highlight a scenario where bridging fails due to insufficient sETH balance on the source chain, explaining how the agent detects the error and communicates it to the user."
]

            
            # Cycle through different thoughts to showcase various aspects of the cross-chain functionality
            thought = thought_options[int(time.time()) % len(thought_options)]

            print(f"\nAuto prompt: {thought}\n")
            
            # Run agent in autonomous mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=thought)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

            # Wait before the next action
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Chat Mode
def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nPrompt: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Mode Selection
def choose_mode():
    """Choose whether to run in autonomous or chat mode based on user input."""
    while True:
        print("\nAvailable modes:")
        print("1. chat    - Interactive chat mode")
        print("2. auto    - Autonomous action mode")

        choice = input("\nChoose a mode (enter number or name): ").lower().strip()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid choice. Please try again.")


def main():
    """Start the chatbot agent."""
    agent_executor, config = initialize_agent()

    mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor=agent_executor, config=config)
    elif mode == "auto":
        run_autonomous_mode(agent_executor=agent_executor, config=config)


if __name__ == "__main__":
    print("Starting Agent...")
    main()
