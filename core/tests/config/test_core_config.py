import pytest
import os
from linuxforhealth.healthos.core.config import load_core_configuration


@pytest.mark.parametrize(
    "config_file_name,expected_connector_length",
    [
        ("core-service.yaml", 2),
    ],
)
def test_load_core_service_configuration(
    resources_path: str, config_file_name: str, expected_connector_length: int
):
    """Loads a connector configuration from file"""
    file_path = os.path.join(resources_path, "service-config", config_file_name)
    core_config = load_core_configuration(file_path)
    assert isinstance(core_config.connectors, list)
    assert len(core_config.connectors) == expected_connector_length


def test_load_core_service_configuration_invalid_path(resources_path: str):
    """Validates that an exception is raised when a config file path is invalid"""
    file_path = os.path.join(resources_path, "not-a-real-file.yaml")
    with pytest.raises(FileNotFoundError):
        load_core_configuration(file_path)
