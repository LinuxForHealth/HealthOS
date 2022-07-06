import pytest
from linuxforhealth.healthos.core.config.connector import (
    ConnectorConfig,
    load_connector_configuration,
)
from pydantic import ValidationError
import os


def test_validate_minimum_kafka_consumer_input():
    config_data = {
        "type": "inbound",
        "id": "kafka-consumer-1",
        "name": "Kafka Consumer Config",
        "config": {
            "type": "KafkaConsumer",
            "topics": ["my_topic", "my_other_topic"],
            "bootstrap_servers": "localhost:9092",
        },
    }
    ConnectorConfig(**config_data)


def test_validate_minimum_kafka_producer_input():
    config_data = {
        "type": "outbound",
        "id": "kafka-producer-1",
        "name": "Kafka Producer Config",
        "config": {
            "type": "KafkaProducer",
            "bootstrap_servers": "localhost:9092",
        },
    }
    ConnectorConfig(**config_data)


def test_validate_minimum_nats_input():
    """Validates the minimal configuration for a NATS connector"""
    config_data = {
        "type": "inbound",
        "id": "nats-client-1",
        "name": "NATS Client",
        "config": {
            "type": "NatsClient",
            "servers": ["nats://localhost:4222"],
        },
    }
    ConnectorConfig(**config_data)

    config_data["type"] = "outbound"
    ConnectorConfig(**config_data)


def test_validate_minimum_rest_input():
    """Validates the minimal configuration for a REST endpoint connector"""
    config_data = {
        "type": "inbound",
        "id": "rest-endpoint-1",
        "name": "REST Endpoint",
        "config": {
            "type": "RestEndpoint",
        },
    }
    ConnectorConfig(**config_data)

    config_data["type"] = "outbound"
    config_data["rest_host"] = "some-server"
    ConnectorConfig(**config_data)


def test_validate_connector_type_value():
    """Validates the connect.type field"""
    config_data = {
        "type": "invalid-value",
        "id": "kafka-producer-1",
        "name": "Kafka Producer Config",
        "config": {
            "type": "KafkaProducer",
            "bootstrap_servers": "localhost:9092",
        },
    }
    with pytest.raises(ValidationError):
        ConnectorConfig(**config_data)


def test_validate_connector_type_config():
    """Validates that an exception is raised if connector.type is not compatible with config.type"""
    config_data = {
        "type": "inbound",
        "id": "kafka-producer-1",
        "name": "Kafka Producer Config",
        "config": {
            "type": "KafkaProducer",
            "bootstrap_servers": "localhost:9092",
        },
    }
    with pytest.raises(ValidationError):
        ConnectorConfig(**config_data)


@pytest.mark.parametrize(
    "config_file_name,expected_length",
    [
        ("kafka-consumer-connector.yaml", 1),
        ("kafka-producer-connector.yaml", 1),
        ("nats-client-connector.yaml", 1),
        ("rest-endpoint-connector.yaml", 1),
        ("inbound-connector.yaml", 2),
    ],
)
def test_load_connector_configuration(resources_path: str,
                                      config_file_name: str,
                                      expected_length: int):
    """Loads a connector configuration from file"""
    file_path = os.path.join(resources_path, config_file_name)
    config_data = load_connector_configuration(file_path)
    assert isinstance(config_data, list)
    assert len(config_data)


def test_load_connector_configuration_invalid_path(resources_path: str):
    """Validates that an exception is raised when a config file path is invalid"""
    file_path = os.path.join(resources_path, "not-a-real-file.yaml")
    with pytest.raises(FileNotFoundError):
        load_connector_configuration(file_path)
