"""
test_kafka_consumer_config.py

Tests the Kafka Consumer configuration model
"""
from typing import Dict, List

import pytest
from pydantic import ValidationError

from linuxforhealth.healthos.core.config.kafka import KafkaConsumerConfig


@pytest.fixture
def config_data() -> Dict:
    """Returns the minimal data fixture required for KafkaConsumer configs"""
    return {
        "type": "KafkaConsumer",
        "topics": ["my_topic", "my_other_topic"],
        "bootstrap_servers": "localhost:9092",
    }


def test_validate_minimum_input(config_data: Dict):
    """Validates the minimal fields for the KafkaConsumer"""
    config = KafkaConsumerConfig(**config_data)
    assert config.topics == ["my_topic", "my_other_topic"]
    assert config.bootstrap_servers == "localhost:9092"


@pytest.mark.parametrize("field_to_unset", ["topics", "bootstrap_servers"])
def test_required_field_validation(config_data: Dict, field_to_unset):
    """Validates that ValidationError is raised when required fields are not set"""
    del config_data[field_to_unset]
    with pytest.raises(ValidationError):
        KafkaConsumerConfig(**config_data)


@pytest.mark.parametrize(
    "field_name",
    [
        "security_protocol",
        "isolation_level",
        "sasl_mechanism",
    ],
)
def test_regex_validations_exception(config_data: Dict, field_name: str):
    """Validates regex validations raise a ValidationError when an invalid value is present"""
    config_data[field_name] = "invalid"

    with pytest.raises(ValidationError):
        KafkaConsumerConfig(**config_data)


@pytest.mark.parametrize(
    "field_name,valid_values",
    [
        ("security_protocol", ["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"]),
        ("isolation_level", ["read_uncommitted", "read_committed"]),
        (
            "sasl_mechanism",
            ["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"],
        ),
    ],
)
def test_regex_validations_valid_values(
    config_data: Dict, field_name: str, valid_values: List
):
    """Validates regex validations raise a ValidationError when an invalid value is present"""
    execution_count = 0

    for v in valid_values:
        config_data[field_name] = v
        KafkaConsumerConfig(**config_data)
        execution_count += 1
    else:
        assert execution_count > 0
        assert execution_count == len(valid_values)


def test_default_values(config_data):
    """Validates that fields have expected default values"""
    config = KafkaConsumerConfig(**config_data)
    assert config.fetch_min_bytes == 1
    assert config.fetch_max_bytes == 1
    assert config.max_partition_fetch_bytes == 1048576
    assert config.max_poll_records is None
    assert config.request_timeout_ms == 40000
    assert config.retry_backoff_ms == 100
    assert config.auto_offset_reset == "latest"
    assert config.enable_auto_commit is True
    assert config.auto_commit_interval_ms == 5000
    assert config.check_crcs is True
    assert config.metadata_max_age_ms == 300000
    assert config.partition_assignment_strategy == ["RoundRobinPartitionAssignor"]
    assert config.max_poll_interval_ms == 300000
    assert config.session_timeout_ms == 10000
    assert config.heartbeat_interval_ms == 3000
    assert config.consumer_timeout_ms == 200
    assert config.api_version == "auto"
    assert config.security_protocol == "PLAINTEXT"
    assert config.exclude_internal_topics is True
    assert config.connections_max_idle_ms == 540000
    assert config.isolation_level == "read_uncommitted"
    assert config.sasl_mechanism == "PLAIN"


@pytest.mark.parametrize(
    "field_name",
    [
        "fetch_min_bytes",
        "fetch_max_bytes",
        "max_partition_fetch_bytes",
        "request_timeout_ms",
        "retry_backoff_ms",
        "auto_commit_interval_ms",
        "metadata_max_age_ms",
        "max_poll_interval_ms",
        "session_timeout_ms",
        "heartbeat_interval_ms",
        "consumer_timeout_ms",
        "connections_max_idle_ms",
    ],
)
def test_positive_numeric_fields(config_data: Dict, field_name: str):
    """Validates that each field listed via parameters supports values >= 0"""
    config_data[field_name] = -1
    with pytest.raises(ValidationError):
        KafkaConsumerConfig(**config_data)
