"""
Tests loading and accessing the core service configuration
"""
import os

import linuxforhealth.healthos.core.config
from linuxforhealth.healthos.core.config import (
    CoreServiceConfig,
    get_core_configuration,
    load_core_configuration,
)


def test_load_get_core_configuration(resources_path: str, monkeypatch):
    """
    Validates that the core configuration accessor returns a configuration after it has been loaded.

    :param resources_path: The path to the test resource directory
    """
    monkeypatch.setattr(
        linuxforhealth.healthos.core.config, "core_service_config", None
    )
    config: CoreServiceConfig = get_core_configuration()
    assert config is None

    config_path: str = os.path.join(
        resources_path, "service-config", "core-service.yml"
    )
    load_core_configuration(config_path)
    config = get_core_configuration()
    assert config is not None
