"""
app.py

Defines the data model used to support the Core service's "app" configuration.
The Core service app provides the event loop used for core service components such as connectors, as
well as Admin API interfaces.
"""
from pydantic import BaseModel, Field
from typing import Optional


class CoreAppMessaging(BaseModel):
    """
    The configuration settings for the Core service application's messaging component.
    """

    url: str = Field(
        description="The URL for the core application messaging service (NATS Jetstream).",
        default="nats://localhost:4222",
    )
    stream_name: str = Field(
        description="The messaging stream name. Defaults to healthos.",
        default="healthos",
    )
    inbound_subject: str = Field(
        description="The messaging subject used to receive all inbound/ingress messages",
        default="ingress",
    )


class CoreApp(BaseModel):
    """
    The configuration settings for the Core service application.

    The Core service application supports the Admin API interface, optional REST connectors, and provides the
    event loop for all Core service tasks.
    """

    host: str = Field(
        description="The host name or ip address bound to the server socket. Defaults to localhost.",
        default="localhost",
    )
    port: int = Field(
        description="The port associated with the application's API server. Defaults to 8080.",
        default=8080,
    )
    debug: bool = Field(
        description="When set to True, the server runs in debug mode supporting `hot reloads`. "
        + "Defaults to False.",
        default=False,
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
    messaging: CoreAppMessaging = Field(
        description="Configuration for the application's internal messaging "
        + "system",
        default=CoreAppMessaging(),
    )
