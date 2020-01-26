"""Test for imported module."""

import imported


def test_get_version(module):
    assert imported.get_version(module) == '1'


def test_has_version(module):
    assert imported.has_version(module)


def test_get_imported(module):
    imported.get_imported(module)


def test_get_imports(module):
    imported.get_imports(module)
