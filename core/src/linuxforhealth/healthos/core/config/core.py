"""
core.py
The top level domain model for the Core service configuration.
"""
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
    # TODO: implement support for:
    # - auditing
    # - data synchronization
    # - observability/metrics
    logging_config: str

    class Config:
        extra = "ignore"
        frozen = True

    @property
    def inbound_connectors(self) -> List[ConnectorConfig]:
        """Returns inbound connectors"""
        return [c for c in self.connectors if c.type == "inbound"]
