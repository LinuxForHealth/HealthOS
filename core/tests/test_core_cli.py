import pytest
from linuxforhealth.healthos.core.cli.main import main
from linuxforhealth.healthos.core.cli.core import uvicorn
from contextlib import nullcontext as does_not_raise
from tests.support import resources_directory
from unittest.mock import patch


@pytest.mark.parametrize(
    "arguments, expectation",
    [
        # invalid path results in a SystemExit
        (
            ["core", "-f", "/invalid/path/core-service.yaml"],
            pytest.raises(SystemExit),
        ),
        # invalid service configuration data results in a SystemExit
        (
            [
                "core",
                "-f",
                f"{resources_directory}/service-config/invalid-core-service.yaml",
            ],
            pytest.raises(SystemExit),
        ),
        # valid file
        (
            ["core", "-f", f"{resources_directory}/service-config/core-service.yaml"],
            does_not_raise(),
        ),
        # invalid path to a logging config falls back to basic config, doesn't exit
        (
            [
                "core",
                "-f",
                f"{resources_directory}/service-config/core-service-invalid-logging.yaml",
            ],
            does_not_raise(),
        ),
    ],
)
def test_core_cli_system_exit(arguments, expectation):
    """
    Validates that the core CLI returns a non-zero status code for exceptional situations.
    Uvicorn is patched to ensure that the ASGI server does not start.
    :param arguments: parameterized CLI arguments
    :param expectation: used to parameterize if exceptions are raised, or if code executes successfully
    """
    with expectation:
        with patch.object(uvicorn, "run", return_value=None):
            main(arguments)
