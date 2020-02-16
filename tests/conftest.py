"""Tests configuration."""

import pytest


class Module:
    """Sample module."""

    import sys
    __version__ = '1'


@pytest.fixture
def module():
    """Pytest fixture."""
    yield Module
