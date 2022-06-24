"""
test_version.py Tests project version metadata
"""
from packaging import version


def test_version():
    from linuxforhealth.core.connect import __version__
    assert version.parse(__version__) > version.parse("0.0.0")
