"""
test_nats_config.py

Test cases for Nats Client connector configuration.
"""
import pytest
from typing import Dict
from linuxforhealth.healthos.core.config.nats import NatsClientConfig
from pydantic import ValidationError


@pytest.fixture
def config_data() -> Dict:
    """Returns the minimal config data for the NATS client"""
    return {"type": "NatsClient", "servers": ["nats://localhost:4222"]}


def test_validate_minimum_input(config_data):
    """Validates the minimum config fields for the NATS client"""
    config = NatsClientConfig(**config_data)
    assert config.servers == ["nats://localhost:4222"]

    # validate the servers field default value
    del config_data["servers"]
    config = NatsClientConfig(**config_data)
    assert config.servers == ["nats://localhost:4222"]


def test_default_values(config_data):
    """Validates that fields have expected default values"""
    config = NatsClientConfig(**config_data)
    assert config.pedantic is False
    assert config.verbose is False
    assert config.allow_reconnect is True
    assert config.connect_timeout == 2
    assert config.reconnect_time_wait == 2
    assert config.max_reconnect_attempts == 60
    assert config.ping_interval == 120
    assert config.max_outstanding_pings == 2
    assert config.dont_randomize is False
    assert config.flusher_queue_size == 1024
    assert config.no_echo is False
    assert config.drain_timeout == 30
    assert config.inbox_prefix == b"_INBOX"
    assert config.pending_size == 2_097_152
    assert config.flush_timeout == 10.0


@pytest.mark.parametrize(
    "field_name",
    [
        "connect_timeout",
        "reconnect_time_wait",
        "max_reconnect_attempts",
        "ping_interval",
        "max_outstanding_pings",
        "flusher_queue_size",
        "drain_timeout",
        "pending_size",
        "flush_timeout",
    ],
)
def test_positive_numeric_fields(config_data: Dict, field_name: str):
    """Validates that each field listed via parameters supports values >= 0"""
    config_data[field_name] = -1
    with pytest.raises(ValidationError):
        NatsClientConfig(**config_data)
