import argparse
from ..config import load_core_configuration, CoreServiceConfig

CLI_DESCRIPTION = """
The LinuxForHealth HealthOS Core CLI starts Core OS services including:
- connectors
- data persistence
- audit
- observability
"""


def _start_core_services(args):
    core_config: CoreServiceConfig = load_core_configuration(args.f)
    for c in core_config.connectors:
        pass


def create_arg_parser():
    arg_parser = argparse.ArgumentParser(
        prog="LFH HealthOS Core",
        description=CLI_DESCRIPTION,
    )

    sub_parsers = arg_parser.add_subparsers()

    # core
    core = sub_parsers.add_parser("core", help="starts LFH HealthOS Core Services")
    core.add_argument("-f", help="The path to the core configuration file.")
    core.set_defaults(func=_start_core_services)

    # admin
    admin = sub_parsers.add_parser("admin")
    admin_operations = admin.add_mutually_exclusive_group()
    admin_operations.add_argument("-l", help="Lists core service tasks")
    admin_operations.add_argument("-r", help="Restarts a core service task")
    admin_operations.add_argument("-s", help="Stops a core service task")

    return arg_parser
