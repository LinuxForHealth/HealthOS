from pydantic import BaseModel, Field
from typing import Literal


class RestEndpointConfig(BaseModel):
    """
    Configures a REST endpoint used to receive inbound data
    """

    type: Literal["RestEndpoint"]
    host_protocol: str = Field(
        description="The protocol used to access the endpoint.",
        regex="^(http|https)$",
        default="http",
    )
    host_name: str = Field(
        default="localhost",
        description="The hostname or IP address for the REST Endpoint",
    )
    host_port: int = Field(
        description="The port number used on the REST API host", default=5002
    )
    relative_endpoint_url: str = Field(
        default="/ingress",
        description="Defines the relative endpoint used to receive inbound data via "
        + "a HTTP POST",
    )
    http_method: str = Field(regex="^(POST|PUT|GET|DELETE)$", default="POST")
