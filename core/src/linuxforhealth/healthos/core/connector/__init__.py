"""
connector package

The connector package contains the core service's inbound and outbound data connectors.
Package level imports are provided for convenience.
"""
from .nats import (
    get_core_jetstream_client,
    create_core_jetstream_client,
    PublishDataModel,
)
from .rest import create_inbound_connector_route
