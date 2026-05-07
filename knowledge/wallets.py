#! /usr/bin/python3
"""
_module_doc_
"""

from eth_account import Account


def main() -> None:
    """
    Main function
    """

    # https://eth-account.readthedocs.io/en/latest/eth_account.html#eth_account.account.Account.create
    account = Account.create("KEYSMASH FJAFJKLDSKF7JKFDJ 1530")

    print(f"Account Public key = {account.address}")
    print(f"Account Private key = {account.key}\ntype={type(account.key)}")
    print(f"{account.key.hex()}")
    


if __name__ == "__main__":
    main()