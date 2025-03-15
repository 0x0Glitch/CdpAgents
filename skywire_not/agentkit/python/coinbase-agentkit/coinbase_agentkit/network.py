"""Network configuration and utilities."""

from pydantic import BaseModel, field_validator
from typing import Optional, Union


class Network(BaseModel):
    """Represents a blockchain network."""

    protocol_family: str
    network_id: Optional[str] = None
    chain_id: Optional[Union[str, int]] = None
    chain_name: Optional[str] = None
    
    @field_validator('chain_id')
    def validate_chain_id(cls, v):
        """Convert chain_id to string if it's an integer."""
        if isinstance(v, int):
            return str(v)
        return v
