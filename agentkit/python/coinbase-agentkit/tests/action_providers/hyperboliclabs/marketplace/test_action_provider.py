"""Tests for the Hyperbolic Marketplace action provider initialization."""

import os
from unittest.mock import patch

import pytest

from coinbase_agentkit.action_providers.hyperboliclabs.marketplace.action_provider import (
    MarketplaceActionProvider,
    hyperbolic_marketplace_action_provider,
)
from coinbase_agentkit.network import Network


def test_init_with_api_key(mock_api_key):
    """Test initialization with API key."""
    provider = MarketplaceActionProvider(api_key=mock_api_key)
    assert provider is not None
    assert provider.api_key == mock_api_key


def test_init_with_env_var(mock_api_key):
    """Test initialization with environment variable."""
    with patch.dict(os.environ, {"HYPERBOLIC_API_KEY": mock_api_key}):
        provider = MarketplaceActionProvider()
        assert provider is not None
        assert provider.api_key == mock_api_key


def test_init_missing_api_key():
    """Test initialization with missing API key."""
    with patch.dict(os.environ, clear=True), pytest.raises(ValueError):
        MarketplaceActionProvider()


def test_supports_network(mock_api_key):
    """Test supports_network method."""
    provider = MarketplaceActionProvider(api_key=mock_api_key)
    network = Network(
        name="test_network",
        protocol_family="ethereum",
        chain_id="1",
        network_id="1",
    )
    assert provider.supports_network(network) is True


def test_factory_function(mock_api_key):
    """Test the factory function."""
    with patch(
        "coinbase_agentkit.action_providers.hyperboliclabs.marketplace.action_provider.MarketplaceActionProvider"
    ) as mock:
        hyperbolic_marketplace_action_provider(mock_api_key)
        mock.assert_called_once_with(api_key=mock_api_key)
