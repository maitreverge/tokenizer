#! /usr/bin/python3
"""
_module_doc_
"""

import asyncio

from web3 import AsyncWeb3, Web3


# async def main() -> None:
def main() -> None:
    """
    Main function
    """
    # web = Web3(Web3.HTTPProvider("https://rpc.sepolia.org"))

    w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
    print(w3.is_connected())  # True

    

if __name__ == "__main__":
    main()