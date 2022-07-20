"""
test_nats_core_client.py

Tests the HealthOS NATS Core Client.
"""
from typing import List
from unittest.mock import AsyncMock, call

import pytest

from linuxforhealth.healthos.core.connector.nats import (
    ConnectorConfig, CoreServiceConfig, PublishDataModel,
    create_inbound_jetstream_clients, get_jetstream_clients,
    inbound_connector_callback, process_data)


@pytest.fixture
def connector_configs() -> List[ConnectorConfig]:
    """Returns a list containing NatsClient ConnectorConfig models"""
    config_data = [
        {
            "type": "inbound",
            "id": "nats-client-1",
            "name": "Test NATS Client 1",
            "config": {
                "type": "NatsClient",
                "servers": ["nats://localhost:4224"],
                "subjects": ["healthy-data"],
            },
        },
        {
            "type": "inbound",
            "id": "nats-client-2",
            "name": "Test NATS Client 2",
            "config": {
                "type": "NatsClient",
                "servers": ["nats://localhost:4230"],
                "subjects": ["healthy-data"],
            },
        },
    ]
    configs: List[ConnectorConfig] = [ConnectorConfig(**c) for c in config_data]
    return configs


@pytest.mark.asyncio
async def test_create_inbound_jetstream_clients(
    monkeypatch, mock_nats, connector_configs
):
    """
    Validates that inbound Jetstream Connectors are created correctly and are accessible.

    :param monkeypatch: The pytest monkeypatch fixture.
    :param mock_nats: AsyncMock object for NATS interactions.
    :param connector_configs: NATS Connector Configuration Fixtures
    """
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.jetstream_clients", None
    )
    monkeypatch.setattr("linuxforhealth.healthos.core.connector.nats.nats", mock_nats)

    js_clients = get_jetstream_clients()
    assert js_clients == []

    await create_inbound_jetstream_clients(connector_configs)

    js_clients = get_jetstream_clients()
    assert len(js_clients) == 2


@pytest.mark.asyncio
async def test_inbound_connector_callback(
    monkeypatch, core_configuration, publish_model
):
    """
    Tests the NATS callback function used for inbound connectors.

    :param monkeypatch: The pytest monkeypatch fixture
    """
    config: CoreServiceConfig = core_configuration("core-service.yml")
    process_data_mock = AsyncMock(spec=process_data)
    process_data_mock.return_value = publish_model

    inbound_message = AsyncMock()
    inbound_ack = AsyncMock()
    inbound_message.ack.return_value = inbound_ack
    inbound_message.data = b"hello world!"

    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.get_core_configuration",
        lambda: config,
    )
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.process_data", process_data_mock
    )

    await inbound_connector_callback(inbound_message)

    assert process_data_mock.call_count == 1

    expected_calls = [call("hello world!")]
    process_data_mock.assert_has_calls(expected_calls)
