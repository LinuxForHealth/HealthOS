from pydantic import BaseModel, Field, root_validator, parse_obj_as
from .kafka import KafkaConsumerConfig, KafkaProducerConfig
from .nats import NatsClientConfig
from .rest import RestEndpointConfig
from typing import Dict, List
import yaml


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
    id: str = Field(description="The connector id used to locate the service for admin operations")
    name: str = Field(description="The user defined connector name")
    config: KafkaProducerConfig | KafkaConsumerConfig | NatsClientConfig | RestEndpointConfig = Field(
        description="The connector configuration settings"
    )

    class Config:
        extra = "ignore"
        frozen = True

    @root_validator(skip_on_failure=True)
    def validate_connector_type_config(cls, values: Dict) -> Dict:
        """
        Ensures that the Connector type, inbound or outbound, is compatible with the associated config.
        :param cls: The class instance
        :param values: The current config values
        :return: the current values
        :raises: ValueError if
        """
        connector_type = values.get("type")
        config_type = values.get("config", {}).type
        supported_configs = cls._connector_type_config.get(connector_type)

        if config_type not in supported_configs:
            msg = f"{config_type} is not a valid {connector_type} connector type"
            raise ValueError(msg)

        return values


def load_connector_configuration(file_path: str) -> List[ConnectorConfig]:
    """
    Loads connector configurations (YAML) from file

    :param file_path: The path to the YAML configuration
    :return: ConnectorConfigFile model
    """
    with open(file_path) as fp:
        connector_data = yaml.safe_load(fp)

    if isinstance(connector_data, dict):
        connector_data = [connector_data]

    connector_configs: List[ConnectorConfig] = [ConnectorConfig(**c) for c in connector_data]
    return connector_configs
