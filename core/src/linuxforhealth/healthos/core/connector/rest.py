"""
rest.py

Implements Rest API connectors
"""
from fastapi.routing import APIRouter
import logging

logger = logging.getLogger(__name__)


def create_inbound_connector_route(url: str, http_method: str) -> APIRouter:
    """
    Creates an API route for an inbound RestEndpoint connector.

    :param url: The target URL
    :param http_method: The http method to support
    :return: Fast API APIRouter
    """

    async def execute_route():
        logger.debug("received inbound payload")
        logger.debug("publishing to NATS")
        logger.debug("received NATS Ack")
        return {"status": "ok"}

    router = APIRouter(prefix=url)
    router_func = getattr(router, http_method)
    router_func("")(execute_route)
    return router
