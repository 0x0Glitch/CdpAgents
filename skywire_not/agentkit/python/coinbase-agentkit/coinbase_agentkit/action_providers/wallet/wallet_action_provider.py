"""Wallet action provider for basic wallet operations."""

from typing import Any, Dict, List, Optional, Union

from web3 import Web3

from ...network import Network
from ...wallet_providers.wallet_provider import WalletProvider
from ..action_decorator import create_action
from ..action_provider import ActionProvider
from .schemas import CallContractSchema, GetBalanceSchema, GetWalletDetailsSchema, NativeTransferSchema, SwitchNetworkSchema


class WalletActionProvider(ActionProvider[WalletProvider]):
    """Action provider for wallet-related actions."""
    
    def __init__(self):
        """Initialize the wallet action provider."""
        # Initialize with empty list of action_providers as required by base class
        super().__init__(name="wallet", action_providers=[])

    @create_action(
        name="get_wallet_details",
        description="Get wallet account and network details",
        schema=GetWalletDetailsSchema,
    )
    def get_wallet_details(self, wallet_provider: WalletProvider, args: dict[str, Any]) -> str:
        """Get wallet account and network details.

        Args:
            wallet_provider (WalletProvider): The wallet provider to get details for.
            args (dict[str, Any]): Arguments for the action.

        Returns:
            str: Formatted message with wallet account and network details.

        """
        try:
            address = wallet_provider.get_address()
            network = wallet_provider.get_network()
            balance_wei = wallet_provider.get_balance()
            formatted_balance = str(balance_wei)

            return f"""Wallet Details:
- Provider: {wallet_provider.get_name() if hasattr(wallet_provider, 'get_name') else type(wallet_provider).__name__.lower()}
- Address: {address}
- Network:
  * Protocol Family: {network.protocol_family}
  * Network ID: {network.network_id}
  * Chain ID: {network.chain_id}
- Native Balance: {formatted_balance}"""
        except Exception as e:
            return f"Error getting wallet details: {e}"

    @create_action(
        name="get_balance",
        description="Get native currency balance",
        schema=GetBalanceSchema,
    )
    def get_balance(self, wallet_provider: WalletProvider, args: dict[str, Any]) -> str:
        """Get native currency balance.

        Args:
            wallet_provider (WalletProvider): The wallet provider to get balance for.
            args (dict[str, Any]): Arguments for the action.

        Returns:
            str: Formatted message with the wallet balance.

        """
        try:
            balance_wei = wallet_provider.get_balance()
            
            # If args contains an asset parameter, try to get that asset's balance if supported
            asset = args.get("asset")
            network = args.get("network")
            
            if network and hasattr(wallet_provider, 'switch_network') and network != wallet_provider.current_network_id:
                # If a different network is specified and wallet provider supports switching
                return f"Please use the switch_network action to change to {network} before checking balance."
            
            if asset and asset.lower() != "eth" and hasattr(wallet_provider, 'get_balance'):
                try:
                    # Try to get balance of specific asset if provider supports it
                    if hasattr(wallet_provider, 'get_token_balance'):
                        token_balance = wallet_provider.get_token_balance(asset)
                        return f"Balance of {asset}: {token_balance}"
                except Exception:
                    pass  # Fall back to native balance if token balance fails
            
            # Convert balance to readable format
            balance_eth = Web3.fromWei(balance_wei, "ether") if hasattr(Web3, 'fromWei') else balance_wei / 10**18
            
            network = wallet_provider.get_network()
            return f"Balance on {network.network_id}: {balance_eth} ETH"
        except Exception as e:
            return f"Error getting balance: {e}"

    @create_action(
        name="native_transfer",
        description="""
This tool will transfer native currency from your wallet to a destination address.

It takes the following arguments:
- to: The destination address to transfer to (e.g. '0x5154eae861cac3aa757d6016babaf972341354cf')
- value: The amount to transfer in whole units (e.g. '1.5' for 1.5 ETH)

Important notes:
- Make sure you have enough balance to cover the transfer amount plus gas fees
- Double check the destination address to avoid losing funds
""",
        schema=NativeTransferSchema,
    )
    def native_transfer(self, wallet_provider: WalletProvider, args: dict[str, Any]) -> str:
        """Transfer native tokens from the connected wallet to a destination address.

        Args:
            wallet_provider (WalletProvider): The wallet provider to transfer tokens from.
            args (dict[str, Any]): Arguments containing destination address and transfer amount.

        Returns:
            str: A message indicating if the transfer was successful or not.

        """
        try:
            to_address = args["to"]
            value = args["value"]
            
            # Handle network switch if specified in the args
            network = args.get("network")
            if network and hasattr(wallet_provider, 'current_network_id') and network != wallet_provider.current_network_id:
                # If a different network is specified and wallet provider supports switching
                return f"Please use the switch_network action to change to {network} before transferring funds."
            
            tx_hash = wallet_provider.native_transfer(to_address, value)
            return f"Successfully transferred {value} ETH to {to_address}. Transaction hash: {tx_hash}"
        except Exception as e:
            return f"Error transferring tokens: {e}"

    @create_action(
        name="switch_network",
        description="""
This tool will switch the wallet to a different network.

It takes the following input:
- network_id: The ID of the network to switch to (e.g., 'base-sepolia', 'optimism-sepolia', 'zora', 'unichain')

Important notes:
- The network must be supported by the wallet provider
- This will change the network context for all subsequent operations
""",
        schema=SwitchNetworkSchema,
    )
    def switch_network(self, wallet_provider: WalletProvider, args: dict[str, Any]) -> str:
        """Switch the wallet to a different network.

        Args:
            wallet_provider (WalletProvider): The wallet provider to switch networks for.
            args (dict[str, Any]): Arguments containing the target network_id.

        Returns:
            str: A message indicating if the network switch was successful or not.

        """
        try:
            network_id = args["network_id"]
            
            # Check if the wallet provider supports network switching
            if not hasattr(wallet_provider, "switch_network"):
                return "This wallet provider does not support network switching."
            
            # Check if we're already on this network
            if hasattr(wallet_provider, "current_network_id") and wallet_provider.current_network_id == network_id:
                return f"Already on network {network_id}, no need to switch."
            
            # Attempt to switch networks
            success = wallet_provider.switch_network(network_id)
            
            if success:
                network = wallet_provider.get_network()
                return f"Successfully switched to network {network_id} (Chain ID: {network.chain_id})"
            else:
                return f"Failed to switch to network {network_id}"
        except Exception as e:
            return f"Error switching networks: {e}"

    @create_action(
        name="call_contract",
        description="""
This tool will call a smart contract function on the blockchain.

It takes the following input:
- contract_address: The address of the smart contract
- abi: The ABI (Application Binary Interface) of the contract function
- function_name: The name of the function to call
- inputs: (Optional) Arguments for the function, can be an object or array
- network: (Optional) Network ID to use for the call (will prompt for switch if needed)

Important notes:
- For read-only functions, the result will be returned immediately
- For state-changing functions, a transaction will be submitted
""",
        schema=CallContractSchema,
    )
    def call_contract(self, wallet_provider: WalletProvider, args: dict[str, Any]) -> str:
        """Call a contract function on the specified blockchain network.

        Args:
            wallet_provider (WalletProvider): The wallet provider to use for the contract call.
            args (dict[str, Any]): Arguments containing contract address, ABI, function name, and inputs.

        Returns:
            str: Result of the contract call or transaction hash for state-changing functions.
        """
        try:
            contract_address = Web3.to_checksum_address(args["contract_address"])
            abi = args["abi"]
            function_name = args["function_name"]
            inputs = args.get("inputs", None)
            network = args.get("network", None)
            
            # Handle network switch if specified in the args
            if network and hasattr(wallet_provider, 'current_network_id') and network != wallet_provider.current_network_id:
                return f"Please use the switch_network action to change to {network} before calling the contract."
            
            # Check if the wallet provider supports contract calls directly
            if hasattr(wallet_provider, 'call_contract'):
                result = wallet_provider.call_contract(
                    contract_address=contract_address,
                    abi=abi,
                    function_name=function_name,
                    inputs=inputs
                )
                return f"Contract call result: {result}"
            
            # Otherwise, use Web3 for the contract call
            if not hasattr(wallet_provider, 'web3'):
                return "This wallet provider does not support contract calls directly."
                
            web3 = wallet_provider.web3
            contract = web3.eth.contract(address=contract_address, abi=abi)
            
            # Prepare arguments based on the input format
            args_list = []
            if inputs:
                if isinstance(inputs, dict):
                    # Find the function ABI to determine the argument order
                    func_abi = next((f for f in abi if f.get("name") == function_name), None)
                    if func_abi and func_abi.get("inputs"):
                        arg_names = [inp["name"] for inp in func_abi["inputs"]]
                        args_list = [inputs.get(name) for name in arg_names if name in inputs]
                    else:
                        # If we can't determine the order, just use the values (less safe)
                        args_list = list(inputs.values())
                elif isinstance(inputs, list):
                    args_list = inputs
            
            # Get the function from the contract
            contract_func = contract.functions[function_name]
            func = contract_func(*args_list)
            
            # Determine if this is a view/pure function or state-changing
            func_abi = next((f for f in abi if f.get("name") == function_name), None)
            is_view = func_abi and func_abi.get("stateMutability") in ("view", "pure")
            
            if is_view:
                # For view functions, just call and return the result
                result = func.call()
                return f"Contract call result: {result}"
            else:
                # For state-changing functions, build and send a transaction
                tx_params = {
                    "from": wallet_provider.get_address(),
                    "gasPrice": web3.eth.gas_price,
                    "nonce": web3.eth.get_transaction_count(wallet_provider.get_address()),
                }
                
                # If the function is payable and value is provided
                if func_abi and func_abi.get("stateMutability") == "payable" and isinstance(inputs, dict) and "value" in inputs:
                    tx_params["value"] = Web3.toWei(inputs["value"], "ether")
                
                # Estimate gas (with 20% buffer for safety)
                try:
                    estimated_gas = func.estimateGas(tx_params)
                    tx_params["gas"] = int(estimated_gas * 1.2)
                except Exception as gas_error:
                    return f"Gas estimation failed: {gas_error}"
                
                # Send the transaction
                signed_tx = wallet_provider.sign_transaction(func.buildTransaction(tx_params))
                tx_hash = web3.eth.send_raw_transaction(signed_tx)
                return f"Transaction sent: {tx_hash.hex()}"
        except Exception as e:
            return f"Error calling contract: {e}"

    def supports_network(self, network: Network) -> bool:
        """Check if network is supported by wallet actions.

        Most wallet providers support common wallet actions like getting balances and transferring.

        Args:
            network (Network): The network to check.

        Returns:
            bool: Whether the network is supported by this action provider.

        """
        # Wallet actions are generally available on all networks
        return True


def wallet_action_provider() -> WalletActionProvider:
    """Create a new WalletActionProvider instance.

    Returns:
        WalletActionProvider: A new wallet action provider instance.

    """
    return WalletActionProvider()
