"""
app.py

Defines the data model used to support the Core service's "app" configuration.
The Core service app provides the event loop used for core service components such as connectors, as
well as Admin API interfaces.
"""
from pydantic import BaseModel, Field
from typing import Optional


class CoreApp(BaseModel):
    """
    The configuration settings for the Core service application.
    The Core service application supports the Admin API interface and the optional REST endpoint connector.
    These settings map to the underlying uvicorn app used to support the Core service's Fast API application.
    """

    port: int = Field(
        description="The port associated with the application's API server. Defaults to 8080.",
        default=8080,
    )
    host: str = Field(
        description="The host name or ip address bound to the server socket. Defaults to localhost.",
        default="localhost",
    )
    debug: bool = Field(
        description="When set to True, the server runs in debug mode supporting `hot reloads`. "
        + "Defaults to False.",
        default=False,
    )
    inbound_message_subject: str = Field(
        description="The Nats Subject used to receive all inbound messages",
        default="ingress"
    )
    ssl_keyfile: Optional[str] = Field(description="The path to a SSL key file.")
    ssl_keyfile_password: Optional[str] = Field(
        description="The password used to decrypt the SSL key."
    )
    ssl_certfile: Optional[str] = Field(description="The SSL certificate file.")
    ssl_version: Optional[str] = Field(description="The SSL version to use.")
    ssl_cert_reqs: Optional[str] = Field(
        description="Whether client certificate is required."
    )
    ssl_ca_certs: Optional[str] = Field(description="The CA certificates file.")
    ssl_ciphers: Optional[str] = Field(description="The SSL ciphers to use.")
