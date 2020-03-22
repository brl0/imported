"""Tests configuration."""

import pytest
from scripttest import TestFileEnvironment


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


@pytest.fixture
def env():
    yield TestFileEnvironment(cwd=".",)
