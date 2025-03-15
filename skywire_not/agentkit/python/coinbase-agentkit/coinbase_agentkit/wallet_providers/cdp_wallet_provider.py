"""CDP Wallet provider."""

import json
import os
import logging
from decimal import Decimal
from typing import Any, Dict, Optional, Union

from cdp import (
    Cdp,
    ExternalAddress,
    MnemonicSeedPhrase,
    Wallet,
    WalletData,
    hash_message,
    hash_typed_data_message,
)
from eth_account.typed_transactions import DynamicFeeTransaction
from pydantic import BaseModel, Field
from web3 import Web3, HTTPProvider
from web3.types import BlockIdentifier, ChecksumAddress, HexStr, TxParams

from ..__version__ import __version__
from ..network import Network
from .evm_wallet_provider import EvmGasConfig, EvmWalletProvider
from .wallet_provider import WalletProvider

logger = logging.getLogger(__name__)

# Default RPC endpoints for known networks (for Web3 connectivity)
DEFAULT_RPC_ENDPOINTS = {
    "base-sepolia": "https://base-sepolia.g.alchemy.com/v2/d40IDFW5NaYldNIOSb_vuJBNF5sm1WR7",        # Base Sepolia testnet RPC
    "optimism-sepolia": "https://opt-sepolia.g.alchemy.com/v2/d40IDFW5NaYldNIOSb_vuJBNF5sm1WR7", # Optimism Sepolia testnet RPC
    "ethereum-sepolia": "https://eth-sepolia.g.alchemy.com/v2/d40IDFW5NaYldNIOSb_vuJBNF5sm1WR7",  # Example Ethereum Sepolia RPC
    "zora": "https://zora-sepolia.g.alchemy.com/v2/d40IDFW5NaYldNIOSb_vuJBNF5sm1WR7",           # Zora testnet
    "unichain": "https://unichain-sepolia.g.alchemy.com/v2/d40IDFW5NaYldNIOSb_vuJBNF5sm1WR7"          # Unichain testnet
}

# Chain IDs for known networks
NETWORK_ID_TO_CHAIN = {
    "ethereum-mainnet": 1,
    "ethereum-sepolia": 11155111,
    "optimism": 10,
    "optimism-sepolia": 11155420,
    "base": 8453,
    "base-sepolia": 84532,
    "polygon": 137,
    "polygon-amoy": 80002,
    "avalanche": 43114,
    "zora": 7777777,
    "zora-sepolia": 999,
    "unichain": 88
}

# Network names
NETWORK_ID_TO_CHAIN_NAME = {
    "ethereum-mainnet": "Ethereum Mainnet",
    "ethereum-sepolia": "Ethereum Sepolia",
    "optimism": "Optimism",
    "optimism-sepolia": "Optimism Sepolia",
    "base": "Base",
    "base-sepolia": "Base Sepolia",
    "polygon": "Polygon",
    "polygon-amoy": "Polygon Amoy",
    "avalanche": "Avalanche",
    "zora": "Zora",
    "zora-sepolia": "Zora Sepolia",
    "unichain": "Unichain"
}

class CdpProviderConfig(BaseModel):
    """Configuration options for CDP providers."""

    api_key_name: str | None = Field(None, description="The CDP API key name")
    api_key_private_key: str | None = Field(None, description="The CDP API private key")


class CdpWalletProviderConfig(CdpProviderConfig):
    """Configuration options for CDP wallet provider."""

    network_id: str | None = Field(None, description="The network id")
    mnemonic_phrase: str | None = Field(None, description="The mnemonic phrase of the wallet")
    wallet_data: str | None = Field(None, description="The data of the CDP Wallet as a JSON string")
    gas: EvmGasConfig | None = Field(None, description="Gas configuration settings")


class CdpWalletProvider(WalletProvider):
    """WalletProvider implementation that uses Coinbase Developer Platform.

    Args:
        config (Optional[CdpWalletProviderConfig], optional): Configuration for the wallet provider. Defaults to None.
        provider_args (Optional[Dict[str, Any]], optional): Args to pass to the provider. Defaults to None.

    """

    def __init__(
        self, config: Optional[CdpWalletProviderConfig] = None, provider_args: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize CDP wallet provider.

        Args:
            config (Optional[CdpWalletProviderConfig], optional): Configuration for the wallet provider. Defaults to None.
            provider_args (Optional[Dict[str, Any]], optional): Args to pass to the provider. Defaults to None.

        """
        super().__init__()
        
        # Parse config
        if not config:
            config = CdpWalletProviderConfig()
            
        # Set up CDP provider
        self._provider_args = provider_args or {}
        
        # Get API credentials from environment if not provided
        api_key_name = os.getenv("CDP_API_KEY_NAME")
        api_key_private_key = os.getenv("CDP_API_KEY_PRIVATE_KEY")
        
        # Initialize network
        self.current_network_id = config.network_id or os.getenv("NETWORK_ID", "base-sepolia")
        
        # Initialize private key for direct wallet operations (alternative to CDP)
        private_key = os.getenv("PRIVATE_KEY")
        
        # Initialize CDP client
        try:
            self._provider = Cdp()
            
            # Use private key for wallet if available
            if private_key:
                # Use direct Web3 wallet with private key
                self._wallet = None
                self.account = Web3().eth.account.from_key(private_key)
                logger.info(f"Initialized wallet using private key")
            else:
                # Create a new wallet using CDP
                try:
                    self._wallet = self._provider.get_wallet(self.current_network_id)
                    logger.info(f"Initialized CDP wallet for {self.current_network_id}")
                except Exception as wallet_error:
                    logger.error(f"Failed to get CDP wallet: {wallet_error}")
                    # Check again for private key as fallback
                    if private_key:
                        self._wallet = None
                        self.account = Web3().eth.account.from_key(private_key)
                        logger.info(f"Initialized wallet using private key (fallback)")
                    else:
                        raise ValueError("No wallet could be initialized. Please add a PRIVATE_KEY to your .env file.")
            
            # Get Web3 instance for the current network
            rpc_url = DEFAULT_RPC_ENDPOINTS.get(self.current_network_id)
            self.web3 = Web3(HTTPProvider(rpc_url)) if rpc_url else None
            
            # Configure Web3 for POA networks if applicable - using alternative approach
            if self.web3:
                from web3.exceptions import ExtraDataLengthError
                try:
                    # Try to get the latest block to check if it works
                    self.web3.eth.get_block('latest')
                except ExtraDataLengthError:
                    # Add support for POA chains manually if needed
                    from web3.middleware.formatting import construct_formatting_middleware
                    poa_middleware = construct_formatting_middleware(
                        request_formatters={
                            'eth_sendTransaction': apply_gas_price,
                            'eth_estimateGas': apply_gas_price
                        }
                    )
                    self.web3.middleware_onion.add(poa_middleware)
                    logger.info("Added POA middleware for compatibility")
                
            # Cache for wallets and web3 instances per network to enable quick switching
            if self._wallet:
                self._wallets = {self.current_network_id: self._wallet}
            else:
                self._wallets = {}
            
            self._web3_clients = {self.current_network_id: self.web3}
            
            logger.info(f"CdpWalletProvider initialized with network: {self.current_network_id}")
            
        except Exception as e:
            logger.error(f"Error initializing CdpWalletProvider: {e}")
            raise

    def get_network(self) -> Network:
        """Get the network.

        Returns:
            Network: Current wallet network.

        """
        if self.current_network_id not in NETWORK_ID_TO_CHAIN:
            raise ValueError(f"Network {self.current_network_id} is not supported")

        # Convert chain_id to string to avoid validation errors
        chain_id = NETWORK_ID_TO_CHAIN[self.current_network_id]
        return Network(
            protocol_family="evm",
            network_id=self.current_network_id,
            chain_id=str(chain_id),  # Convert to string to avoid validation errors
            chain_name=NETWORK_ID_TO_CHAIN_NAME[self.current_network_id],
        )

    def get_address(self) -> str:
        """Get the wallet address.

        Returns:
            str: Wallet address.

        """
        if hasattr(self, 'account'):
            return self.account.address
        elif self._wallet:
            return self._wallet.default_address.lower()
        else:
            raise ValueError("No wallet is initialized")

    def request_funds(self, amount: int = 1) -> Dict[str, Any]:
        """Request funds from the CDP test faucet.

        Args:
            amount (int, optional): Amount in ETH. Defaults to 1.

        Returns:
            Dict[str, Any]: Result of the request.

        """
        if self.current_network_id != "base-sepolia":
            logger.warning(
                f"Requesting funds on {self.current_network_id}, which may not have a faucet. Consider requesting on 'base-sepolia'."
            )
        return self._wallet.request_funds(amount)

    def get_balance(self) -> int:
        """Get the balance of the wallet.

        Returns:
            int: Balance in wei.
        """
        try:
            if self.web3 is None:
                logger.warning("Web3 client not initialized, attempting to initialize")
                # Reinitialize web3 if it's not set
                rpc_url = DEFAULT_RPC_ENDPOINTS.get(self.current_network_id)
                if rpc_url:
                    self.web3 = Web3(HTTPProvider(rpc_url))
                    # Configure Web3 for POA networks if applicable
                    try:
                        # Test if we can get the latest block
                        self.web3.eth.get_block('latest')
                    except Exception as e:
                        logger.warning(f"Error accessing blockchain, configuring for POA: {e}")
                        # Add support for POA chains manually if needed
                        from web3.middleware.formatting import construct_formatting_middleware
                        poa_middleware = construct_formatting_middleware(
                            request_formatters={
                                'eth_sendTransaction': apply_gas_price,
                                'eth_estimateGas': apply_gas_price
                            }
                        )
                        self.web3.middleware_onion.add(poa_middleware)
                        logger.info("Added POA middleware for compatibility")
                else:
                    logger.error(f"No RPC URL found for network {self.current_network_id}")
                    return 0

            if hasattr(self, 'account'):
                address = self.account.address
            elif self._wallet:
                address = self._wallet.address
            else:
                logger.error("No wallet address available")
                return 0

            return self.web3.eth.get_balance(Web3.to_checksum_address(address))
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0
            
    def transfer_native(self, to: str, amount: int) -> str:
        """Transfer native tokens.

        Args:
            to (str): Recipient address.
            amount (int): Amount in wei.

        Returns:
            str: Transaction hash.
        """
        try:
            if self.web3 is None:
                logger.warning("Web3 client not initialized, attempting to initialize")
                # Reinitialize web3 if it's not set
                rpc_url = DEFAULT_RPC_ENDPOINTS.get(self.current_network_id)
                if rpc_url:
                    self.web3 = Web3(HTTPProvider(rpc_url))
                    # Configure Web3 for POA networks if applicable
                    try:
                        # Test if we can get the latest block
                        self.web3.eth.get_block('latest')
                    except Exception as e:
                        logger.warning(f"Error accessing blockchain, configuring for POA: {e}")
                        # Add support for POA chains manually if needed
                        from web3.middleware.formatting import construct_formatting_middleware
                        poa_middleware = construct_formatting_middleware(
                            request_formatters={
                                'eth_sendTransaction': apply_gas_price,
                                'eth_estimateGas': apply_gas_price
                            }
                        )
                        self.web3.middleware_onion.add(poa_middleware)
                        logger.info("Added POA middleware for compatibility")
                else:
                    logger.error(f"No RPC URL found for network {self.current_network_id}")
                    raise Exception(f"No RPC URL found for network {self.current_network_id}")

            # Check if using direct private key wallet
            if hasattr(self, 'account'):
                from_address = Web3.to_checksum_address(self.account.address)
                nonce = self.web3.eth.get_transaction_count(Web3.to_checksum_address(from_address))
                
                # Build the transaction
                gas_price = self.web3.eth.gas_price
                chain_id = self.get_chain_id()
                
                tx = {
                    'nonce': nonce,
                    'to': Web3.to_checksum_address(to),
                    'value': amount,
                    'gas': 21000,  # Standard gas limit for simple ETH transfers
                    'gasPrice': gas_price,
                    'chainId': chain_id
                }
                
                # Sign and send transaction
                signed_tx = self.account.sign_transaction(tx)
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                
                return tx_hash.hex()
            elif self._wallet:
                # Using CDP wallet
                return self._wallet.transfer_eth(to, amount).transaction_hash
            else:
                raise Exception("No wallet initialized")
        except Exception as e:
            logger.error(f"Error during native transfer: {e}")
            raise Exception(f"Error during native transfer: {e}")

    def native_transfer(self, to: str, value: Union[int, str]) -> str:
        """Transfer ETH.

        Args:
            to (str): Address to transfer to.
            value (Union[int, str]): Amount to transfer. Either wei value as int or ETH value as str (e.g. "0.1").

        Returns:
            str: Tx hash of the transfer.

        """
        # Convert value to wei if it's a string (ETH amount)
        wei_value = value if isinstance(value, int) else Web3.to_wei(float(value), "ether")
        
        # Use the transfer_native method
        return self.transfer_native(to, wei_value)

    def get_chain_id(self) -> int:
        """Get the current chain ID.

        Returns:
            int: The chain ID of the current network.
        """
        if self.current_network_id not in NETWORK_ID_TO_CHAIN:
            raise ValueError(f"Network {self.current_network_id} is not supported")
            
        return NETWORK_ID_TO_CHAIN[self.current_network_id]

    def get_name(self) -> str:
        """Get the name of the wallet provider.
        
        Returns:
            str: The name of the wallet provider.
        """
        return "Coinbase CDP Wallet"

    def switch_network(self, network_id: str) -> bool:
        """Switch to a different network.
        
        Args:
            network_id (str): Network ID to switch to.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.current_network_id == network_id:
            logger.info(f"Already on network {network_id}")
            return True
            
        try:
            # Check if the network is supported
            if network_id not in DEFAULT_RPC_ENDPOINTS:
                logger.error(f"Network {network_id} is not supported")
                return False
                
            logger.info(f"Switching from {self.current_network_id} to {network_id}")
            
            # Get or create Web3 instance for the new network
            if network_id in self._web3_clients:
                # Use cached Web3 instance
                new_web3 = self._web3_clients[network_id]
                logger.info(f"Using cached Web3 instance for {network_id}")
            else:
                # Create a new Web3 instance
                rpc_url = DEFAULT_RPC_ENDPOINTS.get(network_id)
                if not rpc_url:
                    logger.error(f"No RPC URL found for network {network_id}")
                    return False
                    
                new_web3 = Web3(HTTPProvider(rpc_url))
                
                # Configure Web3 for POA networks if applicable
                try:
                    # Test if we can get the latest block
                    new_web3.eth.get_block('latest')
                except Exception as e:
                    logger.warning(f"Error accessing blockchain, configuring for POA: {e}")
                    # Add support for POA chains manually if needed
                    from web3.middleware.formatting import construct_formatting_middleware
                    poa_middleware = construct_formatting_middleware(
                        request_formatters={
                            'eth_sendTransaction': apply_gas_price,
                            'eth_estimateGas': apply_gas_price
                        }
                    )
                    new_web3.middleware_onion.add(poa_middleware)
                    logger.info("Added POA middleware for compatibility")
                
                logger.info(f"Created new Web3 instance for {network_id}")
                self._web3_clients[network_id] = new_web3
                
            # Get or create wallet for the new network if using CDP
            new_wallet = None
            if hasattr(self, 'account'):
                # Using private key wallet, no need to create a new one for each network
                logger.info(f"Using private key wallet for {network_id}")
            elif network_id in self._wallets:
                # Use cached wallet
                new_wallet = self._wallets[network_id]
                logger.info(f"Using cached wallet for {network_id}")
            elif self._provider:
                # Create a new wallet using CDP
                try:
                    new_wallet = self._provider.get_wallet(network_id)
                    logger.info(f"Created new wallet for {network_id}")
                    self._wallets[network_id] = new_wallet
                except Exception as wallet_err:
                    logger.error(f"Failed to create CDP wallet: {wallet_err}")
                    # If no wallet is available and we're not using private key
                    if not hasattr(self, 'account'):
                        return False
                
            # Update current network, wallet, and Web3 instance
            self.current_network_id = network_id
            if new_wallet:
                self._wallet = new_wallet
            self.web3 = new_web3
            
            logger.info(f"Successfully switched to network {network_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error switching to network {network_id}: {e}")
            return False

    def sign_message(self, message: str) -> str:
        """Sign a message with the wallet.
        
        Args:
            message (str): Message to sign.
            
        Returns:
            str: Signature.
        """
        from web3 import Web3
        message_hash = Web3.keccak(text=message)
        # Use CDP SDK to create a payload signature
        payload = self._wallet.create_payload_signature(message_hash.hex())
        if hasattr(payload, "wait"):
            payload.wait()  # wait for server signer if applicable
        signature = payload.signature
        return signature

    def read_contract(
        self,
        contract_address: ChecksumAddress,
        abi: list[dict[str, Any]],
        function_name: str,
        args: list[Any] | None = None,
        block_identifier: BlockIdentifier = "latest",
    ) -> Any:
        """Read data from a smart contract.

        Args:
            contract_address (ChecksumAddress): The address of the contract to read from
            abi (list[dict[str, Any]]): The ABI of the contract
            function_name (str): The name of the function to call
            args (list[Any] | None): Arguments to pass to the function call, defaults to empty list
            block_identifier (BlockIdentifier): The block number to read from, defaults to 'latest'

        Returns:
            Any: The result of the contract function call

        Raises:
            Exception: If the contract call fails or wallet is not initialized

        """
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        func = contract.functions[function_name]
        if args is None:
            args = []
        return func(*args).call(block_identifier=block_identifier)

    def sign_typed_data(self, typed_data: dict[str, Any]) -> HexStr:
        """Sign typed data according to EIP-712 standard.

        Args:
            typed_data (dict[str, Any]): The typed data to sign following EIP-712 format

        Returns:
            HexStr: The signature as a hex string

        Raises:
            Exception: If the wallet is not initialized or signing fails

        """
        typed_data_message_hash = hash_typed_data_message(typed_data)

        payload_signature = self._wallet.sign_payload(typed_data_message_hash)

        return payload_signature.signature

    def sign_transaction(self, transaction: TxParams) -> HexStr:
        """Sign an EVM transaction.

        Args:
            transaction (TxParams): Transaction parameters including to, value, and data

        Returns:
            HexStr: The transaction signature as a hex string

        Raises:
            Exception: If wallet is not initialized or signing fails

        """
        dynamic_fee_tx = DynamicFeeTransaction.from_dict(transaction)

        tx_hash_bytes = dynamic_fee_tx.hash()
        tx_hash_hex = tx_hash_bytes.hex()

        payload_signature = self._wallet.sign_payload(tx_hash_hex)
        return payload_signature.signature

    def send_transaction(self, transaction: TxParams) -> HexStr:
        """Send a signed transaction to the network.

        Args:
            transaction (TxParams): Transaction parameters.

        Returns:
            HexStr: Transaction hash.
        """
        try:
            # Ensure web3 is initialized
            if self.web3 is None:
                logger.warning("Web3 client not initialized, attempting to initialize")
                rpc_url = DEFAULT_RPC_ENDPOINTS.get(self.current_network_id)
                if rpc_url:
                    self.web3 = Web3(HTTPProvider(rpc_url))
                    # Configure Web3 for POA networks if applicable
                    try:
                        self.web3.eth.get_block('latest')
                    except Exception as e:
                        logger.warning(f"Error accessing blockchain, configuring for POA: {e}")
                        from web3.middleware.formatting import construct_formatting_middleware
                        poa_middleware = construct_formatting_middleware(
                            request_formatters={
                                'eth_sendTransaction': apply_gas_price,
                                'eth_estimateGas': apply_gas_price
                            }
                        )
                        self.web3.middleware_onion.add(poa_middleware)
                        logger.info("Added POA middleware for compatibility")
                else:
                    raise Exception(f"No RPC URL found for network {self.current_network_id}")

            # Get the address
            if hasattr(self, 'account'):
                from_address = Web3.to_checksum_address(self.account.address)
            elif self._wallet:
                from_address = Web3.to_checksum_address(self._wallet.address)
            else:
                raise Exception("No wallet initialized")

            # Complete transaction parameters
            if 'chainId' not in transaction:
                transaction['chainId'] = self.get_chain_id()
            
            if 'from' not in transaction:
                transaction['from'] = from_address
                
            if 'to' in transaction and transaction['to'] is not None:
                transaction['to'] = Web3.to_checksum_address(transaction['to'])
                
            if 'nonce' not in transaction:
                transaction['nonce'] = self.web3.eth.get_transaction_count(from_address)
                
            if 'gasPrice' not in transaction and 'maxFeePerGas' not in transaction:
                transaction['gasPrice'] = self.web3.eth.gas_price
                
            if 'gas' not in transaction:
                # Estimate gas
                tx_params_for_estimate = dict(transaction)
                if 'gasPrice' in tx_params_for_estimate:
                    tx_params_for_estimate.pop('gasPrice')
                if 'nonce' in tx_params_for_estimate:
                    tx_params_for_estimate.pop('nonce')
                try:
                    transaction['gas'] = int(self.web3.eth.estimate_gas(tx_params_for_estimate) * 1.2)  # Add 20% buffer
                except Exception as e:
                    logger.warning(f"Failed to estimate gas: {e}, using default value")
                    transaction['gas'] = 200000  # Default gas limit
            
            logger.info(f"Sending transaction: {transaction}")
            
            # Send transaction
            if hasattr(self, 'account'):
                # Using private key wallet
                signed_tx = self.account.sign_transaction(transaction)
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                return tx_hash.hex()
            elif self._wallet:
                # Using CDP wallet
                return self._wallet.transfer(
                    to=transaction['to'],
                    data=transaction.get('data', None),
                    value=transaction.get('value', 0),
                    wait_for_receipt=False
                ).transaction_hash
            else:
                raise Exception("No wallet initialized")
        except Exception as e:
            logger.error(f"Error sending transaction: {e}")
            raise Exception(f"Error sending transaction: {e}")

    def wait_for_transaction_receipt(
        self, tx_hash: HexStr, timeout: float = 120, poll_latency: float = 0.1
    ) -> dict[str, Any]:
        """Wait for transaction confirmation and return receipt.

        Args:
            tx_hash (HexStr): The transaction hash to wait for
            timeout (float): Maximum time to wait in seconds, defaults to 120
            poll_latency (float): Time between polling attempts in seconds, defaults to 0.1

        Returns:
            dict[str, Any]: The transaction receipt as a dictionary

        Raises:
            TimeoutError: If transaction is not mined within timeout period

        """
        return self.web3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=timeout, poll_latency=poll_latency
        )

    def _prepare_transaction(self, transaction: TxParams) -> TxParams:
        """Prepare EIP-1559 transaction for signing.

        Args:
            transaction (TxParams): Raw transaction parameters

        Returns:
            TxParams: Transaction parameters with gas estimation and fee calculation

        Raises:
            Exception: If transaction preparation fails

        """
        if transaction["to"]:
            transaction["to"] = Web3.to_bytes(hexstr=transaction["to"])
        else:
            transaction["to"] = b""

        transaction["from"] = self._wallet.default_address.address_id
        transaction["value"] = int(transaction.get("value", 0))
        transaction["type"] = 2
        transaction["chainId"] = int(self.get_chain_id())

        nonce = self.web3.eth.get_transaction_count(self._wallet.default_address.address_id)
        transaction["nonce"] = nonce

        data_field = transaction.get("data", b"")
        if isinstance(data_field, str) and data_field.startswith("0x"):
            data_bytes = bytes.fromhex(data_field[2:])

        transaction["data"] = data_bytes

        max_priority_fee_per_gas, max_fee_per_gas = self._estimate_fees()
        transaction["maxPriorityFeePerGas"] = max_priority_fee_per_gas
        transaction["maxFeePerGas"] = max_fee_per_gas

        gas = int(self.web3.eth.estimate_gas(transaction) * 1.2)
        transaction["gas"] = gas

        del transaction["from"]

        return transaction

    def _estimate_fees(self):
        """Estimate gas fees for a transaction, applying the configured fee multipliers.

        Returns:
            tuple[int, int]: Tuple of (max_priority_fee_per_gas, max_fee_per_gas) in wei

        """

        def get_base_fee():
            latest_block = self.web3.eth.get_block("latest")
            base_fee = latest_block["baseFeePerGas"]
            # Multiply the configured fee multiplier to give some buffer
            return int(base_fee * 1)

        def get_max_priority_fee():
            max_priority_fee_per_gas = Web3.to_wei(0.1, "gwei")
            # Multiply the configured fee multiplier to give some buffer
            return int(max_priority_fee_per_gas * 1)

        base_fee_per_gas = get_base_fee()
        max_priority_fee_per_gas = get_max_priority_fee()
        max_fee_per_gas = base_fee_per_gas + max_priority_fee_per_gas

        return (max_priority_fee_per_gas, max_fee_per_gas)

    def export_wallet(self) -> WalletData:
        """Export the wallet data for persistence.

        Returns:
            WalletData: The wallet data object containing all necessary information

        Raises:
            Exception: If wallet is not initialized

        """
        if self._wallet:
            # Export CDP wallet data
            return self._wallet.export_data()
        elif hasattr(self, 'account'):
            # For private key wallets, return a simplified version
            # Instead of creating WalletData directly, add a custom to_dict method
            # that matches the expected format
            class CustomWalletData:
                def __init__(self, address, network_id):
                    self.address = address
                    self.network_id = network_id
                
                def to_dict(self):
                    return {
                        "address": self.address,
                        "network_id": self.network_id,
                        "wallet_type": "private_key"
                    }
            
            return CustomWalletData(
                address=self.account.address,
                network_id=self.current_network_id
            )
        else:
            raise Exception("Wallet not initialized")

    def deploy_contract(
        self,
        solidity_version: str,
        solidity_input_json: str,
        contract_name: str,
        constructor_args: dict[str, Any],
    ) -> Any:
        """Deploy a smart contract.

        Args:
            solidity_version (str): The version of the Solidity compiler to use
            solidity_input_json (str): The JSON input for the Solidity compiler
            contract_name (str): The name of the contract to deploy
            constructor_args (dict[str, Any]): Key-value map of constructor arguments

        Returns:
            Any: The deployed contract instance

        Raises:
            Exception: If wallet is not initialized or deployment fails

        """
        if not self._wallet:
            raise Exception("Wallet not initialized")

        try:
            return self._wallet.deploy_contract(
                solidity_version=solidity_version,
                solidity_input_json=solidity_input_json,
                contract_name=contract_name,
                constructor_args=constructor_args,
            )
        except Exception as e:
            raise Exception(f"Failed to deploy contract: {e!s}") from e

    def deploy_nft(self, name: str, symbol: str, base_uri: str) -> Any:
        """Deploy a new NFT (ERC-721) smart contract.

        Args:
            name (str): The name of the NFT collection
            symbol (str): The token symbol for the collection
            base_uri (str): The base URI for token metadata

        Returns:
            Any: The deployed NFT contract instance

        Raises:
            Exception: If wallet is not initialized or deployment fails

        """
        if not self._wallet:
            raise Exception("Wallet not initialized")

        try:
            return self._wallet.deploy_nft(
                name=name,
                symbol=symbol,
                base_uri=base_uri,
            )
        except Exception as e:
            raise Exception(f"Failed to deploy NFT: {e!s}") from e

    def deploy_token(self, name: str, symbol: str, total_supply: str) -> Any:
        """Deploy an ERC20 token contract.

        Args:
            name (str): The name of the token
            symbol (str): The symbol of the token
            total_supply (str): The total supply of the token

        Returns:
            Any: The deployed token contract instance

        Raises:
            Exception: If wallet is not initialized or deployment fails

        """
        if not self._wallet:
            raise Exception("Wallet not initialized")

        try:
            return self._wallet.deploy_token(
                name=name,
                symbol=symbol,
                total_supply=total_supply,
            )
        except Exception as e:
            raise Exception(f"Failed to deploy token: {e!s}") from e

    def trade(self, amount: str, from_asset_id: str, to_asset_id: str) -> str:
        """Trade a specified amount of one asset for another.

        Args:
            amount (str): The amount of the from asset to trade, e.g. `15`, `0.000001`.
            from_asset_id (str): The from asset ID to trade (e.g., "eth", "usdc", or a valid contract address).
            to_asset_id (str): The to asset ID to trade (e.g., "eth", "usdc", or a valid contract address).

        Returns:
            str: A message containing the trade details and transaction information

        Raises:
            Exception: If trade fails or wallet is not initialized

        """
        if not self._wallet:
            raise Exception("Wallet not initialized")

        try:
            trade_result = self._wallet.trade(
                amount=amount,
                from_asset_id=from_asset_id,
                to_asset_id=to_asset_id,
            ).wait()

            return "\n".join(
                [
                    f"Traded {amount} of {from_asset_id} for {trade_result.to_amount} of {to_asset_id}.",
                    f"Transaction hash for the trade: {trade_result.transaction.transaction_hash}",
                    f"Transaction link for the trade: {trade_result.transaction.transaction_link}",
                ]
            )
        except Exception as e:
            raise Exception(f"Error trading assets: {e!s}") from e

# Add helper function for gas price
def apply_gas_price(method, params):
    if len(params) >= 1 and isinstance(params[0], dict) and 'gasPrice' not in params[0]:
        params[0]['gasPrice'] = 1000000000  # 1 Gwei default
    return method, params
