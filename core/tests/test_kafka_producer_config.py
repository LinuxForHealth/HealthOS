"""
test_kafka_producer_config.py

Tests the Kafka Producer configuration model
"""
import pytest
from typing import Dict, List
from linuxforhealth.healthos.core.config import KafkaProducerConfig
from pydantic import ValidationError


@pytest.fixture
def config_data() -> Dict:
    return {
        "bootstrap_servers": "localhost:9092"
    }


def test_validate_minimum_input(config_data: Dict):
    config = KafkaProducerConfig(**config_data)
    assert config.bootstrap_servers == "localhost:9092"


def test_required_field_validation(config_data: Dict):
    """Validates that ValidationError is raised when required fields are not set"""
    del config_data["bootstrap_servers"]
    with pytest.raises(ValidationError):
        KafkaProducerConfig(**config_data)


@pytest.mark.parametrize(
    "field_name",
    [
        "acks",
        "compression_type",
        "security_protocol",
        "sasl_mechanism"
    ],
)
def test_regex_validations_exception(config_data: Dict, field_name: str):
    """Validates regex validations raise a ValidationError when an invalid value is present"""
    config_data[field_name] = "invalid"

    with pytest.raises(ValidationError):
        KafkaProducerConfig(**config_data)


@pytest.mark.parametrize(
    "field_name,valid_values",
    [
        ("acks", ["0", "1", "all"]),
        ("compression_type", ["gzip", "snappy", "lz4"]),
        ("security_protocol", ["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"]),
        ("sasl_mechanism", ["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"]),
    ],
)
def test_regex_validations_valid_values(config_data: Dict, field_name: str, valid_values: List):
    """Validates regex validations raise a ValidationError when an invalid value is present"""
    execution_count = 0

    for v in valid_values:
        config_data[field_name] = v
        KafkaProducerConfig(**config_data)
        execution_count += 1
    else:
        assert execution_count > 0
        assert execution_count == len(valid_values)


def test_validate_defaulting_acks(config_data: Dict):
    """Validates that acks is defaulted correct if idempotence is enabled"""
    config_data["enable_idempotence"] = True
    config = KafkaProducerConfig(**config_data)
    assert config.acks == "all"


def test_validate_idempotence_error(config_data: Dict):
    """Validates that a ValidationError is raised if acks and enable_idempotence settings are not compatible"""
    config_data["acks"] = 0
    config_data["enable_idempotence"] = True
    with pytest.raises(ValidationError):
        KafkaProducerConfig(**config_data)
