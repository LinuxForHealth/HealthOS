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

    @property
    def inbound_rest_connectors(self) -> List[ConnectorConfig]:
        """Returns inbound rest connectors or an empty list"""
        return self._find_connectors("inbound", "RestEndpoint")

    @property
    def inbound_nats_connectors(self) -> List[ConnectorConfig]:
        """Returns inbound nats connectors or an empty list"""
        return self._find_connectors("inbound", "NatsClient")

    @property
    def inbound_kafka_connectors(self) -> List[ConnectorConfig]:
        """Returns inbound kafka connectors or an empty list"""
        return self._find_connectors("inbound", "KafkaConsumer")

    def _find_connectors(
        self, connector_type: str, config_type: str
    ) -> List[ConnectorConfig]:
        """Returns inbound connectors of a specific type and config type"""
        connectors: List[ConnectorConfig] = []

        for c in self.connectors:
            if c.type == connector_type and c.config.type == config_type:
                connectors.append(c)
        return connectors
