"""
rest.py
Pydantic models used to support REST endpoint connector configurations.
"""
from typing import Literal

from pydantic import BaseModel, Field


class RestEndpointConfig(BaseModel):
    """
    Configures a REST endpoint used to receive or transmit data
    """

    type: Literal["RestEndpoint"] = "RestEndpoint"
    url: str = Field(
        description="Defines the endpoint used to receive inbound data via "
        + "a HTTP POST or PUT",
    )
    http_method: str = Field(regex="^(post|put)$", default="post")

    class Config:
        extra = "forbid"
        frozen = True
