import logging
from typing import Any, Dict
import json

from web3 import Web3

from coinbase_agentkit.action_providers.action_provider import ActionProvider
from coinbase_agentkit.action_providers.action_decorator import create_action
from coinbase_agentkit.wallet_providers.cdp_wallet_provider import CdpWalletProvider

# Replace the following imports with the actual path to your constants
from .constants import NETWORKS, CONTRACT_ADDRESS, SUPER_ERC20_ABI, CHAIN_IDS, AGENT_ADDRESS

logger = logging.getLogger(__name__)

class SkywireActionProvider(ActionProvider[CdpWalletProvider]):
    """Action provider for interacting with the Skywire Protocol's cross-chain operations."""

    def __init__(self):
        """Initialize the Skywire action provider."""
        super().__init__("skywire", NETWORKS)
        self.contract_abi = SUPER_ERC20_ABI
        self.agent_address = AGENT_ADDRESS

    def supports_network(self, network_id: str) -> bool:
        """Check if the network is supported by this action provider."""
        return network_id in NETWORKS

    @create_action(
        name="crosschain_burn",
        description="""
This action burns sETH tokens on the source chain in preparation for a cross-chain transfer.

Arguments:
- amount: Amount of sETH tokens to burn (in wei or in decimal ETH units)
- chain_id: Chain ID of the source chain where tokens will be burned
- from_address: Address of the user whose tokens will be burned

Notes:
- The user must have sufficient sETH tokens on the source chain.
- This is the first step in a cross-chain transfer process.
- Only the agent can execute this operation (onlyAgent modifier).
""",
    )
    def crosschain_burn(self, wallet_provider: CdpWalletProvider, args: Dict[str, Any]) -> str:
        """Burns sETH tokens on the source chain."""
        try:
            # 1) Parse amount and convert to int
            try:
                raw_amount_str = str(args["amount"]).lower().replace("seth", "").strip()
                if '.' in raw_amount_str:
                    # Convert decimal ETH to wei
                    amount = int(round(float(raw_amount_str) * 10**18))
                else:
                    amount = int(raw_amount_str)
            except ValueError:
                return f"Error: Amount must be a valid number, got {args['amount']}"

            from_address = args["from_address"]
            chain_id = int(args.get("chain_id", 0))

            # 2) Handle default chain_id logic
            if chain_id == 0:
                chain_id = wallet_provider.get_chain_id()
                logger.info(f"Using current chain ID: {chain_id}")

            # 3) Find the matching network_id
            network_id = None
            for net, cid in CHAIN_IDS.items():
                if cid == chain_id:
                    network_id = net
                    break
            if not network_id:
                return f"Error: Chain ID {chain_id} is not supported"

            # 4) Switch network if needed
            if getattr(wallet_provider, 'get_chain_id', None):
                current_chain = wallet_provider.get_chain_id()
                if current_chain != chain_id:
                    logger.info(f"Switching from chain {current_chain} to {chain_id} for burn operation")
                    success = wallet_provider.switch_network(network_id)
                    if not success:
                        return (f"Failed to switch to network {network_id} (Chain ID: {chain_id}). "
                                "Please switch manually and try again.")
                    logger.info(f"Successfully switched to {network_id}")

            # 5) Setup contract
            contract_address = CONTRACT_ADDRESS
            if not contract_address:
                return f"Error: No contract address found for chain ID {chain_id}"
            web3 = wallet_provider.web3
            if not web3:
                return f"Error: No Web3 instance available for network {network_id}"

            contract = web3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=self.contract_abi
            )

            # 6) Check user balance
            try:
                user_balance = contract.functions.balanceOf(from_address).call()
                if user_balance < amount:
                    return (f"Error: Insufficient balance. User has {user_balance} tokens "
                            f"but attempted to burn {amount}")
                logger.info(f"User balance check: {user_balance} tokens, attempting to burn {amount}")
            except Exception as e:
                logger.error(f"Error checking balance: {e}")
                return f"Error: Failed checking user balance: {str(e)}"

            # 7) Ensure the agent address is correct
            agent_address = wallet_provider.get_address()
            if (Web3.to_checksum_address(agent_address)
                    != Web3.to_checksum_address(self.agent_address)):
                return (f"Error: The wallet address {agent_address} does not match the required "
                        f"agent address {self.agent_address}")

            # 8) Prepare the transaction
            logger.info(f"Executing crosschainBurn for {amount} tokens from {from_address} on {network_id}")
            try:
                # Create contract function call
                burn_function = contract.functions.crosschainBurn(
                    Web3.to_checksum_address(from_address),
                    amount
                )
                
                # Try to estimate gas, fallback to fixed amount if estimation fails
                try:
                    gas_estimate = burn_function.estimate_gas({
                        'from': agent_address,
                        'gasPrice': web3.eth.gas_price
                    })
                    logger.info(f"Estimated gas for burn: {gas_estimate}")
                except Exception as gas_error:
                    logger.warning(f"Gas estimation failed: {gas_error}. Using fallback gas limit.")
                    gas_estimate = 5_000_000

                # Build and send transaction
                tx = {
                    'from': agent_address,
                    'gas': gas_estimate,
                    'gasPrice': web3.eth.gas_price,
                    'nonce': web3.eth.get_transaction_count(agent_address)
                }
                
                tx_hash = wallet_provider.send_transaction({
                    **tx,
                    **burn_function.buildTransaction(tx)
                })
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                if receipt.status == 1:
                    return (f"Successfully burned {amount} tokens from {from_address} on {network_id}. "
                            f"Transaction hash: {tx_hash}")
                else:
                    return f"Burn transaction failed. Transaction hash: {tx_hash}. Status: {receipt.status}"

            except Exception as e:
                logger.error(f"Error in crosschain_burn: {e}")
                return f"Error performing burn operation: {str(e)}"

        except Exception as e:
            logger.error(f"Error in crosschain_burn: {e}")
            return f"Error performing burn operation: {str(e)}"

    @create_action(
        name="crosschain_mint",
        description="""
Mints sETH tokens on the destination chain to complete a cross-chain transfer.

Arguments:
- amount: Amount of tokens to mint (in wei or decimal ETH units)
- chain_id: Chain ID of the destination chain where tokens will be minted
- to_address: Address of the recipient to receive the minted tokens

Notes:
- This is typically called after burning tokens on the source chain.
- Only the agent can execute this operation (onlyAgent modifier).
""",
    )
    def crosschain_mint(self, wallet_provider: CdpWalletProvider, args: Dict[str, Any]) -> str:
        """Mints sETH tokens on the destination chain."""
        try:
            # 1) Parse amount and convert to int
            try:
                raw_amount_str = str(args["amount"]).lower().replace("seth", "").strip()
                if '.' in raw_amount_str:
                    amount = int(round(float(raw_amount_str) * 10**18))
                else:
                    amount = int(raw_amount_str)
            except ValueError:
                return f"Error: Amount must be a valid number, got {args['amount']}"

            to_address = args["to_address"]
            chain_id = int(args.get("chain_id", 0))
            if chain_id == 0:
                chain_id = wallet_provider.get_chain_id()
                logger.info(f"Using current chain ID: {chain_id}")

            # 2) Find the matching network_id
            network_id = None
            for net, cid in CHAIN_IDS.items():
                if cid == chain_id:
                    network_id = net
                    break
            if not network_id:
                return f"Error: Chain ID {chain_id} is not supported"

            # 3) Switch network if needed
            if getattr(wallet_provider, 'get_chain_id', None):
                current_chain = wallet_provider.get_chain_id()
                if current_chain != chain_id:
                    logger.info(f"Switching from chain {current_chain} to {chain_id} for mint operation")
                    success = wallet_provider.switch_network(network_id)
                    if not success:
                        return (f"Failed to switch to network {network_id} (Chain ID: {chain_id}). "
                                "Please switch manually and try again.")
                    logger.info(f"Successfully switched to {network_id}")

            # 4) Setup contract
            contract_address = CONTRACT_ADDRESS
            if not contract_address:
                return f"Error: No contract address found for chain ID {chain_id}"
            web3 = wallet_provider.web3
            if not web3:
                return f"Error: No Web3 instance available for network {network_id}"

            contract = web3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=self.contract_abi
            )

            # 5) Check agent address
            agent_address = wallet_provider.get_address()
            if (Web3.to_checksum_address(agent_address)
                    != Web3.to_checksum_address(self.agent_address)):
                return (f"Error: The wallet address {agent_address} does not match the required "
                        f"agent address {self.agent_address}")

            # 6) Execute mint transaction using the contract function call.
            logger.info(f"Executing crosschainMint for {amount} tokens to {to_address} on {network_id}")
            try:
                # Create contract function call
                mint_function = contract.functions.crosschainMint(
                    Web3.to_checksum_address(to_address),
                    amount
                )
                
                # Try to estimate gas, fallback to fixed amount if estimation fails
                try:
                    gas_estimate = mint_function.estimate_gas({
                        'from': agent_address,
                        'gasPrice': web3.eth.gas_price
                    })
                    logger.info(f"Estimated gas for mint: {gas_estimate}")
                except Exception as gas_error:
                    logger.warning(f"Gas estimation failed: {gas_error}. Using fallback gas limit.")
                    gas_estimate = 5_000_000

                # Build and send transaction
                tx = {
                    'from': agent_address,
                    'gas': gas_estimate,
                    'gasPrice': web3.eth.gas_price,
                    'nonce': web3.eth.get_transaction_count(agent_address)
                }
                
                tx_hash = wallet_provider.send_transaction({
                    **tx,
                    **mint_function.buildTransaction(tx)
                })
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                if receipt.status == 1:
                    return (f"Successfully minted {amount} tokens to {to_address} on {network_id}. "
                            f"Transaction hash: {tx_hash}")
                else:
                    return f"Mint transaction failed. Transaction hash: {tx_hash}. Status: {receipt.status}"

            except Exception as e:
                logger.error(f"Error executing crosschainMint: {str(e)}")
                return f"Failed to execute crosschainMint: {str(e)}"

        except Exception as e:
            logger.error(f"Error in crosschain_mint: {e}")
            return f"Error performing mint operation: {str(e)}"

    @create_action(
        name="crosschain_transfer",
        description="""
Performs a complete cross-chain transfer by burning tokens on the source chain and minting them on the destination chain.

Arguments:
- amount: Amount of tokens to transfer (in wei or in decimal)
- from_address: Address on the source chain where tokens will be burned from
- to_address: Address on the destination chain where tokens will be minted to
- source_chain_id: Chain ID of the source chain
- destination_chain_id: Chain ID of the destination chain

Notes:
- This combines the crosschain_burn and crosschain_mint operations.
- The source and destination addresses can be the same or different.
- Only the agent can execute this operation (onlyAgent modifier).
""",
    )
    def crosschain_transfer(self, wallet_provider: CdpWalletProvider, args: Dict[str, Any]) -> str:
        """Performs a complete cross-chain transfer."""
        try:
            # 1) Parse and validate 'amount'
            try:
                raw_amount_str = str(args["amount"]).lower().replace("seth", "").strip()
                if '.' in raw_amount_str:
                    amount = int(round(float(raw_amount_str) * 10**18))
                else:
                    amount = int(raw_amount_str)
            except ValueError:
                return f"Error: Amount must be a valid integer/decimal, got {args['amount']}"

            from_address = args["from_address"]
            to_address = args["to_address"]
            source_chain_id = int(args.get("source_chain_id", 0))
            destination_chain_id = int(args.get("destination_chain_id", 0))
            if source_chain_id == 0 or destination_chain_id == 0:
                return "Error: Both source_chain_id and destination_chain_id must be specified"

            logger.info(
                f"Starting cross-chain transfer: Burning {amount} tokens from {from_address} "
                f"on chain {source_chain_id}"
            )

            # 2) Perform burn
            burn_args = {
                "amount": amount,
                "from_address": from_address,
                "chain_id": source_chain_id,
            }
            burn_result = self.crosschain_burn(wallet_provider, burn_args)
            if "Successfully burned" not in burn_result:
                return f"Cross-chain transfer failed during burn step: {burn_result}"

            logger.info("Burn operation completed successfully. Proceeding to mint operation.")

            # 3) Perform mint
            mint_args = {
                "amount": amount,
                "to_address": to_address,
                "chain_id": destination_chain_id,
            }
            mint_result = self.crosschain_mint(wallet_provider, mint_args)
            if "Successfully minted" not in mint_result:
                return f"Cross-chain transfer partially completed. Burn was successful, but mint failed: {mint_result}"

            return (
                f"Cross-chain transfer completed successfully. {amount} tokens transferred from "
                f"{from_address} on chain {source_chain_id} to {to_address} on chain {destination_chain_id}."
            )

        except Exception as e:
            logger.error(f"Error in crosschain_transfer: {e}")
            return f"Error performing cross-chain transfer: {str(e)}"

    @create_action(
        name="deposit_eth",
        description="""
Deposits ETH to receive sETH tokens in a 1:1 ratio.

Arguments:
- amount: Amount of ETH to deposit (in normal ETH units, not wei)
- chain_id: Chain ID where the deposit will be made

Notes:
- This function will convert the specified amount to wei before sending.
- You will receive sETH tokens in a 1:1 ratio.
""",
    )
    def deposit_eth(self, wallet_provider: CdpWalletProvider, args: Dict[str, Any]) -> str:
        """Deposits ETH to receive sETH tokens."""
        try:
            # 1) Parse the deposit amount (ETH => wei)
            try:
                amount_eth = float(args["amount"])
                amount_wei = int(amount_eth * 10**18)
            except ValueError:
                return f"Error: Amount must be a valid number, got {args['amount']}"

            chain_id = int(args.get("chain_id", 0))
            if chain_id == 0:
                chain_id = wallet_provider.get_chain_id()
                logger.info(f"Using current chain ID: {chain_id}")

            # 2) Find the matching network_id
            network_id = None
            for net, cid in CHAIN_IDS.items():
                if cid == chain_id:
                    network_id = net
                    break
            if not network_id:
                return f"Error: Chain ID {chain_id} is not supported"

            # 3) Switch network if needed
            if getattr(wallet_provider, 'get_chain_id', None):
                current_chain = wallet_provider.get_chain_id()
                if current_chain != chain_id:
                    logger.info(f"Switching from chain {current_chain} to {chain_id} for deposit operation")
                    success = wallet_provider.switch_network(network_id)
                    if not success:
                        return (f"Failed to switch to network {network_id} (Chain ID: {chain_id}). "
                                "Please switch manually and try again.")
                    logger.info(f"Successfully switched to {network_id}")

            # 4) Setup contract
            contract_address = CONTRACT_ADDRESS
            if not contract_address:
                return f"Error: No contract address found for chain ID {chain_id}"
            web3 = wallet_provider.web3
            if not web3:
                return f"Error: No Web3 instance available for network {network_id}"

            contract = web3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=self.contract_abi
            )

            # 5) Build & send transaction
            logger.info(f"Executing deposit transaction for {amount_eth} ETH on {network_id}")
            try:
                sender_address = wallet_provider.get_address()
                tx_hash = wallet_provider.send_transaction({
                    'to': Web3.to_checksum_address(contract_address),
                    'data': contract.encodeABI(fn_name='deposit'),
                    'gas': 300_000,
                    'value': amount_wei,
                })
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                if receipt.status == 1:
                    return (f"Successfully deposited {amount_eth} ETH to receive sETH on {network_id}. "
                            f"Transaction hash: {tx_hash}")
                else:
                    return f"Deposit transaction failed. Transaction hash: {tx_hash}. Status: {receipt.status}"

            except Exception as e:
                logger.error(f"Error executing deposit: {str(e)}")
                return f"Failed to execute deposit: {str(e)}"

        except Exception as e:
            logger.error(f"Error in deposit_eth: {e}")
            return f"Error performing deposit operation: {str(e)}"

    @create_action(
        name="withdraw_eth",
        description="""
Withdraws ETH by burning sETH tokens.

Arguments:
- amount: Amount of sETH tokens to burn (in normal ETH units, not wei)
- chain_id: Chain ID where the withdrawal will be made

Notes:
- This function will convert the specified amount to wei before burning.
- You will receive ETH in a 1:1 ratio for your burned sETH.
""",
    )
    def withdraw_eth(self, wallet_provider: CdpWalletProvider, args: Dict[str, Any]) -> str:
        """Withdraws ETH by burning sETH tokens."""
        try:
            # 1) Parse the withdrawal amount (ETH => wei)
            try:
                amount_eth = float(args["amount"])
                amount_wei = int(amount_eth * 10**18)
            except ValueError:
                return f"Error: Amount must be a valid number, got {args['amount']}"

            chain_id = int(args.get("chain_id", 0))
            if chain_id == 0:
                chain_id = wallet_provider.get_chain_id()
                logger.info(f"Using current chain ID: {chain_id}")

            # 2) Find the matching network_id
            network_id = None
            for net, cid in CHAIN_IDS.items():
                if cid == chain_id:
                    network_id = net
                    break
            if not network_id:
                return f"Error: Chain ID {chain_id} is not supported"

            # 3) Switch network if needed
            if getattr(wallet_provider, 'get_chain_id', None):
                current_chain = wallet_provider.get_chain_id()
                if current_chain != chain_id:
                    logger.info(f"Switching from chain {current_chain} to {chain_id} for withdrawal operation")
                    success = wallet_provider.switch_network(network_id)
                    if not success:
                        return (f"Failed to switch to network {network_id} (Chain ID: {chain_id}). "
                                "Please switch manually and try again.")
                    logger.info(f"Successfully switched to {network_id}")

            # 4) Setup contract
            contract_address = CONTRACT_ADDRESS
            if not contract_address:
                return f"Error: No contract address found for chain ID {chain_id}"
            web3 = wallet_provider.web3
            if not web3:
                return f"Error: No Web3 instance available for network {network_id}"

            contract = web3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=self.contract_abi
            )

            sender_address = wallet_provider.get_address()

            # 5) Check sETH balance
            try:
                user_balance = contract.functions.balanceOf(sender_address).call()
                if user_balance < amount_wei:
                    return (f"Error: Insufficient balance. You have {user_balance / 10**18} sETH "
                            f"but attempted to withdraw {amount_eth} ETH")
            except Exception as e:
                logger.error(f"Error checking balance: {e}")
                return f"Error checking balance: {str(e)}"

            # 6) Build & send transaction
            logger.info(f"Executing withdraw transaction for {amount_eth} ETH on {network_id}")
            try:
                tx_hash = wallet_provider.send_transaction({
                    'to': Web3.to_checksum_address(contract_address),
                    'data': contract.encodeABI(fn_name='withdraw', args=[amount_wei]),
                    'gas': 300_000,
                })
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                if receipt.status == 1:
                    return (f"Successfully withdrew {amount_eth} ETH by burning sETH on {network_id}. "
                            f"Transaction hash: {tx_hash}")
                else:
                    return f"Withdrawal transaction failed. Transaction hash: {tx_hash}. Status: {receipt.status}"

            except Exception as e:
                logger.error(f"Error executing withdrawal: {str(e)}")
                return f"Failed to execute withdrawal: {str(e)}"

        except Exception as e:
            logger.error(f"Error in withdraw_eth: {e}")
            return f"Error performing withdrawal operation: {str(e)}"


def skywire_action_provider():
    """Create a SkywireActionProvider.

    Returns:
        SkywireActionProvider: A Skywire action provider.
    """
    return SkywireActionProvider()
