"""Tests configuration."""

import pytest


class Module:
    """Sample module."""

    __version__ = '1'


@pytest.fixture
def module():
    yield Module
