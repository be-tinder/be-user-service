import importlib
import pkgutil
from typing import List, Dict, Any
from fastapi import APIRouter


def _is_api_router(module_name: str) -> APIRouter | None:
    """
    Check if the module specified by `module_name` has a 'router'
    attribute that is an instance of FastAPI's APIRouter.

    Args:
        module_name (str): The full dotted module name to check.

    Returns:
        APIRouter | None: The APIRouter instance if found; otherwise, None.
    """
    try:
        module = importlib.import_module(module_name)
        router = getattr(module, "router", None)
        return router if isinstance(router, APIRouter) else None
    except (ModuleNotFoundError, ImportError, AttributeError):
        return None


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
        if hasattr(package, "__path__"):
            for _, module_name, ispkg in pkgutil.walk_packages(
                package.__path__, prefix=path + "."
            ):
                modules.append(module_name)
                if ispkg:
                    modules.extend(_deep_import(module_name))
    except ModuleNotFoundError:
        return []

    return list(set(modules))  # Remove potential duplicates


def import_api_routers(root_path: str) -> List[Dict[str, Any]]:
    """
    Discover and return all APIRouter instances under `root_path`.

    Args:
        root_path (str): The base package path to search for API routers.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing APIRouter instances and module names.
    """
    all_modules = _deep_import(root_path)
    routers = []

    for module_name in all_modules:
        router = _is_api_router(module_name)
        if router:
            routers.append({"router": router, "module": module_name.split(".")[-1]})

    return routers
