"""
_module_doc_
"""

from web3 import AsyncWeb3, Web3
import json
import os
import sys
from utils import print_w3_logs
from utils import is_virtual_env_sys
from solcx import install_solc, compile_source
import solcx


def pass_init_checks() -> bool:
    if not is_virtual_env_sys():
        print(f"You are not running inside a virtual environment")
        # sys.exit(1)
        return False
        # TODO : Make logs for how to run the program in virtual env

    return True


def install_contract_compiler() -> None:
    """
    _Function to install the `py-solc-x` contract compiler_
    """
    # try:
    #     print(f"=== Checking Smart Contract Compiler ===")
    #     solcx.get_solc_version()
    #     print(f"=== Smart Contract Compiler already installed ===")
    # except Exception as e:
    #     print(f"=== Smart Contract Compiler not installed. Installing... ==")
    #     install_solc(version='latest')
    #     print(f"=== Installed Contract Compiler ===")
    # install_solc()
    install_solc(version='0.8.35')
    solcx.set_solc_version("0.8.35")
    # print(f"Installable version : \n{solcx.get_installable_solc_versions()}")
    print(f"Installed version = {solcx.get_installed_solc_versions()}")


def upload_contract(w3: Web3) -> None:
    """
    Function to first interract with uploading a eazy smart contract

    Args:
        w3 (Web3): _description_
    """
    # try:
    with open("../code/test_contract/Token_42_Base.sol", "r") as test_contract:
        content = test_contract.read()
        print(f"CONTRACT OUTPUT : \n\n===\n{content}\n===\n")

        # compiled_contract = compile_source(content,
        #     output_values=["abi", "bin"],
        #     solc_version='0.8.35'
        # )
        oz_path = os.path.abspath("./node_modules")

        compiled_contract = compile_source(
            """
            // SPDX-License-Identifier: GPL-3.0
            pragma solidity ^0.8.35;

            import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

            // Base contract inherits fromthe standart ERC20 object
            contract Token_42_Base is ERC20 {
                constructor() ERC20("Token_42_Base", "T4B") {
                    _mint(msg.sender, 4242);
                }
            }
            """ ,
            output_values=["abi", "bin"],
            solc_version='0.8.35',
            import_remappings=[f"@openzeppelin/={oz_path}/@openzeppelin/"],
            allow_paths=[oz_path]
        )
        print(f"COMPIILED : {compiled_contract}")


def main() -> None:
    """
    Main function
    """
    if not pass_init_checks():
        sys.exit(1)

    try:
        w3 = Web3(
            Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com")
        )
        assert (
            w3.is_connected()
        ), "Web3 node failed. Please check the node connector and try again"

        # last_block = w3.eth.get_transaction(
        #     "0xc8dd810c5286ee8f72ee4dcff30903b230c047b33bab76e34207f298a01b38ce"
        # )

        # print_w3_logs(last_block)

        install_contract_compiler()
        upload_contract(w3)
    except Exception as e:
        print(f"Error {e}")


if __name__ == "__main__":
    main()
