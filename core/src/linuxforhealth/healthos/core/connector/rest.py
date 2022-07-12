"""
rest.py

Implements Rest API connectors
"""
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
import logging
from ..config import get_core_configuration
from ..connector import get_core_jetstream_client
from nats.js.errors import NoStreamResponseError

logger = logging.getLogger(__name__)


def create_inbound_connector_route(url: str, http_method: str) -> APIRouter:
    """
    Creates an API route for an inbound RestEndpoint connector.

    :param url: The target URL
    :param http_method: The http method to support
    :return: Fast API APIRouter
    """

    async def execute_route(
        core_config=Depends(get_core_configuration),
        jetstream_client=Depends(get_core_jetstream_client),
    ):
        logger.debug("received inbound payload")

        messaging_config = core_config.app.messaging
        try:
            publish_ack = await jetstream_client.publish(
                subject=messaging_config.inbound_subject,
                stream=messaging_config.stream_name,
                payload="hello world!".encode(),
            )
        except NoStreamResponseError as nsre:
            msg = f"Unable to publish message to {messaging_config.stream_name}:{messaging_config.inbound_subject}"
            logger.error(msg)
            logger.error(f"NATS NoStreamResponseError {nsre}")
            raise HTTPException(status_code=500, detail=msg)
        else:
            logger.debug(
                f"publishing to NATS {messaging_config.stream_name}:{messaging_config.inbound_subject}"
            )
            logger.debug(f"received NATS Ack {publish_ack}")
            return {"status": "ok"}

    router = APIRouter(prefix=url)
    router_func = getattr(router, http_method)
    router_func("")(execute_route)
    return router
