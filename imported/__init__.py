"""imported module."""

from types import ModuleType
from typing import Dict, Optional, Union

__version__ = '0.0.2'

version_types = Union[str, int, float]


def get_version(m: ModuleType) -> Optional[version_types]:
    """Get conventional version attribute from module, if any."""
    if hasattr(m, '__version__'):
        return getattr(m, '__version__')
    if hasattr(m, 'VERSION'):
        return getattr(m, 'VERSION')
    return None


def has_version(m: ModuleType) -> bool:
    """Check if module has a convential version attribute."""
    if get_version(m):
        return True
    return False


def get_imported(context: dict) -> Dict[str, Optional[version_types]]:
    """Create list of imported modules in given context.

    Only outputs modules from given context that have
    conventional version attributes.
    Context is typically globals() or locals().
    """
    try:
        imports = {
            val.__name__: get_version(val)
            for name, val in context.items()
            if isinstance(val, ModuleType) and has_version(val)
        }
    except Exception:
        imports = {}
    return imports


def get_imports(context: dict) -> str:
    """Create string list of imported modules in given context.

    Only outputs modules from given context that have
    conventional version attributes.
    Context is typically globals() or locals().
    """
    imports = get_imported(context)
    return ",".join(sorted(set(imports.keys())))
