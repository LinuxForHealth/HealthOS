"""
test_core_app_messaging.py

Test cases for the Core App Messaging configuration.
"""
from typing import Dict

import pytest

from linuxforhealth.healthos.core.config.app import CoreAppMessaging


@pytest.fixture
def config_data() -> Dict:
    return {
        "url": "nats://0.0.0.0:4223",
    }


def test_validate_minimum_input(config_data: Dict):
    """Validates the minimum input config for a CoreApp"""
    config = CoreAppMessaging(**config_data)
    assert config.url == "nats://0.0.0.0:4223"
    assert config.stream_name == "healthos"
    assert config.ingress_subject == "core.ingress"
    assert config.error_subject == "core.error"


def test_defaults(config_data: Dict):
    """Validates the defaults for a CoreApp"""
    config = CoreAppMessaging()
    assert config.url == "nats://localhost:4222"
    assert config.stream_name == "healthos"
    assert config.ingress_subject == "core.ingress"
    assert config.error_subject == "core.error"
