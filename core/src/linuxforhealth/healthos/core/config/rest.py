"""
rest.py
Pydantic models used to support REST endpoint connector configurations.
"""
from pydantic import BaseModel, Field
from typing import Literal


class RestEndpointConfig(BaseModel):
    """
    Configures a REST endpoint used to receive or transmit data
    """

    type: Literal["RestEndpoint"]
    url: str = Field(
        description="Defines the endpoint used to receive inbound data via "
        + "a HTTP POST or PUT",
    )
    http_method: str = Field(regex="^(post|put)$", default="post")
