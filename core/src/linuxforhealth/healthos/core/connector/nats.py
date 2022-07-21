"""
nats.py

Implements NATS connectors, or clients for ingress, core, and egress.
The ingress client pulls data from external systems.
The core client submits data to "internal" NATS subjects which power the HealthOS core pipeline.
The egress client transmits data to external systems.
"""
import logging
from typing import List

import nats
from nats.js import JetStreamContext, JetStreamManager
from nats.js.errors import NotFoundError

from ..config import ConnectorConfig, CoreServiceConfig, get_core_configuration
from .processor import PublishDataModel, process_data

logger = logging.getLogger(__name__)

# client used for core messaging
jetstream_core_client: JetStreamContext | None = None

# clients used for messaging with external systems
jetstream_clients: List[JetStreamContext] | None = None

# underlying jetstream connections, used to provide a clean shutdown
jetstream_connections: List[nats.NATS] | None = None


async def create_jetstream_core_client(url: str, stream_name: str, subject: str):
    """
    Creates a NATS client for the Core service.
    Additional operations include:
    - creating the target stream and subject if they do not exist
    - associating the target subject with the NATS client instance

    :param url: The NATS server url, including protocol, host, and port.
    :param stream_name: The NATS server stream name
    :param subject: The NATS server subject which is published to
    :return:
    """
    nats_connection: nats.NATS
    jetstream_mgr: JetStreamManager

    try:
        nats_connection = await nats.connect(url)
    except Exception as ex:
        logger.error("An error occurred connecting to the Jetstream server")
        logger.error(f"{ex}")
        raise

    logger.info(f"Internal NATS Client Connected on {url}")
    jetstream_mgr: JetStreamManager = nats_connection.jsm()

    try:
        await jetstream_mgr.stream_info(stream_name)
    except NotFoundError:
        logger.info("HealthOS Stream Not Found Within NATS Jetstream Server")
        logger.info("Creating HealthOS Stream")
        await jetstream_mgr.add_stream(name=stream_name, subjects=[subject])

    global jetstream_core_client
    jetstream_core_client = nats_connection.jetstream()

    connections = get_jetstream_connections()
    connections.append(nats_connection)


async def create_inbound_jetstream_clients(inbound_nats_clients: List[ConnectorConfig]):
    """
    Creates inbound jetstream clients from specified configurations.

    :param inbound_nats_clients: The inbound NATS Jetstream configurations
    """
    global jetstream_clients
    jetstream_clients = []

    for c in inbound_nats_clients:
        subscription_subjects = c.config.subjects
        connection_config = c.config.dict(exclude={"type", "subjects"})
        try:
            nats_connection = await nats.connect(**connection_config)
        except Exception as ex:
            logger.error(
                "An error occurred connecting to the external Jetstream server"
            )
            logger.error(f"{ex}")
            raise

        logger.info(
            f"NATS Client Connected to external Jetstream server {c.config.servers}"
        )

        jetstream_client = nats_connection.jetstream()
        jetstream_clients.append(jetstream_client)

        for s in subscription_subjects:
            await jetstream_client.subscribe(s, cb=inbound_connector_callback)
            logger.info(f"Subscribed to subject {s}")

        connections = get_jetstream_connections()
        connections.append(nats_connection)


def get_jetstream_core_client() -> JetStreamContext:
    """Returns the NATS jetstream client used for core messaging"""
    global jetstream_core_client
    return jetstream_core_client


def get_jetstream_clients() -> List[JetStreamContext]:
    """Returns the NATS jetstream client used for external messaging"""
    global jetstream_clients
    return jetstream_clients or []


def get_jetstream_connections() -> List[nats.NATS]:
    """Returns the NATS Jetstreams connections which are currently in use"""
    global jetstream_connections
    if jetstream_connections is None:
        jetstream_connections = []
    return jetstream_connections


async def inbound_connector_callback(msg):
    """
    This callback function is used to consolidate inbound message processing.
    Messages received are published to the core service's internal messaging system

    :param msg: The message from the internal system
    """
    await msg.ack()

    service_config: CoreServiceConfig = get_core_configuration()
    messaging_config = service_config.app.messaging

    msg_str = msg.data.decode("utf-8")
    publish_model: PublishDataModel = await process_data(msg_str)

    logger.debug(f"published message to {messaging_config.inbound_subject}")
    logger.debug(f"message metadata {publish_model.dict()}")
