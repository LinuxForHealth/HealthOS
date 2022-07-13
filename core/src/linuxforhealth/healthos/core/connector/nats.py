"""
nats.py

Implements NATS connectors, or clients for ingress, core, and egress.
The ingress client pulls data from external systems.
The core client submits data to "internal" NATS subjects which power the HealthOS core pipeline.
The egress client transmits data to external systems.
"""
import nats
from nats.js import JetStreamManager, JetStreamContext
import logging
from nats.js.errors import NotFoundError
from pydantic import BaseModel, Field
import uuid
from ..detect import ContentType
from typing import List

logger = logging.getLogger(__name__)

# client used for core messaging
jetstream_core_client: JetStreamContext

# client used for messaging with external systems
jetstream_client: JetStreamContext


class PublishDataModel(BaseModel):
    """
    Model used to publish data to NATS Jetstream
    """

    data_id: uuid.UUID = Field(
        description="The unique id for the data message", default=uuid.uuid4()
    )
    data: str = Field(description="The data payload")
    content_type: ContentType = Field(description="The data content-type")


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
        await jetstream_mgr.add_stream(name="healthos", subjects=[subject])

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
        await jetstream_client.subscribe(s)
        logger.info(f"Subscribed to subject {s}")


def get_jetstream_core_client() -> JetStreamContext:
    """Returns the NATS jetstream client used for core messaging"""
    return jetstream_core_client


def get_jetstream_client() -> JetStreamContext:
    """Returns the NATS jetstream client used for external messaging"""
    return jetstream_client
