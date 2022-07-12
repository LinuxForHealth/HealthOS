"""
test_core_config.py

Test cases for the top level "core" service model.
"""
import pytest
import os
from linuxforhealth.healthos.core.config import (
    load_core_configuration,
    get_core_configuration,
    CoreServiceConfig,
)


@pytest.fixture
def core_configuration(resources_path) -> CoreServiceConfig:
    """Returns the Core Service Configuration Model"""
    file_path = os.path.join(resources_path, "service-config", "core-service.yml")
    load_core_configuration(file_path)
    return get_core_configuration()


def test_core_service_inbound_connectors_prop(core_configuration: CoreServiceConfig):
    """
    Validates the inbound_connectors property.

    :param core_configuration: The core service configuration model
    """
    connector_types = {c.type for c in core_configuration.inbound_connectors}
    assert connector_types == {"inbound"}


def test_load_core_service_configuration(core_configuration: CoreServiceConfig):
    """
    Validates the core service configuration model

    :param core_configuration: The core service configuration model
    """
    assert isinstance(core_configuration.connectors, list)
    assert len(core_configuration.connectors) == 2
    assert len(core_configuration.inbound_connectors) == 2


def test_load_core_service_configuration_invalid_path():
    """
    Validates that an exception is raised when a config file path is invalid
    """
    with pytest.raises(FileNotFoundError):
        load_core_configuration("/tmp/not-a-valid-config-file.ymlz")
