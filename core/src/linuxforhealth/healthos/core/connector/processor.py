"""
processor.py

Common data processing implementations for HealthOS connectors.
"""
import json
import logging
import uuid

from nats.js import JetStreamContext
from nats.js.errors import NoStreamResponseError
from pydantic import BaseModel, Field

from ..config import get_core_configuration
from ..detect import ContentType, validate_message

logger = logging.getLogger(__name__)


class PublishDataModel(BaseModel):
    """
    Model used to publish data to NATS Jetstream
    """

    data_id: uuid.UUID = Field(
        description="The unique id for the data message", default=uuid.uuid4()
    )
    data: str = Field(description="The data payload")
    content_type: ContentType = Field(description="The data content-type")


async def process_data(msg: str) -> PublishDataModel:
    """
    The core function used to process data received by an inbound HealthOS connector.

    :param msg: The input data message
    :return: The PublishDataModel containing the validated data and associated metadata
    """
    try:
        content_type = validate_message(msg)
    except ValueError:
        msg = "request payload is invalid"
        logger.error(msg)
        raise

    # publish data to HealthOS Core Messaging
    publish_model = PublishDataModel(data=msg, content_type=content_type)
    message_payload = json.dumps(publish_model.json()).encode()
    messaging_config = get_core_configuration().app.messaging

    # workaround for circular import
    from .nats import get_jetstream_core_client

    core_client: JetStreamContext = get_jetstream_core_client()

    try:
        publish_ack = await core_client.publish(
            subject=messaging_config.inbound_subject,
            stream=messaging_config.stream_name,
            payload=message_payload,
        )
    except NoStreamResponseError as nsre:
        msg = f"Unable to publish message to {messaging_config.stream_name}:{messaging_config.inbound_subject}"
        logger.error(msg)
        logger.error(f"NATS NoStreamResponseError {nsre}")
        raise
    else:
        logger.debug(
            f"publishing to NATS {messaging_config.stream_name}:{messaging_config.inbound_subject}"
        )
        logger.debug(f"received NATS Ack {publish_ack}")
        logger.debug(f"returning status = received, id = {publish_model.data_id}")

    return publish_model
