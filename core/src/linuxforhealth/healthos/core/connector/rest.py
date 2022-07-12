"""
rest.py

Implements Rest API connectors
"""
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
import logging
from ..config import get_core_configuration
from ..connector import get_core_jetstream_client, PublishDataModel
from pydantic import BaseModel, Field
from ..detect import validate_message
from nats.js.errors import NoStreamResponseError
import uuid
import json


logger = logging.getLogger(__name__)


class RestEndpointRequest(BaseModel):
    """RestEndpoint Request Object"""

    data: str = Field(description="Contains the request data payload")

    class Config:
        extra = "ignore"
        frozen = True
        schema_extra = {
            "example": {
                "data": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*270*0001*005010X279A1~BHT*0022*13*10001234*20200929*1319~HL*1**20*1~NM1*PR*2*UNIFIED INSURANCE CO*****PI*842610001~HL*2*1*21*1~NM1*1P*2*DOWNTOWN MEDICAL CENTER*****XX*2868383243~HL*3*2*22*0~TRN*1*1*1453915417~NM1*IL*1*DOE*JOHN****MI*11122333301~DMG*D8*19800519~DTP*291*D8*20200101~EQ*30~SE*13*0001~GE*1*0001~IEA*1*000010216~"
            }
        }


async def endpoint_template(
    request_model: RestEndpointRequest,
    core_config=Depends(get_core_configuration),
    jetstream_client=Depends(get_core_jetstream_client),
):
    """
    Provides an asyncio based template for core connector RestEndpoint implementations.
    Includes configuration and NATS Jetstream dependencies to support publishing to the core NATS Jetstream server.

    Response Codes:
    - 200 for successful processing
    - 400 if the input message's cannot be parsed
    - 500 if an error occurs transmitting to NATS

    :param request_model: The RestEndpoint request model.
    :param core_config: The Service core configuration.
    :param jetstream_client: Configured NATS Jetstream client.
    :return: a 200 status code with a response payload containing the request status and id
    """
    data_id = str(uuid.uuid4())
    logger.debug("Generated {data_id} for incoming payload")

    try:
        content_type = validate_message(request_model.data)
    except ValueError:
        msg = "request payload is invalid"
        logger.error(msg)
        raise HTTPException(status_code=400, detail=msg)

    publish_model = PublishDataModel(
        data_id=data_id, data=request_model.data, content_type=content_type
    )
    message_payload = json.dumps(publish_model.json()).encode()

    messaging_config = core_config.app.messaging
    try:
        publish_ack = await jetstream_client.publish(
            subject=messaging_config.inbound_subject,
            stream=messaging_config.stream_name,
            payload=message_payload,
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
        return {"status": "received", "id": data_id}


def create_inbound_connector_route(url: str, http_method: str) -> APIRouter:
    """
    Creates an API route for an inbound RestEndpoint connector.

    :param url: The target URL
    :param http_method: The http method to support
    :return: Fast API APIRouter
    """
    router = APIRouter(prefix=url)
    router_func = getattr(router, http_method)
    router_func("")(endpoint_template)
    return router
