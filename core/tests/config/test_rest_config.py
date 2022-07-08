from linuxforhealth.healthos.core.config.rest import RestEndpointConfig
from pydantic import ValidationError
import pytest
from typing import Dict


@pytest.fixture
def config_data() -> Dict:
    return {
        "type": "RestEndpoint",
        "url": "/ingress",
        "http_method": "POST",
    }


def test_validate_minimum_input(config_data):
    """Validates the minimal config data required for a REST endpoint configuration"""
    config = RestEndpointConfig(**config_data)
    assert config.url == "/ingress"
    assert config.http_method == "POST"


@pytest.mark.parametrize("field_name", ["http_method"])
def test_validate_regexs_validation_error(config_data, field_name):
    """Validates that ValidationErrors are raised if a regex backed field has an invalid value"""
    config_data[field_name] = "INVALID"
    with pytest.raises(ValidationError):
        RestEndpointConfig(**config_data)


@pytest.mark.parametrize(
    "field_name, field_value",
    [
        ("http_method", "POST"),
        ("http_method", "PUT"),
    ],
)
def test_validate_regexs(config_data, field_name, field_value):
    """Validates that regex backed fields do not raise a ValidationError for valid values"""
    config_data[field_name] = field_value
    RestEndpointConfig(**config_data)
