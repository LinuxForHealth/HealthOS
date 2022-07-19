"""
connector.py

Pydantic domain models for Core Service connectors.
"""
from typing import Annotated, Dict, Union

from pydantic import BaseModel, Field, root_validator

from .kafka import KafkaConsumerConfig, KafkaProducerConfig
from .nats import NatsClientConfig
from .rest import RestEndpointConfig


class ConnectorConfig(BaseModel):
    """
    Models a single connector configuration within a configuration file.
    """

    # maps connector type to compatible configs
    _connector_type_config = {
        "inbound": ("KafkaConsumer", "NatsClient", "RestEndpoint"),
        "outbound": ("KafkaProducer", "NatsClient", "RestEndpoint"),
    }
    type: str = Field(
        description="Indicates if the connector is used for receiving (inbound) or "
        + "transmitting (outbound) data",
        regex="^(inbound|outbound)$",
    )
    id: str = Field(
        description="The connector id used to locate the service for admin operations"
    )
    name: str = Field(description="The user defined connector name")
    config: Annotated[
        Union[
            KafkaConsumerConfig,
            KafkaProducerConfig,
            NatsClientConfig,
            RestEndpointConfig,
        ],
        Field(discriminator="type"),
    ]

    class Config:
        extra = "forbid"
        frozen = True

    @root_validator(skip_on_failure=True)
    def validate_connector_type_config(cls, values: Dict) -> Dict:
        """
        Ensures that the Connector type, inbound or outbound, is compatible with the associated config.
        :param cls: The class instance
        :param values: The current config values
        :return: the current values
        :raises: ValueError if the connector type and config type are invalid
        """
        connector_type = values.get("type")
        config_type = values.get("config", {}).type
        supported_configs = cls._connector_type_config.get(connector_type)

        if config_type not in supported_configs:
            msg = f"{config_type} is not a valid {connector_type} connector type"
            raise ValueError(msg)

        return values
