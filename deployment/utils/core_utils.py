#! /usr/bin/python3
"""
_Core utils functions_
"""

import sys

def is_virtual_env_sys() -> bool:
    """
    Detects virtual env by comparing `sys.base_prefix != sys.prefix`
    False otherwise.

    Returns:
        bool: _Is the programs runs in a venv_
    """
    return sys.base_prefix != sys.prefix

