"""
test_core_config.py

Test cases for the top level "core" service model.
"""
import os
from typing import List

import pytest

from linuxforhealth.healthos.core.config import (ConnectorConfig,
                                                 CoreServiceConfig,
                                                 get_core_configuration,
                                                 load_core_configuration)


@pytest.fixture
def core_configuration(resources_path) -> CoreServiceConfig:
    """Returns the Core Service Configuration Model"""
    file_path = os.path.join(resources_path, "service-config", "core-service.yml")
    load_core_configuration(file_path)
    return get_core_configuration()


def test_inbound_connectors_prop(core_configuration: CoreServiceConfig):
    """
    Validates the inbound_connectors property.

    :param core_configuration: The core service configuration model
    """
    connector_types = {c.type for c in core_configuration.inbound_connectors}
    assert connector_types == {"inbound"}


def test_inbound_nats_connectors_property(core_configuration: CoreServiceConfig):
    """
    Validates the inbound_nats_connectors property.

    :param core_configuration: The core service configuration model
    """
    nats_connectors: List[ConnectorConfig] = core_configuration.inbound_nats_connectors
    assert len(nats_connectors) == 1
    assert nats_connectors[0].config.type == "NatsClient"


def test_inbound_rest_connectors_property(core_configuration: CoreServiceConfig):
    """
    Validates the inbound_rest_connectors property.

    :param core_configuration: The core service configuration model
    """
    rest_connectors: List[ConnectorConfig] = core_configuration.inbound_rest_connectors
    assert len(rest_connectors) == 1
    assert rest_connectors[0].config.type == "RestEndpoint"


def test_inbound_kafka_connectors_property(core_configuration: CoreServiceConfig):
    """
    Validates the inbound_kafka_connectors property.

    :param core_configuration: The core service configuration model
    """
    kafka_connectors: List[
        ConnectorConfig
    ] = core_configuration.inbound_kafka_connectors
    assert len(kafka_connectors) == 1


def test_load_core_service_configuration(core_configuration: CoreServiceConfig):
    """
    Validates the core service configuration model

    :param core_configuration: The core service configuration model
    """
    assert isinstance(core_configuration.connectors, list)
    assert len(core_configuration.connectors) == 3
    assert len(core_configuration.inbound_connectors) == 3


def test_load_core_service_configuration_invalid_path():
    """
    Validates that an exception is raised when a config file path is invalid
    """
    with pytest.raises(FileNotFoundError):
        load_core_configuration("/tmp/not-a-valid-config-file.ymlz")
