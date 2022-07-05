from pydantic import BaseModel, Field
from typing import List, Optional, Union, Tuple, Literal


class NatsClientConfig(BaseModel):
    """
    NATS Client (Core or Jetstream) configuration
    """
    type: Literal["NatsClient"]

    servers: str | List[str] = Field(
        description="URL to NATS server instance(s).", default=["nats://localhost:4222"]
    )
    name: Optional[str] = Field(
        description="name is an optional name label which will be sent to the server on "
        + "CONNECT to identify the client"
    )
    pedantic: bool = Field(
        description="Pedantic signals the server whether it should be doing further validation "
        + "of subjects.",
        default=False,
    )
    verbose: bool = Field(
        default=False,
        description=" Verbose signals the server to send an OK ack for commands successfully "
        + "processed by the server.",
    )
    allow_reconnect: bool = Field(
        default=True,
        description="AllowReconnect enables reconnection logic to be used when we encounter "
        + "a disconnect from the current server.",
    )
    connect_timeout: int = Field(
        default=2, ge=0, description="Connection timeout setting."
    )
    reconnect_time_wait: int = Field(
        default=2,
        ge=0,
        description="The amount of time to wait before making another connection attempt.",
    )
    max_reconnect_attempts: int = Field(
        default=60,
        ge=0,
        description="The maximum number of reconnection attempts to make.",
    )
    ping_interval: int = Field(
        default=120,
        ge=0,
        description="PingInterval is the period at which the client will be sending ping commands to the server, disabled if 0 or negative.",
    )
    max_outstanding_pings: int = Field(
        default=2,
        ge=0,
        description="The maximum number of pending ping commands that can be awaiting a response before raising an ErrStaleConnection error.",
    )
    dont_randomize: bool = Field(
        default=False,
        description="Is an Option to turn off randomizing the server pool.",
    )
    flusher_queue_size: int = Field(default=1024, ge=0)
    no_echo: bool = Field(
        default=False,
        description="NoEcho configures whether the server will echo back messages that are sent on this connection if we also have matching subscriptions.",
    )
    tls_hostname: Optional[str]
    user: Optional[str] = Field(
        description="User sets the username to be used when connecting to the server."
    )
    password: Optional[str] = Field(
        description="Password sets the password to be used when connecting to a server."
    )
    token: Optional[str] = Field(
        description="Token sets the token to be used when connecting to a server."
    )
    drain_timeout: int = Field(
        default=30, description="Set the timeout for draining a connection.", ge=0
    )
    user_credentials: Optional[Union[str, Tuple[str, str]]] = Field(
        description="Convenience field which takes a filename for a user's JWT and a file name for the user's " +
                    "private Nkey seed"
    )
    nkeys_seed: Optional[str] = Field(description="Seed value used for NATS 2.0 Auth")
    inbox_prefix: Union[str, bytes] = Field(
        default=b"_INBOX",
        description="Allows the default _INBOX prefix to be customized.",
    )
    pending_size: int = Field(
        default=2_097_152,
        description="The maximum size of the data that can be buffered.",
        ge=0,
    )
    flush_timeout: Optional[float] = Field(
        default=10.0,
        description="Allows a flush operation to have an associated timeout.",
        ge=0,
    )

    class Config:
        extra = "ignore"
        frozen = True
