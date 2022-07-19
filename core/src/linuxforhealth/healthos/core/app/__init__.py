"""
app.py

Implements the Fast API application used to support the core service.
"""
import logging
import sys
from asyncio import Task
from functools import partial
from typing import Dict, List

import uvicorn
import yaml
from fastapi import FastAPI
from pydantic import ValidationError

from ..config import (ConnectorConfig, CoreServiceConfig,
                      get_core_configuration, load_core_configuration)
from ..connector import (create_inbound_connector_route,
                         create_inbound_jetstream_clients,
                         create_jetstream_core_client,
                         create_kafka_consumer_connector)
from .admin import router as admin_router

logger = logging.getLogger(__name__)

APP_BASE_URL = "/healthos/core"

# the Fast API application for the Core Service
core_service_app: FastAPI = FastAPI(
    title="LinuxForHealth HealthOS Core App", description="HealthOS Core Service"
)

# provides a lookup for current core service tasks
core_service_tasks: Dict[str, Task] = {}


def core_startup(args):
    """
    Starts the HealthOS core service using the service config.
    Bootstrapping tasks include:
    - loading and parsing the service configuration
    - registering app startup handlers
    - registering app shutdown handlers

    Exits and returns a 1 status code if the service config is not found or invalid

    :param args: parsed CLI arguments
    """

    try:
        # load service config
        load_core_configuration(args.f)
        core_config: CoreServiceConfig = get_core_configuration()
    except (FileNotFoundError, ValidationError) as e:
        msg = f"Unable to start HealthOS Core Service\n An exception occurred {e}"
        logger.error(msg)
        sys.exit(1)
    else:
        # use partial functions to align with the Fast API/starlette "no-arg" event handler functions

        # configure logging
        startup_logging = partial(configure_logging, core_config.logging_config)
        core_service_app.add_event_handler("startup", startup_logging)

        # configure endpoints
        startup_endpoints = partial(
            configure_inbound_endpoints,
            core_service_app,
            core_config.inbound_rest_connectors,
        )
        core_service_app.add_event_handler("startup", startup_endpoints)

        # configure internal NATS (Jetstream)
        startup_internal_nats = partial(
            create_jetstream_core_client,
            core_config.app.messaging.url,
            core_config.app.messaging.stream_name,
            core_config.app.messaging.inbound_subject,
        )
        core_service_app.add_event_handler("startup", startup_internal_nats)

        # configure external/inbound NATS (Jetstream)
        startup_inbound_jetstream = partial(
            create_inbound_jetstream_clients, core_config.inbound_nats_connectors
        )
        core_service_app.add_event_handler("startup", startup_inbound_jetstream)

        # configure Kafka consumer for external cluster
        startup_kafka_consumers = partial(
            create_kafka_consumer_connector, core_config.inbound_kafka_connectors
        )
        core_service_app.add_event_handler("startup", startup_kafka_consumers)

        uvicorn_params = {
            "app": core_service_app,
            "host": core_config.app.host,
            "port": core_config.app.port,
            "reload": core_config.app.debug,
        }
        logger.info("Starting HealthOS Core service")
        uvicorn.run(**uvicorn_params)


def configure_logging(file_path: str):
    """
    Configures logging using the specified yaml file.
    If an error occurs loading the yaml file, the basic logging config is used.

    :param file_path: The file path to the yaml logging configuration
    """
    try:
        # configure logging
        with open(file_path, "r") as f:
            logging_config = yaml.load(f, Loader=yaml.FullLoader)
            logging.config.dictConfig(logging_config)
    except FileNotFoundError:
        logger.warning(f"Unable to load logging configuration from {file_path}")
        logger.warning("Falling back to basic config")
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )


def configure_inbound_endpoints(
    app: FastAPI, inbound_rest_connectors: List[ConnectorConfig]
):
    """
    Configures the inbound endpoints for the Core service's internal Fast API application.
    Endpoints configured include:
    - the /admin endpoints used to monitor and manage tasks
    - the "optional" ingress endpoints which function as data connectors

    :param app: The Fast API application
    :param inbound_rest_connectors: List of inbound RestEndpoint connectors
    """
    app.include_router(admin_router, prefix=APP_BASE_URL)
    logger.info(f"Adding Admin Rest Endpoints to {APP_BASE_URL}/{admin_router.prefix}")

    for c in inbound_rest_connectors:
        r = create_inbound_connector_route(c.config.url, c.config.http_method)
        app.include_router(r, prefix=APP_BASE_URL)
        logger.info(
            f"Adding Inbound RestEndpoint Connector to {APP_BASE_URL}/{r.prefix}"
        )
