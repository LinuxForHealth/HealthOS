from linuxforhealth.healthos.core.config.rest import RestEndpointConfig
from pydantic import ValidationError
import pytest


def test_validate_minimum_input():
    """Validates the minimal config data required for a REST endpoint configuration"""
    config_data = {"type": "RestEndpoint"}
    config = RestEndpointConfig(**config_data)

    assert config.relative_endpoint_url == "/ingress"
    assert config.host_name == "localhost"
    assert config.host_port == 5002
    assert config.host_protocol == "http"
    assert config.http_method == "POST"


@pytest.mark.parametrize("field_name", ["http_method", "host_protocol"])
def test_validate_regexs_validation_error(field_name):
    """Validates that ValidationErrors are raised if a regex backed field has an invalid value"""
    config_data = {"type": "RestEndpoint", field_name: "INVALID"}
    with pytest.raises(ValidationError):
        RestEndpointConfig(**config_data)


@pytest.mark.parametrize("field_name, field_value", [
    ("http_method", "POST"),
    ("http_method", "GET"),
    ("http_method", "PUT"),
    ("http_method", "DELETE"),
    ("host_protocol", "http"),
    ("host_protocol", "https"),
])
def test_validate_regexs(field_name, field_value):
    """Validates that regex backed fields do not raise a ValidationError for valid values"""
    config_data = {"type": "RestEndpoint", field_name: field_value}
    RestEndpointConfig(**config_data)
