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

logger = logging.getLogger(__name__)


core_jetstream_client: JetStreamContext


class PublishDataModel(BaseModel):
    """
    Model used to publish data to NATS Jetstream
    """

    data_id: uuid.UUID = Field(
        description="The unique id for the data message", default=uuid.uuid4()
    )
    data: str = Field(description="The data payload")
    content_type: ContentType = Field(description="The data content-type")


async def create_core_jetstream_client(
    host: str, port: int, stream_name: str, subject: str
):
    """
    Creates a NATS client for the Core service.
    Additional operations include:
    - creating the target stream and subject if they do not exist
    - associating the target subject with the NATS client instance

    :param host: The NATS server host name or ip address.
    :param port: The NATS server port number.
    :param stream_name: The NATS server stream name
    :param subject: The NATS server subject which is published to
    :return:
    """
    nats_connection: nats.NATS
    jetstream_mgr: JetStreamManager

    try:
        nats_connection = await nats.connect(f"nats://{host}:{port}")
    except Exception as ex:
        logger.error("An error occurred connecting to the Jetstream server")
        logger.error(f"{ex}")
        raise

    logger.info(f"Internal NATS Client Connected on {host}:{port}")
    jetstream_mgr: JetStreamManager = nats_connection.jsm()

    try:
        await jetstream_mgr.stream_info(stream_name)
    except NotFoundError:
        logger.info("HealthOS Stream Not Found Within NATS Jetstream Server")
        logger.info("Creating HealthOS Stream")
        await jetstream_mgr.add_stream(name="healthos", subjects=[subject])

    global core_jetstream_client
    core_jetstream_client = nats_connection.jetstream()


def get_core_jetstream_client() -> JetStreamContext:
    """Returns the NATS jetstream client used for core messaging"""
    return core_jetstream_client
