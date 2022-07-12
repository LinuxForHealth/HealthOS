"""
test_core_app_config.py

Test cases for the Application configuration model.
"""
import pytest
from typing import Dict
from linuxforhealth.healthos.core.config.app import CoreApp


@pytest.fixture
def config_data() -> Dict:
    return {
        "port": 5000,
        "host": "0.0.0.0",
        "debug": True,
        "messaging": {
            "host": "0.0.0.0",
            "port": 4223,
            "stream_name": "core",
            "inbound_subject": "landing_zone",
        },
    }


def test_validate_minimum_input(config_data: Dict):
    """Validates the minimum input config for a CoreApp"""
    config = CoreApp(**config_data)
    assert config.port == 5000
    assert config.host == "0.0.0.0"
    assert config.debug is True
    assert config.messaging.host == "0.0.0.0"
    assert config.messaging.port == 4223
    assert config.messaging.stream_name == "core"
    assert config.messaging.inbound_subject == "landing_zone"


def test_defaults(config_data: Dict):
    """Validates the defaults for a CoreApp"""
    config = CoreApp()
    assert config.port == 8080
    assert config.host == "localhost"
    assert config.debug is False
    assert config.messaging.host == "localhost"
    assert config.messaging.port == 4222
    assert config.messaging.stream_name == "healthos"
    assert config.messaging.inbound_subject == "ingress"
