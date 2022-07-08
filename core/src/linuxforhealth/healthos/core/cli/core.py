"""
core.py
Implements the core_startup function supported by the core CLI
"""
from ..config import load_core_configuration, CoreServiceConfig
from pydantic import ValidationError
from fastapi import FastAPI
import uvicorn
import logging
import logging.config
import yaml
import sys

logger = logging.getLogger(__name__)

app: FastAPI


def core_startup(args):
    """
    Starts the HealthOS core service using the service config.
    Bootstrapping tasks include:
    - loading and parsing the service configuration
    - configuring logging

    Exits and returns a 1 status code if the service config is not found or invalid

    :param args: parsed CLI arguments
    """
    try:
        # load service config
        core_config: CoreServiceConfig = load_core_configuration(args.f)
    except (FileNotFoundError, ValidationError) as e:
        msg = f"Unable to start HealthOS Core Service\n An exception occurred {e}"
        logger.error(msg)
        sys.exit(1)
    try:
        # configure logging
        with open(core_config.logging_config, "r") as f:
            logging_config = yaml.load(f, Loader=yaml.FullLoader)
            logging.config.dictConfig(logging_config)
    except FileNotFoundError:
        logger.warning(
            f"Unable to load logging configuration from {core_config.logging_config}"
        )
        logger.warning("Falling back to basic config")
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s)",
            level=logging.INFO,
        )

    logger.info("Starting HealthOS Core service")
    global app
    app = FastAPI(
        title="LinuxForHealth HealthOS Core", description="HealthOS Core Service"
    )

    uvicorn_params = {
        "app": app,
        "host": core_config.app.host,
        "port": core_config.app.port,
        "reload": core_config.app.debug,
    }
    uvicorn.run(**uvicorn_params)
