"""
core.py
The top level domain model for the Core service configuration.
"""
import yaml
from pydantic import BaseModel

from .connector import ConnectorConfig
from .app import CoreApp
from typing import List


class CoreServiceConfig(BaseModel):
    """
    The LFH HealthOS Core Service Configuration.
    Supports configuration settings pertaining to:
    - connectors
    - auditing
    - data synchronization
    - observability and metrics
    """

    connectors: List[ConnectorConfig]
    app: CoreApp
    # TODO: implement support for
    # auditing:
    # data synchronization:
    # observability/metrics:
    logging_config: str

    class Config:
        extra = "ignore"
        frozen = True


def load_core_configuration(file_path: str) -> CoreServiceConfig:
    """
    Loads the core service configurations (YAML) from file

    :param file_path: The path to the YAML configuration
    :return: CoreServiceConfig model
    """
    with open(file_path) as fp:
        core_data = yaml.safe_load(fp)

    core_config = CoreServiceConfig(**core_data)
    return core_config
