"""
rest.py

Implements Rest API connectors
"""
import logging
import uuid
from typing import Optional

from fastapi import HTTPException
from fastapi.routing import APIRouter
from nats.js.errors import NoStreamResponseError
from pydantic import BaseModel, Field

from ..detect import ContentType
from .processor import process_data

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


class RestEndpointResponse(BaseModel):
    """RestEndpoint Response Object"""

    status: str = Field(
        description="Indicates if the data was received or failed validation.",
        regex="^(received|failed)$",
    )
    content_type: Optional[ContentType] = Field(
        description="The data message's content type. The content type is "
        + "not provided if the data fails validation."
    )
    data_id: str = Field(description="The unique id assigned to the data message")

    class Config:
        extra = "ignore"
        frozen = True
        schema_extra = {
            "example": {
                "status": "received",
                "content_type": "application/EDI-X12",
                "data_id": "8005a343-54dd-43f4-a455-5c38beb545ad",
            }
        }


async def endpoint_template(
    request_model: RestEndpointRequest,
):
    """
    Provides an asyncio based template for core connector RestEndpoint implementations.
    Includes configuration and NATS Jetstream dependencies to support publishing to the core NATS Jetstream server.

    Response Codes:
    - 200 for successful processing which includes valid and invalid data messages
    - 500 if an error occurs transmitting to NATS

    :param request_model: The RestEndpoint request model.
    :return: a 200 status for completed processing or 500 status if an error occurred publishing to NATS
    """
    try:
        publish_model = await process_data(request_model.data)
        logger.debug(
            f"Generated data id {publish_model.data_id} for {publish_model.content_type}"
        )
        return RestEndpointResponse(
            data_id=str(publish_model.data_id),
            content_type=publish_model.content_type,
            status="received",
        )
    except ValueError:
        return RestEndpointResponse(data_id=str(uuid.uuid4()), status="failed")
    except NoStreamResponseError:
        raise HTTPException(
            status_code=500, detail="An internal messaging error occurred"
        )


def create_inbound_connector_route(url: str, http_method: str) -> APIRouter:
    """
    Creates an API route for an inbound RestEndpoint connector.

    :param url: The target URL
    :param http_method: The http method to support
    :return: Fast API APIRouter
    """
    router = APIRouter(prefix=url)
    router_func = getattr(router, http_method)
    router_func("", response_model=RestEndpointResponse)(endpoint_template)
    return router
