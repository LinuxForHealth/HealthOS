"""
connector package

The connector package contains the core service's inbound and outbound data connectors.
Package level imports are provided for convenience.
"""
from .nats import (create_jetstream_client, create_jetstream_core_client,
                   get_jetstream_client, get_jetstream_core_client)
from .processor import PublishDataModel
from .rest import create_inbound_connector_route
