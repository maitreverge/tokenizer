"""
_module_doc_
"""

from web3 import Web3
import os
import sys
from utils import print_w3_logs
from utils import is_virtual_env_sys
from solcx import install_solc, compile_source
import solcx
from eth_account import Account

from dotenv import load_dotenv

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import SignAndSendRawMiddlewareBuilder

load_dotenv()

SEPOLIA_ENTRYPOINT = os.getenv("SEPOLIA_ENTRYPOINT")
TEST_CONTRACT = os.getenv("TEST_CONTRACT")
MY_PRIVATE_KEY = os.getenv("MY_PRIVATE_KEY")
MY_PUBLIC_KEY = os.getenv("MY_PUBLIC_KEY")


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
    try:
        print(f"=== Checking Smart Contract Compiler ===")
        assert solcx.get_solc_version() == ["<Version('0.8.35')>"]
        print(f"=== Smart Contract Compiler already installed ===")
    except Exception as e:
        print(f"=== Smart Contract Compiler not installed. Installing... ==")
        install_solc(version="0.8.35")
        print(f"=== Installed Contract Compiler ===")
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

        openzeppelin_path = os.path.abspath("./node_modules")

        compiled_contract = compile_source(
            content,
            output_values=["abi", "bin"],
            solc_version="0.8.35",
            import_remappings=[
                f"@openzeppelin/={openzeppelin_path}/@openzeppelin/"
            ],
            allow_paths=[openzeppelin_path],
        )

        # retrieve the contract interface
        contract_id, contract_interface = compiled_contract.popitem()

        # get bytecode / bin
        bytecode = contract_interface["bin"]

        # get abi
        abi = contract_interface["abi"]

        account: LocalAccount = Account.from_key(MY_PRIVATE_KEY)
        w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)
        w3.eth.default_account = account.address

        Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = Greeter.constructor().transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print(tx_receipt)

        # print(f"COMPIILED : {compiled_contract}")


def main() -> None:
    """
    Main function
    """
    if not pass_init_checks():
        sys.exit(1)

    try:
        w3 = Web3(Web3.HTTPProvider(SEPOLIA_ENTRYPOINT))
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
