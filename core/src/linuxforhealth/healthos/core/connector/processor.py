"""
processor.py

Common data processing implementations for HealthOS connectors.
"""
import json
import logging
import uuid
from typing import Optional

from nats.js import JetStreamContext
from nats.js.errors import NoStreamResponseError
from pydantic import BaseModel, Field

from ..config import get_core_configuration
from ..detect import (
    ContentType,
    ContentTypeError,
    DataValidationError,
    detect_content_type,
    validate_message,
)

logger = logging.getLogger(__name__)


class PublishDataModel(BaseModel):
    """
    Model used to publish data to NATS Jetstream
    """

    data_id: uuid.UUID = Field(
        description="The unique id for the data message", default=uuid.uuid4()
    )
    data: str = Field(description="The data payload")
    error: Optional[str] = Field(description="Contains data processing errors.")
    content_type: Optional[ContentType] = Field(description="The data content-type")


async def process_data(msg: str) -> PublishDataModel:
    """
    The core function used to process data received by an inbound HealthOS connector.

    :param msg: The input data message
    :return: The PublishDataModel containing the validated data and associated metadata
    """
    publish_data = {}
    try:
        publish_data["data"] = msg
        content_type = detect_content_type(msg)
        publish_data["content_type"] = content_type
        validate_message(msg)
    except (ContentTypeError, DataValidationError, KeyError, AttributeError) as ex:
        msg = f"Exception occurred processing data {ex}"
        logger.error(msg)
        publish_data["error"] = str(ex)

    # publish data to HealthOS Core Messaging
    publish_model = PublishDataModel(**publish_data)
    message_payload = json.dumps(publish_model.json()).encode()
    messaging_config = get_core_configuration().app.messaging

    # workaround for circular import
    from .nats import get_jetstream_core_client

    core_client: JetStreamContext = get_jetstream_core_client()

    if publish_model.error is not None:
        nats_subject = messaging_config.error_subject
    else:
        nats_subject = messaging_config.ingress_subject

    try:
        publish_ack = await core_client.publish(
            subject=nats_subject,
            stream=messaging_config.stream_name,
            payload=message_payload,
        )
    except NoStreamResponseError as nsre:
        msg = f"Unable to publish message to {messaging_config.stream_name}:{nats_subject}"
        logger.error(msg)
        logger.error(f"NATS NoStreamResponseError {nsre}")
        raise
    else:
        logger.debug(
            f"publishing to NATS {messaging_config.stream_name}:{nats_subject}"
        )
        logger.debug(f"received NATS Ack {publish_ack}")
        logger.debug(f"returning status = received, id = {publish_model.data_id}")

    return publish_model
