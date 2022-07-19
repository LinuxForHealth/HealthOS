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

from ..config import CoreServiceConfig, get_core_configuration
from .processor import PublishDataModel, process_data

logger = logging.getLogger(__name__)

# client used for core messaging
jetstream_core_client: JetStreamContext | None = None

# client used for messaging with external systems
jetstream_client: JetStreamContext | None = None


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


async def create_jetstream_client(urls: List[str], subjects: List[str]):
    """
    Creates a NATS client which is subscribed to a one or more subjects on a specific host.

    :param urls: The NATS server urls, including protocol, host, and port.
    :param subjects: The NATS server subjects to subscribe to.
    """
    nats_connection: nats.NATS
    jetstream_mgr: JetStreamManager

    try:
        nats_connection = await nats.connect(urls)
    except Exception as ex:
        logger.error("An error occurred connecting to the external Jetstream server")
        logger.error(f"{ex}")
        raise

    logger.info(f"NATS Client Connected to external Jetstream server {urls}")

    global jetstream_client
    jetstream_client = nats_connection.jetstream()

    for s in subjects:
        await jetstream_client.subscribe(s, cb=inbound_connector_callback)
        logger.info(f"Subscribed to subject {s}")


def get_jetstream_core_client() -> JetStreamContext:
    """Returns the NATS jetstream client used for core messaging"""
    global jetstream_core_client
    return jetstream_core_client


def get_jetstream_client() -> JetStreamContext:
    """Returns the NATS jetstream client used for external messaging"""
    global jetstream_client
    return jetstream_client


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
