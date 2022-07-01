"""
test_kafka_consumer_config.py

Tests the Kafka Consumer configuration model
"""
import pytest
from typing import Dict
from linuxforhealth.healthos.core.config import KafkaConsumerConfig
from pydantic import ValidationError


@pytest.fixture
def config_data() -> Dict:
    return {
        "topics": "A,B,C",
        "bootstrap_servers": ["host-a:9092", "host-b:9093"],
    }


def test_valid_model(config_data):
    m = KafkaConsumerConfig(**config_data)
    assert m.topics == "A,B,C"
    assert m.bootstrap_servers == ["host-a:9092", "host-b:9093"]

    config_data.update({
        "topics": "A",
        "bootstrap_servers": "host-a:9092"
    })

    m = KafkaConsumerConfig(**config_data)
    assert m.topics == "A"
    assert m.bootstrap_servers == "host-a:9092"


@pytest.mark.parametrize("field_name,invalid_value",
                         [
                             ("isolation_level", "invalid"),
                             ("sasl_mechanism", "invalid")
                         ])
def test_regex_validations(config_data, field_name, invalid_value):
    config_data[field_name] = invalid_value

    with pytest.raises(ValidationError):
        KafkaConsumerConfig(**config_data)
