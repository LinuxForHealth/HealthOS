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
        "name": "Kafka Producer Config",
        "config": {
            "type": "KafkaProducer",
            "bootstrap_servers": "localhost:9092",
        },
    }
    ConnectorConfig(**config_data)


def test_validate_connector_type_value():
    """Validates the connect.type field"""
    config_data = {
        "type": "invalid-value",
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
        "name": "Kafka Producer Config",
        "config": {
            "type": "KafkaProducer",
            "bootstrap_servers": "localhost:9092",
        },
    }
    with pytest.raises(ValidationError):
        ConnectorConfig(**config_data)


@pytest.mark.parametrize(
    "config_file_name",
    [
        "kafka-consumer-connector.yaml",
        "kafka-producer-connector.yaml",
        "nats-client-connector.yaml",
        "rest-endpoint-connector.yaml"
    ],
)
def test_load_connector_configuration(resources_path: str, config_file_name: str):
    """Loads a connector configuration from file"""
    file_path = os.path.join(resources_path, config_file_name)
    load_connector_configuration(file_path)


def test_load_connector_configuration_invalid_path(resources_path: str):
    """Validates that an exception is raised when a config file path is invalid"""
    file_path = os.path.join(resources_path, "not-a-real-file.yaml")
    with pytest.raises(FileNotFoundError):
        load_connector_configuration(file_path)
