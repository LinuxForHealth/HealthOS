import argparse
from linuxforhealth.healthos.core.config import load_connector_configuration
import pprint
import os
import sys

CLI_DESCRIPTION = """
The LinuxForHealth HealthOS Core Module starts inbound and outbound data connectors used for data processing.
"""


def parse_args(args):
    """
    Parses command line arguments
    :param args: The arguments captured from sys.argv
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(prog="LFH-HealthOS-Core",
                                     description=CLI_DESCRIPTION,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", "--file", help="The path to the connector configuration file.")
    return parser.parse_args(args)


def main():
    """
    Launches the core application.
    The application accepts a single argument, -f or --file, which specifies the path to the connector configuration
    file.
    :raises: FileNotFoundError if the configuration file is not found.
    """
    args = parse_args(sys.argv[1:])
    if not os.path.exists(args.file):
        raise FileNotFoundError(f"Unable to load configuration file {args.file}")

    config = load_connector_configuration(args.file)
    pprint.pprint(config.dict())


if __name__ == "__main__":
    main()
