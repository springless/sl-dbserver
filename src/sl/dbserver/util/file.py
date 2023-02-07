import importlib.util
import os
from os.path import exists
import json
from typing import Any


def module_path(path: str) -> str:
    """Takes in a path that can be either a regular path, a module, or a module followed by a path.
    They can take the form:

        <module>:<path>
        <module>
        <path>

    For example, if the module `sl.module` exists at `/home/user/proj/src/sl/module`, the following
    are example paths and what they would map to:

        # Regular absolute path
        > module_path('/home/user/proj/src/sl/module/subfolder/file.txt')
        '/home/user/proj/src/sl/module/subfolder/file.txt'

        # Module followed by a path
        > module_path('sl.module:subfolder/file.txt')
        '/home/user/proj/src/sl/module/subfolder/file.txt'

        # The path portion can start anywhere, even if it includes a "module" folder in it
        > module_path('sl:module/subfolder/file.txt')
        '/home/user/proj/src/sl/module/subfolder/file.txt'

        # Path directly to the module
        > module_path('sl.module')
        '/home/user/proj/src/sl/module'

        # Relative paths are unchanged
        > module_path('../some_file.txt')
        '../some_file.txt'

    It will not change paths that do not include the module component. If a path does not include
    the colon and has no slashes it will attempt to load the path as a module, and otherwise it
    will return the path unchanged.
    """
    if ":" in path:
        # If a colon does exist then we know for a fact that the lefthand side is meant to be a python module
        module, append = path.split(":")
        dir_path = os.path.dirname(importlib.util.find_spec(module).origin)
        # Return the directory path plus the apended value
        return os.path.join(dir_path, os.path.normpath(append))
    # If there are no slashes and no colon, attempt to read the path as a module
    elif not ("/" in path or "\\" in path):
        return os.path.dirname(importlib.util.find_spec(path).origin)

    # Otherwise this does not conform to anything we recognize; return the path unchanged
    return path


def json_to_str(val: Any, *, sort_keys: bool = True, indent: int = 2) -> str:
    """Dumps to json string using default values. Primarily used for
    writing to files. `val` should already be json-serializable
    """
    return json.dumps(val, sort_keys=sort_keys, indent=indent)


def str_to_json(val: str) -> dict[Any, Any]:
    return json.loads(val)
