"""Tests configuration."""

import pytest


class Module:
    """Sample module."""

    import sys

    __version__ = "1"


@pytest.fixture
def module():
    """Pytest module fixture."""
    yield Module


@pytest.fixture
def context():
    """Pytest module fixture."""
    import sys

    yield locals()
