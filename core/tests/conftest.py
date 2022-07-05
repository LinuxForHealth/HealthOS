from tests.support import resources_directory
import pytest


@pytest.fixture
def resources_path() -> str:
    """returns the path to the test resources directory"""
    return resources_directory
