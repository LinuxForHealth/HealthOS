"""
cli.py

HealthOS Core Service CLI "entrypoint". The CLI supports the following subparsers:
- core: starts the core service
- admin: admin cli for core services
"""
import argparse
from typing import List
import logging.config
import sys
from linuxforhealth.healthos.core.app import core_startup

CLI_DESCRIPTION = """
The LinuxForHealth HealthOS Core CLI manages Core OS services including:
- connectors
- data persistence
- audit
- observability
"""

logger = logging.getLogger(__name__)


def main(received_arguments: List[str] = None):
    """
    Executes the CLI programs.
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
    """
    Creates the CLI argument parser for the HealthOS core and admin programs.
    """
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
    core.set_defaults(func=core_startup)

    # admin
    admin = sub_parsers.add_parser(
        "admin", help="provides access to running tasks and services."
    )
    admin_operations = admin.add_mutually_exclusive_group()
    admin_operations.add_argument("-l", help="Lists core service tasks")
    admin_operations.add_argument("-r", help="Restarts a core service task")
    admin_operations.add_argument("-s", help="Stops a core service task")
    # admin_operations.set_defaults(func=admin_operation)

    return arg_parser


if __name__ == "__main__":
    # parsing system arguments and passing them in so that we can:
    # - bootstrap test cases easily
    # - print help information if no arguments are provided
    system_arguments = sys.argv[1:] if sys.argv else []
    main(system_arguments)
