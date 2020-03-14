"""Inspect imports."""
from functools import lru_cache
from inspect import getmembers, ismodule
from types import ModuleType
from typing import Dict, Optional, Union

from decorators import *

version_types = Union[str, int, float]


def get_version(m: ModuleType) -> Optional[version_types]:
    """Get conventional version attribute from module, if any."""
    VERSION_ATTRS = [
        '__version__',
        'VERSION',
        'version',
    ]
    for v in VERSION_ATTRS:
        if hasattr(m, v):
            return getattr(m, v)
    return None


def has_version(m: ModuleType) -> bool:
    """Check if module has a convential version attribute."""
    if get_version(m):
        return True
    return False


visited = set()


@rec_cycle
def process_module(m: ModuleType):
    output = {}
    n = getattr(m, '__name__')
    visited.add(n)
    print(n)
    if has_version(m):
        version = get_version(m)
        output.update({n: version})
    for name, val in getmembers(m):
        n = getattr(m, '__name__', name)
        if ismodule(val) and n not in visited:
            output.update(process_module(val))
    return output


def get_imported(context: dict) -> Dict[str, Optional[version_types]]:
    """Create list of imported modules in given context.

    Only outputs modules from given context that have
    conventional version attributes.
    Context is typically globals() or locals().
    """
    imports = {}
    try:
        for val in context.values():
            if ismodule(val):
                imports.update(process_module(val))
    except AttributeError:
        pass
    return imports


def get_imports(context: dict, limit: int = 0) -> str:
    """Create string list of imported modules in given context.

    Only outputs modules from given context that have
    conventional version attributes.
    Context is typically globals() or locals().
    """
    imports = get_imported(context, limit)
    return ",".join(sorted(set(imports.keys())))


if __name__ == '__main__':
    import os
    import sys
    from pprint import pprint
    from pathlib import Path
    import pandas as pd
    import numpy as np
    from decorators import *
    pprint(get_imported(globals()))
