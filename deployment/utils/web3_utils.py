#! /usr/bin/python3
"""
_Web3 Utils functions_
"""

import json
from typing import Any


def hex_default(obj: Any) -> str:
    if isinstance(obj, bytes):
        return obj.hex()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def print_w3_logs(w3_obj: Any) -> None:
    """
    _Prints on `stdout` web3 logs in a `json` style_

    Args:
        w3_obj (Web3): _Web3 object_
    """
    print(
        json.dumps(
            dict(w3_obj), indent=2, sort_keys=False, default=hex_default
        )
    )
