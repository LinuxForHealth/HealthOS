from linuxforhealth.healthos.core.config.rest import RestEndpointConfig
from pydantic import ValidationError
import pytest


def test_validate_minimum_input():
    config_data = {"type": "RestEndpoint"}
    config = RestEndpointConfig(**config_data)

    assert config.relative_endpoint_url == "/ingress"
    assert config.host_name == "localhost"
    assert config.host_port == 5002
    assert config.host_protocol == "http"
    assert config.http_method == "POST"


@pytest.mark.parametrize("field_name", ["http_method", "host_protocol"])
def test_validate_regexs(field_name):
    config_data = {"type": "RestEndpoint", field_name: "INVALID"}
    with pytest.raises(ValidationError):
        RestEndpointConfig(**config_data)
