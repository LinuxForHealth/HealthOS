"""
connector package

The connector package contains the core service's inbound and outbound data connectors.
Package level imports are provided for convenience.
"""
from .nats import (
    get_jetstream_core_client,
    create_jetstream_core_client,
    PublishDataModel,
)
from .rest import create_inbound_connector_route
