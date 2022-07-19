"""
test_connector_config.py

Test cases for the Connector configuration model.
"""
import pytest
from pydantic import ValidationError

from linuxforhealth.healthos.core.config.connector import ConnectorConfig


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
            "url": "/ingress",
            "http_method": "post",
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
