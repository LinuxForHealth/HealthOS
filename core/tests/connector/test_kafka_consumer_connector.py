"""
test_kafka_consumer_connector.py

Tests the KafkaConsumer connector.
"""
from typing import List
from unittest.mock import AsyncMock, call

import pytest

from linuxforhealth.healthos.core.config import ConnectorConfig
from linuxforhealth.healthos.core.connector.kafka import (
    AIOKafkaConsumer, consume_message, create_kafka_consumer_connector,
    get_kafka_consumer_connectors, process_data)


@pytest.fixture
def connector_configs() -> List[ConnectorConfig]:
    """Returns a list containing KafkaConsumer ConnectorConfig models"""
    config_data = [
        {
            "type": "inbound",
            "id": "kafka-consumer-1",
            "name": "Test Kafka Consumer 1",
            "config": {
                "type": "KafkaConsumer",
                "topics": ["topic-a"],
                "bootstrap_servers": "somehost:9092",
            },
        },
        {
            "type": "inbound",
            "id": "kafka-consumer-2",
            "name": "Test Kafka Consumer 2",
            "config": {
                "type": "KafkaConsumer",
                "topics": ["hot-topic"],
                "bootstrap_servers": "otherhost:9092",
            },
        },
    ]

    configs: List[ConnectorConfig] = [ConnectorConfig(**c) for c in config_data]
    return configs


@pytest.mark.asyncio
async def test_get_and_create_kafka_consumer_connectors(monkeypatch, connector_configs):
    """
    Validates that get_kafka_consumer_connectors and create_kafka_consumer_connectors work correctly.
    - get_kafka_connnectors returns an empty list prior to create_kafka_consumer_connectors being invoked
    - get_kafka_connectors returns a populated list after create_kafka_consumer_connectors is invoked.

    :param monkeypatch: The pytest monkeypatch fixture
    :param connector_configs: The Kafka Connector Configuration fixtures
    """
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.kafka.kafka_consumer_connectors",
        None,
    )
    assert True

    monkeypatch.setattr(AIOKafkaConsumer, "start", AsyncMock())

    kafka_consumers = get_kafka_consumer_connectors()
    assert kafka_consumers == []

    await create_kafka_consumer_connector(connector_configs)

    kafka_consumers = get_kafka_consumer_connectors()
    assert len(kafka_consumers) == 2


@pytest.mark.asyncio
async def test_consume_message(monkeypatch, mock_kafka_consumer, publish_model):
    """
    Tests consume messages when processing completes as expected
    """
    process_data_mock = AsyncMock(spec=process_data)
    process_data_mock.return_value = publish_model
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.kafka.process_data", process_data_mock
    )

    mock_consumer = mock_kafka_consumer([b"ADT-hl7v2-message", b"ORU-hl7v2-message"])
    await consume_message(mock_consumer)

    expected_calls = [call("ADT-hl7v2-message"), call("ORU-hl7v2-message")]
    assert process_data_mock.call_count == 2
    process_data_mock.assert_has_calls(expected_calls)
