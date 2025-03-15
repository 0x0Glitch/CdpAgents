"""Schemas for the Skywire Protocol action provider."""

from typing import Optional
from pydantic import BaseModel, Field

class CrosschainBurnArgs(BaseModel):
    """Arguments for burning sETH tokens on the source chain."""
    amount: str = Field(..., description="Amount of sETH tokens to burn")
    from_address: str = Field(..., description="Address to burn tokens from")
    chain_id: Optional[int] = Field(None, description="Chain ID for the burn operation")

class CrosschainMintArgs(BaseModel):
    """Arguments for minting sETH tokens on the destination chain."""
    amount: str = Field(..., description="Amount of sETH tokens to mint")
    to_address: str = Field(..., description="Address to mint tokens to")
    chain_id: Optional[int] = Field(None, description="Chain ID for the mint operation")

class CrosschainTransferArgs(BaseModel):
    """Arguments for performing a cross-chain transfer."""
    amount: str = Field(..., description="Amount of sETH tokens to transfer")
    from_address: str = Field(..., description="Source address to transfer tokens from")
    to_address: str = Field(..., description="Destination address to transfer tokens to")
    source_chain_id: int = Field(..., description="Chain ID of the source network")
    destination_chain_id: int = Field(..., description="Chain ID of the destination network")

class DepositEthArgs(BaseModel):
    """Arguments for depositing ETH to receive sETH tokens."""
    amount: str = Field(..., description="Amount of ETH to deposit")
    chain_id: Optional[int] = Field(None, description="Chain ID for the deposit operation")

class WithdrawEthArgs(BaseModel):
    """Arguments for withdrawing ETH from sETH tokens."""
    amount: str = Field(..., description="Amount of ETH to withdraw")
    chain_id: Optional[int] = Field(None, description="Chain ID for the withdrawal operation")
