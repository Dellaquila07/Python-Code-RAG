import importlib
import sys

from contextlib import contextmanager


@contextmanager
def patched_module(module_name, module_obj):
    """Temporarily register a module in sys.modules."""
    previous = sys.modules.get(module_name)
    sys.modules[module_name] = module_obj
    try:
        yield
    finally:
        if previous is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous


def import_fresh(module_name: str):
    """Import a module after removing any previously cached version."""
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)
