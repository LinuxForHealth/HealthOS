"""
nats.py

Implements Nats connectors, or clients for ingress, core, and egress.
The ingress client pulls data from external systems.
The core client submits data to "internal" Nats subjects which power the HealthOS core pipeline.
The egress client transmits data to external systems.
"""
import nats
from nats.js import JetStreamManager, JetStreamContext
import logging
from nats.js.errors import NotFoundError

logger = logging.getLogger(__name__)


core_jetstream_client: JetStreamContext


async def create_core_client(host: str, port: int, subject: str):
    """
    Creates the core NATS client used to publish to core service subjects.

    :param host: The NATS server host name or ip address.
    :param port: The NATS server port number.
    :param subject: The NATS server subject which is published to
    :return:
    """
    nats_connection = None
    jetstream_mgr = None

    try:
        nats_connection = await nats.connect(f"nats://{host}:{port}")
    except Exception as ex:
        logger.error("An error occurred connecting to the Jetstream server")
        logger.error(f"{ex}")
        raise

    logger.info(f"Internal Nats Client Connected on {host}:{port}")
    jetstream_mgr: JetStreamManager = nats_connection.jsm()

    try:
        await jetstream_mgr.stream_info("healthos")
    except NotFoundError:
        logger.info("HealthOS Stream Not Found Within Nats Jetstream Server")
        logger.info("Creating HealthOS Stream")
        await jetstream_mgr.add_stream(name="healthos", subjects=["ingress"])

    global core_jetstream_client
    core_jetstream_client = nats_connection.jetstream()
