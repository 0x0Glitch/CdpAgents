import json
import os
import sys
import time
from decimal import Decimal
from typing import Any, Dict, List, Optional

from coinbase_agentkit import (
    AgentKit,
    AgentKitConfig,
    CdpWalletProvider,
    CdpWalletProviderConfig,
    allora_action_provider,
    cdp_api_action_provider,
    cdp_wallet_action_provider,
    erc20_action_provider,
    pyth_action_provider,
    skywire_action_provider,
    wallet_action_provider,
    weth_action_provider,
)
from coinbase_agentkit.network import CHAIN_ID_TO_NETWORK_ID, NETWORK_ID_TO_CHAIN
from coinbase_agentkit_langchain import get_langchain_tools

from dotenv import load_dotenv

# The LangChain / LLM stack
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv()

wallet_data_file = "wallet_data.txt"

###############################################################################
#                SUPPORTED CHAINS & DEFAULT CHAIN
###############################################################################


SUPPORTED_CHAINS = {
    # Base Sepolia
    "84532": {
        "name": "Base Sepolia",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://sepolia.basescan.org"
    },
    # Ethereum Sepolia
    "11155111": {
        "name": "Ethereum Sepolia",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://sepolia.etherscan.io"
    },
    # Arbitrum Sepolia
    "421614": {
        "name": "Arbitrum Sepolia",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://sepolia.arbiscan.io"
    },
    # Optimism Sepolia
    "11155420": {
        "name": "Optimism Sepolia",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://sepolia-optimism.etherscan.io"
    },
    # Base Mainnet
    "8453": {
        "name": "Base Mainnet",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://basescan.org"
    },
    # Ethereum Mainnet
    "1": {
        "name": "Ethereum Mainnet",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://etherscan.io"
    },
    # Arbitrum One
    "42161": {
        "name": "Arbitrum One",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://arbiscan.io"
    },
    # Optimism
    "10": {
        "name": "Optimism",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://optimistic.etherscan.io"
    },
    # Polygon Mumbai
    "80001": {
        "name": "Polygon Mumbai",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://mumbai.polygonscan.com"
    },
    # Polygon Mainnet
    "137": {
        "name": "Polygon",
        "contract_address": "0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2",
        "explorer_url": "https://polygonscan.com"
    }
}

DEFAULT_CHAIN_ID = "84532"  

###############################################################################
#                     CROSSCHAIN CONTRACT ABI
###############################################################################
"""
CROSSCHAIN_CONTRACT_ABI for the bridging contract. This includes crosschainMint,
crosschainBurn, deposit, withdraw, etc. 
"""

CROSSCHAIN_CONTRACT_ABI = [
    {
        "type": "constructor",
        "inputs": [
            {"name": "_aiAgent", "type": "address", "internalType": "address"},
            {"name": "_owner",   "type": "address", "internalType": "address"}
        ],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "aiAgent",
        "inputs": [],
        "outputs": [
            {"name": "", "type": "address", "internalType": "address"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "allowance",
        "inputs": [
            {"name": "owner",   "type": "address", "internalType": "address"},
            {"name": "spender", "type": "address", "internalType": "address"}
        ],
        "outputs": [
            {"name": "", "type": "uint256", "internalType": "uint256"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "approve",
        "inputs": [
            {"name": "spender", "type": "address", "internalType": "address"},
            {"name": "value",   "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [
            {"name": "", "type": "bool", "internalType": "bool"}
        ],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "balanceOf",
        "inputs": [
            {"name": "account", "type": "address", "internalType": "address"}
        ],
        "outputs": [
            {"name": "", "type": "uint256", "internalType": "uint256"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "crosschainBurn",
        "inputs": [
            {"name": "from",   "type": "address", "internalType": "address"},
            {"name": "amount", "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "crosschainMint",
        "inputs": [
            {"name": "to",     "type": "address", "internalType": "address"},
            {"name": "amount", "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "decimals",
        "inputs": [],
        "outputs": [
            {"name": "", "type": "uint8", "internalType": "uint8"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "deposit",
        "inputs": [],
        "outputs": [],
        "stateMutability": "payable"
    },
    {
        "type": "function",
        "name": "name",
        "inputs": [],
        "outputs": [
            {"name": "", "type": "string", "internalType": "string"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "owner",
        "inputs": [],
        "outputs": [
            {"name": "", "type": "address", "internalType": "address"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "renounceOwnership",
        "inputs": [],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "symbol",
        "inputs": [],
        "outputs": [
            {"name": "", "type": "string", "internalType": "string"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "totalSupply",
        "inputs": [],
        "outputs": [
            {"name": "", "type": "uint256", "internalType": "uint256"}
        ],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "transfer",
        "inputs": [
            {"name": "to",    "type": "address", "internalType": "address"},
            {"name": "value", "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [
            {"name": "", "type": "bool", "internalType": "bool"}
        ],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "transferFrom",
        "inputs": [
            {"name": "from",  "type": "address", "internalType": "address"},
            {"name": "to",    "type": "address", "internalType": "address"},
            {"name": "value", "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [
            {"name": "", "type": "bool", "internalType": "bool"}
        ],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "transferOwnership",
        "inputs": [
            {"name": "newOwner", "type": "address", "internalType": "address"}
        ],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "withdraw",
        "inputs": [
            {"name": "amount", "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [],
        "stateMutability": "nonpayable"
    }
]


###############################################################################
#                      GLOBALS / INITIAL STATE
###############################################################################


wallet_provider = None
current_chain_id = DEFAULT_CHAIN_ID
wallet_providers_cache = {}
agentkit = None

###############################################################################
#                    HELPER FUNCTIONS: CHAIN UTILS
###############################################################################
def get_contract_address():
    """Return the contract address for the current chain from SUPPORTED_CHAINS."""
    if current_chain_id in SUPPORTED_CHAINS:
        return SUPPORTED_CHAINS[current_chain_id]["contract_address"]
    raise ValueError(f"Chain ID {current_chain_id} not supported")

def get_chain_name():
    """Return the chain's human-readable name from SUPPORTED_CHAINS."""
    if current_chain_id in SUPPORTED_CHAINS:
        return SUPPORTED_CHAINS[current_chain_id]["name"]
    raise ValueError(f"Chain ID {current_chain_id} not supported")

def get_explorer_url():
    """Return the block explorer base URL for the current chain."""
    if current_chain_id in SUPPORTED_CHAINS:
        return SUPPORTED_CHAINS[current_chain_id]["explorer_url"]
    raise ValueError(f"Chain ID {current_chain_id} not supported")


###############################################################################
#                    HELPER: NETWORK SWITCHING
###############################################################################


def switch_network(new_chain_id: str) -> str:
    """
    switch_network(new_chain_id: str) -> str

    Switch the global chain to new_chain_id, re-initializing the wallet provider
    from wallet_data. Return a success or error string.
    """
    global current_chain_id, wallet_provider, agentkit, wallet_providers_cache

    if new_chain_id not in SUPPORTED_CHAINS:
        return f"Error: Chain ID {new_chain_id} not supported. Must be one of: {', '.join(SUPPORTED_CHAINS.keys())}"

    if new_chain_id == current_chain_id:
        return f"Already on {get_chain_name()} (Chain ID: {current_chain_id})"

    try:
        # Clear cached provider if we had one
        if new_chain_id in wallet_providers_cache:
            del wallet_providers_cache[new_chain_id]

        # Build a fresh CdpWalletProvider for new_chain_id:
        new_provider = get_cdp_wallet_provider_for_chain(new_chain_id)
        if not new_provider:
            return f"Error: Could not create a wallet provider for chain {new_chain_id}"

        # Check if the chain_id from new_provider matches:
        net = new_provider.get_network()
        if net.chain_id != new_chain_id:
            return f"Error: Provider chain mismatch. Expected {new_chain_id}, got {net.chain_id}"

        # Check if we can do a get_balance():
        try:
            native_balance = new_provider.get_balance()
            print(f"DEBUG: Native balance on chain {new_chain_id}: {native_balance}")
        except Exception as e:
            print(f"ERROR: Could not get balance for chain {new_chain_id}: {str(e)}")
            return f"Error connecting to {SUPPORTED_CHAINS[new_chain_id]['name']}: {str(e)}"

        # Switch globally:
        current_chain_id = new_chain_id
        wallet_provider = new_provider

        # Recreate agentkit with new provider:
        agentkit = AgentKit(
            AgentKitConfig(
                wallet_provider=wallet_provider,
                action_providers=[
                    cdp_api_action_provider(),
                    cdp_wallet_action_provider(),
                    erc20_action_provider(),
                    skywire_action_provider(),  # add skywire bridging
                    pyth_action_provider(),
                    wallet_action_provider(),
                    weth_action_provider(),
                    allora_action_provider(),
                ],
            )
        )
        # final check:
        actual_net = wallet_provider.get_network()
        print(f"DEBUG: switched to network with chain_id={actual_net.chain_id}")

        return f"Switched to {get_chain_name()} (Chain ID: {current_chain_id})"
    except Exception as e:
        return f"Error switching to chain {new_chain_id}: {str(e)}"


def get_cdp_wallet_provider_for_chain(chain_id: str) -> CdpWalletProvider:
    """
    get_cdp_wallet_provider_for_chain(chain_id: str) -> CdpWalletProvider

    Creates or retrieves from cache a CdpWalletProvider that is on the requested chain.
    We rely on wallet_data from wallet_data.txt and pass it into CdpWalletProviderConfig.
    If the chain ID doesn't match, we attempt to switch the provider's internal chain.

    This is the code path used by switch_network. If the user tries to do an operation
    on a chain we are not connected to, we can call switch_network first or
    the agent can do it automatically if it's in skywire_action_provider.
    """
    global wallet_providers_cache

    if chain_id in wallet_providers_cache:
        print(f"DEBUG: reusing cached wallet provider for chain_id={chain_id}")
        return wallet_providers_cache[chain_id]

    # Otherwise, load from wallet_data.txt:
    wallet_data = None
    if os.path.exists(wallet_data_file):
        with open(wallet_data_file, "r") as f:
            wallet_data = f.read()

    cdp_config = None
    if wallet_data is not None:
        cdp_config = CdpWalletProviderConfig(wallet_data=wallet_data)
    else:
        print("WARNING: No existing wallet_data.txt found; will start from empty config.")
        cdp_config = CdpWalletProviderConfig()

    # We set chain_id explicitly. The underlying code may need to confirm.
    cdp_config.default_chain_id = chain_id

    provider = CdpWalletProvider(cdp_config)

    # Let the provider do its network detection:
    net = provider.get_network()
    print(f"DEBUG: new CdpWalletProvider => chain_id={net.chain_id}, network_id={net.network_id or 'N/A'}")

    if net.chain_id != chain_id:
        
        print("WARNING: The CdpWalletProvider's chain_id doesn't match the requested chain.")
        

    # Store to cache
    wallet_providers_cache[chain_id] = provider

    # Also persist any updated wallet data so that if the provider was changed, we keep it.
    updated_data = provider.export_wallet().to_dict()
    with open(wallet_data_file, "w") as f:
        f.write(json.dumps(updated_data))

    return provider


###############################################################################
#             CONTRACT INVOCATION (CdpWalletProvider-based)
###############################################################################
def invoke_contract_function(
    provider: CdpWalletProvider,
    function_name: str,
    args: Optional[list] = None,
    value: Decimal = Decimal(0)
) -> Dict[str, Any]:
    """
    A generic function to do a write (transaction) to the bridging contract.
    For example, crosschainMint, crosschainBurn, deposit, withdraw, etc.

    We rely on the cdp_wallet_provider "read_contract" or "transact_contract"
    method to do this. We'll just do the approach used in your code to encode
    and send the TX, then wait for a receipt. Then we link an explorer URL.
    """
    try:
        net = provider.get_network()
        if net.chain_id != current_chain_id:
            return {"error": f"Chain mismatch: Wallet on chain {net.chain_id}, but global chain is {current_chain_id}"}

        if args is None:
            args = []

        contract_address = get_contract_address()

        print(f"DEBUG: calling {function_name} with args={args}, value={value} on chain {current_chain_id}")
        result = provider.transact_contract(
            contract_address=contract_address,
            abi=CROSSCHAIN_CONTRACT_ABI,
            function_name=function_name,
            args=args,
            value=int(value * Decimal(10**18)) if value > 0 else 0
        )
        tx_hash = result.tx_hash
        print(f"DEBUG: transaction hash: {tx_hash}")
        receipt = provider.wait_for_transaction_receipt(tx_hash)

        chain_name = get_chain_name()
        explorer_url = get_explorer_url()

        return {
            "tx_hash": tx_hash,
            "receipt": receipt,
            "chain_id": current_chain_id,
            "chain_name": chain_name,
            "explorer_url": f"{explorer_url}/tx/{tx_hash}"
        }
    except Exception as e:
        return {"error": str(e)}


def read_contract(
    provider: CdpWalletProvider,
    function_name: str,
    args: Optional[list] = None
) -> Dict[str, Any]:
    """
    read_contract(provider, function_name, args) -> dict with 'result' or 'error'.

    A read-only call to the bridging contract. E.g. read "balanceOf", "totalSupply", etc.
    """
    try:
        net = provider.get_network()
        if net.chain_id != current_chain_id:
            return {"error": f"Chain mismatch: provider on chain {net.chain_id}, global chain is {current_chain_id}"}

        if args is None:
            args = []

        contract_address = get_contract_address()
        print(f"DEBUG: reading function {function_name}, args={args} on chain {current_chain_id}")

        result = provider.read_contract(
            contract_address=contract_address,
            abi=CROSSCHAIN_CONTRACT_ABI,
            function_name=function_name,
            args=args
        )
        return {"result": result, "chain_id": current_chain_id, "chain_name": get_chain_name()}
    except Exception as e:
        return {"error": str(e)}


###############################################################################
#             CROSSCHAIN MINT / BURN, DEPOSIT, WITHDRAW
###############################################################################
def crosschain_mint(provider: CdpWalletProvider, to_address: str, amount: int) -> str:
    """Calls crosschainMint(to_address, amount). Must be recognized as aiAgent."""
    resp = invoke_contract_function(provider, "crosschainMint", [to_address, amount])
    if "error" in resp:
        return f"Error: {resp['error']}"
    return (
        f"Successfully minted {amount} tokens to {to_address} on {get_chain_name()}.\n"
        f"Transaction: {resp['explorer_url']}"
    )


def crosschain_burn(provider: CdpWalletProvider, from_address: str, amount: int) -> str:
    """Calls crosschainBurn(from_address, amount). Must be recognized as aiAgent."""
    resp = invoke_contract_function(provider, "crosschainBurn", [from_address, amount])
    if "error" in resp:
        return f"Error: {resp['error']}"
    return (
        f"Successfully burned {amount} tokens from {from_address} on {get_chain_name()}.\n"
        f"Transaction: {resp['explorer_url']}"
    )


def get_balance_of(provider: CdpWalletProvider, address: str) -> str:
    """Reads balanceOf(address). Returns a user-facing string or an error message."""
    r = read_contract(provider, "balanceOf", [address])
    if "error" in r:
        return f"Error: {r['error']}"
    return f"Balance of {address} on {get_chain_name()}: {r['result']} tokens"


def deposit_native_eth(provider: CdpWalletProvider, eth_amount: float) -> str:
    """Calls deposit() with a payable value. That mints sETH for the user."""
    val = Decimal(str(eth_amount))
    resp = invoke_contract_function(provider, "deposit", [], val)
    if "error" in resp:
        return f"Error: {resp['error']}"

    return (
        f"Successfully deposited {eth_amount} ETH on {get_chain_name()}.\n"
        f"Transaction: {resp['explorer_url']}"
    )


def withdraw_tokens(provider: CdpWalletProvider, amount: int) -> str:
    """Calls withdraw(amount). Burns user's sETH, returns that many native ETH."""
    resp = invoke_contract_function(provider, "withdraw", [amount])
    if "error" in resp:
        return f"Error: {resp['error']}"
    return (
        f"Successfully withdrew {amount} tokens on {get_chain_name()}.\n"
        f"Transaction: {resp['explorer_url']}"
    )




def parse_mint_args(input_str: str) -> str:
    parts = input_str.strip().split()
    if len(parts) != 2:
        return "Error: Must provide 'TO_ADDRESS AMOUNT'"
    to_addr, amt_str = parts
    if not to_addr.startswith("0x"):
        return "Error: address must start with 0x"
    try:
        amount_int = int(amt_str)
    except:
        return "Error: amount must be integer"
    return crosschain_mint(wallet_provider, to_addr, amount_int)

def parse_burn_args(input_str: str) -> str:
    parts = input_str.strip().split()
    if len(parts) != 2:
        return "Error: Must provide 'FROM_ADDRESS AMOUNT'"
    from_addr, amt_str = parts
    if not from_addr.startswith("0x"):
        return "Error: address must start with 0x"
    try:
        amount_int = int(amt_str)
    except:
        return "Error: amount must be integer"
    return crosschain_burn(wallet_provider, from_addr, amount_int)

def parse_balance_of_args(input_str: str) -> str:
    addr = input_str.strip()
    if not addr.startswith("0x"):
        return "Error: Provide a valid address that starts with 0x"

    try:
        # Show local wallet's native balance too:
        local_balance = wallet_provider.get_balance()
        chainname = get_chain_name()
        # Also get the token balance of the user-supplied address:
        tok_str = get_balance_of(wallet_provider, addr)
        return (
            f"My wallet native balance on {chainname}: {local_balance} wei\n"
            f"{tok_str}"
        )
    except Exception as e:
        return f"Error reading balance: {str(e)}"

def parse_deposit_eth_args(input_str: str) -> str:
    amt_str = input_str.strip()
    try:
        amt_float = float(amt_str)
    except:
        return "Error: Provide a valid float (e.g. 0.01)"

    return deposit_native_eth(wallet_provider, amt_float)

def parse_withdraw_args(input_str: str) -> str:
    amt_str = input_str.strip()
    try:
        amt_int = int(amt_str)
    except:
        return "Error: Provide a valid integer"
    return withdraw_tokens(wallet_provider, amt_int)

def parse_switch_network_args(input_str: str) -> str:
    chain_id = input_str.strip()
    if not chain_id:
        # List current chain and supported networks:
        net = wallet_provider.get_network()
        actual_chain_id = net.chain_id
        listing = "\n".join([f"{cid}: {info['name']}" for cid, info in SUPPORTED_CHAINS.items()])
        return (
            f"Currently in global state: {get_chain_name()} (Chain ID: {current_chain_id})\n"
            f"Provider actual chain_id: {actual_chain_id}\n\n"
            f"Supported networks:\n{listing}"
        )

    ans = switch_network(chain_id)
    # Possibly re-init tools
    global agentkit
    if agentkit:
        get_langchain_tools(agentkit)
    return ans

def parse_get_current_network(input_str: str) -> str:
    net = wallet_provider.get_network()
    if net.chain_id != current_chain_id:
        return (
            f"WARNING: mismatch. Global chain_id={current_chain_id}, provider chain_id={net.chain_id}\n"
            f"Current chain name: {get_chain_name()}"
        )
    return f"Current network: {get_chain_name()} (Chain ID={current_chain_id})"

def verify_all_chains() -> str:
    """
    Attempt connecting to each chain in SUPPORTED_CHAINS with a fresh
    CdpWalletProvider, check the wallet's native balance, then show success/failure.
    """
    lines = []
    lines.append(f"Current chain in global state: {get_chain_name()} (ID={current_chain_id})")

    for chain_id, info in SUPPORTED_CHAINS.items():
        try:
            # create new provider
            prov = get_cdp_wallet_provider_for_chain(chain_id)
            net = prov.get_network()
            # check balance
            bal = prov.get_balance()
            lines.append(f"✅ {info['name']} (Chain {chain_id}): got balance {bal} wei")
        except Exception as e:
            lines.append(f"❌ {info['name']} (Chain {chain_id}): {str(e)}")

    return "\n".join(lines)

def parse_verify_chains(input_str: str) -> str:
    return verify_all_chains()


###############################################################################
#                      INITIALIZE THE AGENT
###############################################################################
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
    else:
        print("No existing wallet_data.txt found. We'll create new wallet data.")
        cdp_config = CdpWalletProviderConfig()

    # Build provider
    global wallet_provider
    wallet_provider = CdpWalletProvider(cdp_config)
    
    # Immediately persist updated data
    with open(wallet_data_file, "w") as f:
        new_data = wallet_provider.export_wallet().to_dict()
        f.write(json.dumps(new_data))

    net = wallet_provider.get_network()
    print(f"DEBUG: loaded wallet data. chain_id={net.chain_id}")

    global current_chain_id
    if net.chain_id != current_chain_id:
        print(f"WARNING: provider chain_id={net.chain_id} doesn't match global={current_chain_id}")

    # Build the agentkit
    global agentkit
    agentkit = AgentKit(
        AgentKitConfig(
            wallet_provider=wallet_provider,
            action_providers=[
                cdp_api_action_provider(),
                cdp_wallet_action_provider(),
                erc20_action_provider(),
                skywire_action_provider(),  # bridging
                pyth_action_provider(),
                wallet_action_provider(),
                weth_action_provider(),
                allora_action_provider(),
            ],
        )
    )

    # Get Langchain tools
    tools = get_langchain_tools(agentkit)

    # Add custom tools for bridging / network ops
    custom_tools = [
        Tool(
            name="crosschain_mint",
            description="Crosschain-mint tokens to an address. Input: 'TO_ADDRESS AMOUNT'",
            func=parse_mint_args
        ),
        Tool(
            name="crosschain_burn",
            description="Crosschain-burn tokens from an address. Input: 'FROM_ADDRESS AMOUNT'",
            func=parse_burn_args
        ),
        Tool(
            name="balance_of",
            description="Check sETH balance of an address. Input: 'ADDRESS'",
            func=parse_balance_of_args
        ),
        Tool(
            name="deposit_eth",
            description="Deposit native ETH => sETH. Input: '0.01' etc.",
            func=parse_deposit_eth_args
        ),
        Tool(
            name="withdraw",
            description="Withdraw sETH => native ETH. Input: '100' (uint256).",
            func=parse_withdraw_args
        ),
        Tool(
            name="switch_network",
            description="Switch chains. Provide chain_id or none for help. Ex: '11155420'",
            func=parse_switch_network_args
        ),
        Tool(
            name="get_current_network",
            description="Show the current network and chain ID in global state & provider.",
            func=parse_get_current_network
        ),
        Tool(
            name="verify_chains",
            description="Check connectivity to all chains in SUPPORTED_CHAINS",
            func=parse_verify_chains
        )
    ]

    # Combine with standard agentkit tools
    tools.extend(custom_tools)

    # Store buffered conversation history in memory
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "CDP-based bridging chatbot"}}

    # Create ReAct Agent with enhanced system message for crosschain operations
    agent = create_react_agent(
        llm,
        tools,
        state_modifier=(
            "You are an advanced AI agent with a CdpWalletProvider using wallet_data.txt for chain states. "
            "You can bridge sETH via crosschainBurn / crosschainMint. "
            "You also can deposit or withdraw ETH => sETH. Provide block explorer links. "
            "If bridging, do crosschainBurn on source chain, then switch to destination chain, do crosschainMint. "
            "If user wants to see sETH balances, use the 'balance_of' tool. If user wants to deposit, call 'deposit_eth'. "
            "If user wants to switch networks, call 'switch_network'. If user calls 'verify_chains', you test them all."
        ),
        checkpointer=memory,
    )
    
    return agent, config


###############################################################################
#               AUTONOMOUS & INTERACTIVE MODES
###############################################################################
def run_autonomous_mode(agent_executor, config, interval=10):
    """
    Repeatedly sends bridging or chain-check prompts to the agent.
    """
    print("Starting autonomous mode. Press Ctrl+C to stop.")
    # Some sample prompts:
    prompts = [
        "Verify all chains to ensure my wallet is recognized on each.",
        "Crosschain-burn 0.01 sETH from my address on Base Sepolia, then crosschain-mint 0.01 sETH on Optimism Sepolia to same address. Then show final balances.",
        "Switch to Ethereum Sepolia and show me my native ETH balance. Then switch back to Base Sepolia. Then deposit 0.001 ETH => sETH.",
        "Withdraw 50 sETH from my address. Then bridging 25 from Base to Optimism. Then check final sETH. If insufficient, show error."
    ]
    idx = 0

    while True:
        try:
            prompt = prompts[idx % len(prompts)]
            idx += 1

            print(f"\n[Autonomous prompt] {prompt}\n")
            for chunk in agent_executor.stream({"messages": [HumanMessage(content=prompt)]}, config):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

            time.sleep(interval)
        except KeyboardInterrupt:
            print("Exiting autonomous mode via KeyboardInterrupt.")
            sys.exit(0)
        except Exception as e:
            print(f"Error in autonomous mode: {e}")
            time.sleep(2)

def run_chat_mode(agent_executor, config):
    """
    Interactive REPL for the user to type commands like
    'switch_network 11155420' or 'balance_of 0xABC...' or 'deposit_eth 0.01'
    """
    print("Starting chat mode... Type 'exit' to quit.")
    while True:
        try:
            user_input = input("\nPrompt: ")
            if user_input.lower() == "exit":
                break

            for chunk in agent_executor.stream({"messages": [HumanMessage(content=user_input)]}, config):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")
        except KeyboardInterrupt:
            print("Exiting chat mode via KeyboardInterrupt.")
            break
        except Exception as e:
            print(f"Error in chat mode: {e}")
            time.sleep(1)


###############################################################################
#            MODE SELECTION
###############################################################################
def choose_mode():
    """
    Let user pick 'chat' or 'auto'.
    """
    while True:
        print("Modes:\n1) chat\n2) auto")
        choice = input("Enter choice: ").strip().lower()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid, please choose 1 or 2.")


def main():
    """Initialize the agent, then let the user pick chat or auto mode."""
    agent_executor, config = initialize_agent()

    mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor, config)
    else:
        run_autonomous_mode(agent_executor, config, interval=12)


if __name__ == "__main__":
    print("Starting the bridging chatbot with CDP wallet_data approach (~1000 lines).")
    main()
