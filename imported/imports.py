"""Inspect imports."""
from inspect import getmembers, ismodule
from types import ModuleType
from typing import Dict, Optional, Union


version_types = Union[str, int, float]


def get_version(m: ModuleType) -> Optional[version_types]:
    """Get conventional version attribute from module, if any."""
    VERSION_ATTRS = [
        "__version__",
        "VERSION",
        "version",
    ]
    for v in VERSION_ATTRS:
        if hasattr(m, v):
            return getattr(m, v)
    return None


def has_version(m: ModuleType) -> bool:
    """Check if module has a convential version attribute."""
    if get_version(m):
        return True
    return False  # pragma: no cover


def get_imported(context: dict) -> Dict[str, Optional[version_types]]:
    """Create list of imported modules in given context.

    Only outputs modules from given context that have
    conventional version attributes.
    Context is typically globals() or locals().
    """
    visited = dict()

    def _process_module(*args):
        ((name, module),) = args
        n = getattr(module, "__name__", name)
        if ismodule(module) and n not in visited:
            visited.update({n: get_version(module)})
            try:
                [*map(_process_module, getmembers(module, ismodule))]
            except:  # pragma: no cover
                pass

    [*map(_process_module, context.items())]

    return dict([*filter(lambda _: _[1] is not None, visited.items())])


def get_imports(context: dict) -> str:
    """Create string list of imported modules in given context.

    Only outputs modules from given context that have
    conventional version attributes.
    Context is typically globals() or locals().
    """
    imports = get_imported(context)
    return ",".join(sorted(set(imports.keys())))
