"""Schemas for Wallet action provider."""

from pydantic import BaseModel, Field, field_validator
from typing import Union, List, Dict, Optional

from .validators import positive_decimal_validator


class GetWalletDetailsSchema(BaseModel):
    """Input schema for getting wallet details."""

    pass


class GetBalanceSchema(BaseModel):
    """Input schema for getting native currency balance."""

    pass


class NativeTransferSchema(BaseModel):
    """Input schema for native asset transfer."""

    to: str = Field(
        ...,
        description="The destination address to transfer to (e.g. '0x5154eae861cac3aa757d6016babaf972341354cf')",
    )
    value: str = Field(
        ..., description="The amount to transfer in whole units (e.g. '1.5' for 1.5 ETH)"
    )

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: str) -> str:
        """Validate the transfer value."""
        return positive_decimal_validator(v)


class SwitchNetworkSchema(BaseModel):
    """Input schema for switching networks."""
    
    network_id: str = Field(
        ...,
        description="The ID of the network to switch to (e.g., 'base-sepolia', 'optimism-sepolia', 'zora', 'unichain')",
    )


class CallContractSchema(BaseModel):
    """Input schema for calling smart contract functions."""
    
    contract_address: str = Field(
        ...,
        description="The address of the smart contract to interact with",
    )
    
    abi: Union[str, List, Dict] = Field(
        ...,
        description="The ABI (Application Binary Interface) of the contract function, can be a JSON string or object",
    )
    
    function_name: str = Field(
        ...,
        description="The name of the function to call on the contract",
    )
    
    inputs: Optional[Union[Dict, List]] = Field(
        None,
        description="Arguments for the function, can be an object with named parameters or an array of positional arguments",
    )
    
    network: Optional[str] = Field(
        None,
        description="Network ID to use for the call (if different from current network)",
    )
