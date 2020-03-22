"""Test for imported module."""

import imported


def test_get_version(module):
    """Test get_version function."""
    assert imported.get_version(module) == "1"


def test_has_version(module):
    """Test has_version function."""
    assert imported.has_version(module)


def test_get_imported(context):
    """Test get_imported function."""
    assert imported.get_imported(context)
    from pathlib import Path
    import os
    import sys

    results = imported.get_imported(locals())
    assert 'sys' in results.keys()


def test_get_imports(context):
    """Test get_imports module."""
    assert imported.get_imports(context)
