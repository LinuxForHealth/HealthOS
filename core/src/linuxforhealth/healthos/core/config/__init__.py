"""
config.py
The config module contains the Pydantic domain models used to support the core service configuration file.
Package level imports are provided for convenience.
"""
import yaml

from .core import CoreServiceConfig, ConnectorConfig
from .connector import ConnectorConfig
from typing import List

core_service_config: CoreServiceConfig


def load_core_configuration(file_path: str):
    """
    Loads the core service configurations (YAML) from file

    :param file_path: The path to the YAML configuration
    :return: CoreServiceConfig model
    """
    with open(file_path) as fp:
        core_data = yaml.safe_load(fp)

    global core_service_config
    core_service_config = CoreServiceConfig(**core_data)


def get_core_configuration() -> CoreServiceConfig:
    """Returns the core service configuration"""
    return core_service_config

