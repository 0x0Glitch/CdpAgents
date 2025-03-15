# Freya Action Provider

The Freya action provider enables cross-chain token transfers between super chain networks (Base Sepolia, Optimism Sepolia, Zora, and Unichain) using the Freya protocol's SuperERC20 token contracts.

## Features

- **Cross-chain Burn**: Burns sETH tokens on the source chain (agent-only operation)
- **Cross-chain Mint**: Mints sETH tokens on the destination chain (agent-only operation)
- **Cross-chain Transfer**: Orchestrates complete cross-chain transfers by burning tokens on the source chain and minting on the destination chain

## Contract Deployment

The SuperETH (sETH) contract is deployed at the following address across all supported chains:
```
0xEBE8Ca83dfFeaa2288a70B4f1e29EcD089d325E2
```

## Supported Chains

- Base Sepolia
- Optimism Sepolia
- Zora
- Unichain

## Security

The Freya protocol implements the `onlyAgent` modifier to ensure that sensitive operations (burn and mint) can only be executed by authorized AI agents. This security measure prevents unauthorized access and maintains the integrity of cross-chain transfers.

## Example Usage

```python
from coinbase_agentkit import AgentKit, AgentKitConfig, freya_action_provider

# Initialize AgentKit with Freya action provider
agentkit = AgentKit(
    AgentKitConfig(
        wallet_provider=wallet_provider,
        action_providers=[
            freya_action_provider(),
            # ... other action providers
        ],
    )
)

# Execute a cross-chain transfer
result = agentkit.execute_action(
    "crosschain_transfer",
    {
        "amount": "0.1",  # Amount in ETH units
        "source_chain": "base-sepolia",
        "destination_chain": "optimism-sepolia"
    }
)
```

## Implementation Details

- Transaction monitoring and block confirmation logic ensure reliable cross-chain transfers
- Seamless integration with the existing AgentKit architecture
- Proper verification to ensure only AI agent wallets can execute sensitive operations
