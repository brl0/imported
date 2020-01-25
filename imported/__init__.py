"""imported module"""

def has_version(m):
    """Check if module has version attribute."""
    try:
        if m.__version__:
            return True
    except Exception:
        pass
    try:
        if m.VERSION:
            return True
    except Exception:
        pass
    return False


def get_imports(context):
    """Create string list of imported modules.

    Only outputs modules that have conventional version attributes.
    """
    imports = [
        val.__name__ for name, val in context.items()
        if isinstance(val, types.ModuleType) and has_version(val)
    ]
    imports = set(imports)
    imports = sorted(imports)
    imports = ",".join(imports)
    return imports
