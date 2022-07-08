import pytest
from typing import Dict
from linuxforhealth.healthos.core.config.app import CoreApp


@pytest.fixture
def config_data() -> Dict:
    return {"port": 5000, "host": "0.0.0.0", "debug": True}


def test_validate_minimum_input(config_data: Dict):
    """Validates the minimum input config for a CoreApp"""
    config = CoreApp(**config_data)
    assert config.port == 5000
    assert config.host == "0.0.0.0"
    assert config.debug is True


def test_defaults(config_data: Dict):
    """Validates the defaults for a CoreApp"""
    config = CoreApp()
    assert config.port == 8080
    assert config.host == "localhost"
    assert config.debug is False
