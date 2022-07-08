"""
main.py

HealthOS Core Service CLI "entrypoint". The CLI supports the following subparsers:
- core: starts the core service
- admin: admin cli for core services
"""
import argparse
from ..config import load_core_configuration, CoreServiceConfig
from pydantic import ValidationError
from typing import List
import logging
import logging.config
import yaml
import sys

CLI_DESCRIPTION = """
The LinuxForHealth HealthOS Core CLI manages Core OS services including:
- connectors
- data persistence
- audit
- observability
"""

logger = logging.getLogger(__name__)


def _start_core_services(args):
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


def main(received_arguments: List[str] = None):
    """
    Executes the CLI utilities
    :param received_arguments: The arguments from the CLI. Defaults to None
    """
    parser = create_arg_parser()
    args = parser.parse_args(received_arguments)

    if hasattr(args, "func"):
        # execute CLI
        args.func(args)
    else:
        parser.print_help()


def create_arg_parser():
    arg_parser = argparse.ArgumentParser(
        prog="LFH HealthOS Core",
        description=CLI_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub_parsers = arg_parser.add_subparsers()

    # core
    core = sub_parsers.add_parser(
        "core",
        help="starts the LFH HealthOS Core Service using the core configuration file.",
    )
    core.add_argument("-f", help="The path to the core configuration file.")
    core.set_defaults(func=_start_core_services)

    # admin
    admin = sub_parsers.add_parser(
        "admin", help="provides access to running tasks and services."
    )
    admin_operations = admin.add_mutually_exclusive_group()
    admin_operations.add_argument("-l", help="Lists core service tasks")
    admin_operations.add_argument("-r", help="Restarts a core service task")
    admin_operations.add_argument("-s", help="Stops a core service task")

    return arg_parser


if __name__ == "__main__":
    # parsing system arguments and passing them in so that we can:
    # - bootstrap test cases easily
    # - print help information if no arguments are provided
    system_arguments = sys.argv[1:] if sys.argv else []
    main(system_arguments)
