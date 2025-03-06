import importlib
import pkgutil
from typing import List

from fastapi import APIRouter


def _is_api_router(module_name: str) -> bool:
    """
    Check if the module specified by `module_name` has a 'router'
    attribute that is an instance of FastAPI's APIRouter.

    Args:
        module_name (str): The full dotted module name to check.

    Returns:
        bool: True if the module contains an APIRouter instance under
              the attribute 'router'; otherwise, False.
    """
    try:
        module = importlib.import_module(module_name)
    except Exception:
        return False

    router = getattr(module, "router", None)
    return isinstance(router, APIRouter)


def _deep_import(path: str) -> List[str]:
    """
    Recursively traverse the package at `path` to gather all module names,
    including sub-packages and modules.

    Args:
        path (str): The dotted path of the package to traverse.

    Returns:
        List[str]: A list of fully qualified module names.
    """
    modules = []
    try:
        package = importlib.import_module(path)
    except ModuleNotFoundError:
        return modules

    modules.append(path)
    if hasattr(package, "__path__"):
        for _, module_name, ispkg in pkgutil.walk_packages(package.__path__, prefix=path + "."):
            modules.append(module_name)
            if ispkg:
                modules.extend(_deep_import(module_name))
    return list(set(modules))


def import_api_routers(root_path: str) -> List[str]:
    """
    Discover and return all module names under `root_path` that define
    an APIRouter instance (assigned to the attribute 'router').

    Args:
        root_path (str): The base package path to search for API routers.

    Returns:
        List[str]: A list of module names containing an APIRouter.
    """
    all_modules = _deep_import(root_path)
    return [module for module in all_modules if _is_api_router(module)]
