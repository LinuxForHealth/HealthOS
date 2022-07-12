"""
test_core_config.py

Test cases for the top level "core" service model.
"""
import pytest
import os
from linuxforhealth.healthos.core.config import load_core_configuration


def test_core_service_inbound_connectors_prop(resources_path: str):
    """
    Validates the inbound_connectors property.

    :param resources_path: The path to the service configuration file
    """
    file_path = os.path.join(resources_path, "service-config", "core-service.yml")
    core_config = load_core_configuration(file_path)
    connector_types = {c.type for c in core_config.inbound_connectors}
    assert connector_types == {"inbound"}


def test_load_core_service_configuration(resources_path: str):
    """
    Validates the core service configuration model

    :param resources_path: The path to the service configuration
    :return:
    """
    file_path = os.path.join(resources_path, "service-config", "core-service.yml")
    core_config = load_core_configuration(file_path)
    assert isinstance(core_config.connectors, list)
    assert len(core_config.connectors) == 2
    assert len(core_config.inbound_connectors) == 2


def test_load_core_service_configuration_invalid_path(resources_path: str):
    """Validates that an exception is raised when a config file path is invalid"""
    file_path = os.path.join(resources_path, "not-a-real-file.yaml")
    with pytest.raises(FileNotFoundError):
        load_core_configuration(file_path)
