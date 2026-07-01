import sys
import os
import readchar

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.live import Live
from rich.layout import Layout

from dotenv import load_dotenv
from web3 import Web3
from pyperclip import copy as clipboard_cpy
from eth_account import Account

load_dotenv()

WALLETS_FILE = os.getenv("WALLETS_FILE")
SEPOLIA_ENTRYPOINT = os.getenv("SEPOLIA_ENTRYPOINT")

console = Console()

# Minimal ERC-20 ABI: only the functions wallet_manager actually uses.
# balanceOf + decimals (read) for display; transfer (write) for Step 4.
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
]


class Wallet:
    """
    A class representing a cryptocurrency wallet on Sepolia
    """

    def __init__(
        self,
        contract_address: str,
        key: str | None = None,
    ) -> None:

        if not key:
            self.account = Account.create()
        else:
            self.account = Account.from_key(key)

        self._entrypoint_obj = Web3(Web3.HTTPProvider(SEPOLIA_ENTRYPOINT))

        # Build the ERC-20 contract handle used for balance/transfer calls.
        self._contract = self._entrypoint_obj.eth.contract(
            address=contract_address,
            abi=ERC20_ABI,
        )

        # Token decimals are fixed at deployment -> fetch once, cache it.
        self._token_decimals: int = self._contract.functions.decimals().call()

        self._sepolia_balance_wei: int = self._fetch_balance()
        self._my_token_balance_raw: int = self._fetch_my_token_balance()

    def _fetch_balance(self) -> int:
        """
        Fetches the native (SepoliaETH) balance of the wallet in Wei.

        Returns:
            int: The balance in Wei.
        """
        checksum_addr = self._entrypoint_obj.to_checksum_address(
            self.get_public_key()
        )
        return self._entrypoint_obj.eth.get_balance(checksum_addr)

    def _fetch_my_token_balance(self) -> int:
        """
        Fetches the UT42 token balance of the wallet, in the token's
        smallest unit (raw integer, before applying decimals).

        Returns:
            int: The token balance in its smallest unit.
        """
        checksum_addr = self._entrypoint_obj.to_checksum_address(
            self.get_public_key()
        )
        return self._contract.functions.balanceOf(checksum_addr).call()

    def refresh_balance(self) -> None:
        """
        Refreshes BOTH the native and the token balance of the wallet.

        Returns:
            None
        """
        self._sepolia_balance_wei = self._fetch_balance()
        self._my_token_balance_raw = self._fetch_my_token_balance()

    @property
    def sepolia_balance(self) -> float:
        """
        The native balance of the wallet in SepoliaETH (human-readable).

        Returns:
            float: The balance in SepoliaETH.
        """
        return round((self._sepolia_balance_wei / 10**18), 4)

    @property
    def token_balance(self) -> float:
        """
        The UT42 token balance of the wallet (human-readable),
        scaled down by the token's decimals.

        Returns:
            float: The token balance in UT42.
        """
        return round(self._my_token_balance_raw / 10**self._token_decimals, 4)

    def get_public_key(self) -> str:
        """
        Fetches the public key (address) of the wallet.

        Returns:
            str: The public key.
        """
        return str(self.account.address)

    def get_private_key(self) -> str:
        """
        Fetches the private key of the wallet.

        Returns:
            str: The private key.
        """
        return str(self.account.key.hex())


def load_contract_address() -> str:
    """
    Reads CONTRACT_ADDRESS from the environment and validates it.

    Fails fast (exits the program) if:
      - the variable is missing or empty
      - the value is not a valid Ethereum address

    Returns the checksummed address on success.
    """
    address = os.getenv("CONTRACT_ADDRESS")

    if not address:
        sys.exit(
            "❌ CONTRACT_ADDRESS is not defined in your .env file.\n"
            "   Deploy your token with contract_uploader.py first, "
            "then add its address to .env:\n"
            "   CONTRACT_ADDRESS=0x...."
        )

    # in case of malformed address
    if not Web3.is_address(address):
        sys.exit(
            f"❌ CONTRACT_ADDRESS is defined but is not a valid "
            f"Ethereum address:\n   '{address}'"
        )

    # Return checksummed form
    return Web3.to_checksum_address(address)


def create_wallet(wallets: list[Wallet], contract_address: str) -> str:
    """
    Creates a new wallet and adds it to the list.

    Args:
        wallets (list[Wallet]): The list of existing wallets.
        contract_address (str): The deployed UT42 contract address.

    Returns:
        str: A message indicating the result of the operation.
    """
    new_wallet = Wallet(contract_address)

    if WALLETS_FILE is None:
        return "[red]WALLETS_FILE is not configured.[/red]"

    with open(WALLETS_FILE, "a", encoding="utf-8") as wallet_file:
        wallet_file.write(f"{new_wallet.get_private_key()}\n")
    wallets.append(new_wallet)
    return "[bold green]✓ Wallet Created.[/bold green]"


def refresh_balance(wallets: list[Wallet]) -> str:
    """
    Refreshes the balance of all wallets in the list.

    Args:
        wallets (list[Wallet]): The list of existing wallets.

    Returns:
        str: A message indicating the result of the operation.
    """
    for wallet in wallets:
        wallet.refresh_balance()
    return "[bold green]✓ Wallets balance refreshed [/bold green]"


def copy_adress(wallets: list[Wallet], cmd: str) -> str:
    """
    Copies the public address of a wallet to the clipboard.

    Args:
        wallets (list[Wallet]): The list of existing wallets.
        cmd (str): The command string containing the wallet index.

    Returns:
        str: A message indicating the result of the operation.
    """
    nb_wallets = len(wallets)

    try:
        cmd, _index = cmd.split("-")
        index = int(_index)
        if index not in range(nb_wallets):
            return "[bold red]❌ Selected Wallet does not exist [/bold red]"
    except Exception as e:
        return f"[bold red]❌ Invalid command format: {e} [/bold red]"

    wallet_address = wallets[index].get_public_key()

    # Attempt the clipboard copy, fallback to manual copy
    try:
        clipboard_cpy(wallet_address)
        return f"[bold green]✓ Wallet's address `{index}` copied [/bold green]"
    except Exception:
        return f"[bold yellow]Manual Copy (Wallet {index}):[/bold yellow] {wallet_address}"



def copy_key(wallets: list[Wallet], cmd: str) -> str:
    """
    Copies the private key of a wallet to the clipboard.

    Args:
        wallets (list[Wallet]): The list of existing wallets.
        cmd (str): The command string containing the wallet index.

    Returns:
        str: A message indicating the result of the operation.
    """
    nb_wallets = len(wallets)

    try:
        cmd, _index = cmd.split("-")
        index = int(_index)
        if index not in range(nb_wallets):
            return "[bold red]❌ Selected Wallet does not exist [/bold red]"
    except Exception as e:
        return f"[bold red]❌ Invalid command format: {e} [/bold red]"

    private_key = wallets[index].get_private_key()

    # Attempt the clipboard copy, fallback to manual copy
    try:
        clipboard_cpy(private_key)
        return f"[bold green]✓ Wallet's private key `{index}` copied [/bold green]"
    except Exception:
        return f"[bold yellow]Manual Copy (Private Key {index}):[/bold yellow] {private_key}"



def build_table(wallets: list[Wallet]) -> Table:
    """
    Builds a table displaying wallet information.

    Args:
        wallets (list[Wallet]): The list of existing wallets.

    Returns:
        Table: The constructed table.
    """
    table = Table(
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold cyan",
        expand=True,
    )
    table.add_column("Number", style="dim", min_width=8, justify="center")
    table.add_column(
        "Public Address", style="cyan", min_width=20, justify="center"
    )
    table.add_column(
        "Balance (SepoliaETH)", style="green", min_width=18, justify="center"
    )
    table.add_column(
        "Balance (UT42)", style="magenta", min_width=14, justify="center"
    )

    if len(wallets) == 0:
        table.add_row(
            "",
            "[bold red]NO WALLET AVAILABLE.[/bold red]",
            "",
            "",
        )
    else:
        for i, w in enumerate(wallets):
            table.add_row(
                str(i),
                w.get_public_key(),
                str(w.sepolia_balance),
                str(w.token_balance),
            )
    return table


def build_layout(
    wallets: list[Wallet], input_buffer: str = "", status_msg: str = ""
) -> Layout:
    """
    Builds the layout for the application.

    Args:
        wallets (list[Wallet]): The list of existing wallets.
        input_buffer (str, optional): The input buffer for user input.
        status_msg (str, optional): The status message to display.

    Returns:
        Layout: The constructed layout.
    """
    layout = Layout()
    layout.split_column(
        Layout(name="table", ratio=2),
        Layout(name="menu", ratio=2),
    )

    layout["table"].update(
        Panel(
            build_table(wallets),
            title="[bold cyan]Wallets[/bold cyan]",
            border_style="cyan",
        )
    )

    menu_text = Text()

    # ! Classic commands
    menu_text.append("Type:\n\n", style="bold white")
    menu_text.append("  1", style="bold yellow")
    menu_text.append(". Create a wallet\n", style="white")
    menu_text.append("  2", style="bold yellow")
    menu_text.append(". Refresh Wallets balances\n", style="white")
    menu_text.append("  3", style="bold yellow")
    menu_text.append(". Quit Program\n\n", style="white")

    # ! Copy commands
    menu_text.append("Copy Wallet Attributes:\n\n", style="bold white")
    menu_text.append("  Type `adr-0`", style="bold yellow")
    menu_text.append(
        ". Copies the public address of wallet `0`\n\n", style="white"
    )
    menu_text.append("  Type `key-0`", style="bold yellow")
    menu_text.append(
        ". Copies the private key of wallet `0`\n\n", style="white"
    )

    # Return message from commands
    if status_msg:
        menu_text.append("  → ", style="dim")
        menu_text.append_text(Text.from_markup(status_msg)) # !!!!
        menu_text.append("\n\n")

    menu_text.append("  > ", style="bold white")
    menu_text.append(input_buffer, style="bold yellow")
    menu_text.append("█", style="blink white")

    layout["menu"].update(
        Panel(
            menu_text, title="[bold cyan]Menu[/bold cyan]", border_style="cyan"
        )
    )

    return layout


def ensure_wallets_file() -> None:
    """
    Ensures the wallets file (and its parent directory) exists.
    Creates an empty file if it does not.
    """
    if WALLETS_FILE is None:
        return
    # Create parent dir (e.g. wallets/) if missing
    parent = os.path.dirname(WALLETS_FILE)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # Create empty file if missing, without truncating an existing one
    if not os.path.exists(WALLETS_FILE):
        with open(WALLETS_FILE, "w", encoding="utf-8"):
            pass


def load_wallets(
    contract_address: str,
    wallets_file_path: str | None = None,
) -> list[Wallet]:
    """
    Loads wallets from a file.

    Args:
        contract_address (str): The deployed UT42 contract address.
        wallets_file_path (str | None, optional): The path to the file
        containing wallet keys. Defaults to None.

    Returns:
        list[Wallet]: The list of loaded wallets.
    """
    result: list[Wallet] = []

    if wallets_file_path is None:
        return []  # No file path provided, return empty list

    ensure_wallets_file()

    with open(wallets_file_path, "r", encoding="utf-8") as raw_keys:
        # Strip '\n' from readlines()
        unstriped_keys = raw_keys.readlines()
        keys = [k.strip("\n") for k in unstriped_keys]
        if len(keys) == 0:
            return result

        for key in keys:
            try:
                w = Wallet(contract_address, key)
            except Exception as e:
                print(f"Error in init wallets : {e}")
            else:
                result.append(w)
    return result


def main() -> None:
    """
    _Main function_
    """
    load_dotenv()

    contract_address = load_contract_address()

    status = ""
    # Buffer for user prompt
    buf = ""
    try:
        wallets = load_wallets(contract_address, WALLETS_FILE)
    except Exception as e:
        print(f"Error loading from {WALLETS_FILE}.\nError= {e}\nAborting")
        sys.exit(1)

    with Live(
        build_layout(wallets),
        console=console,
        screen=True,
        refresh_per_second=10,
    ) as live:
        while True:
            live.update(build_layout(wallets, buf, status))

            key = readchar.readkey()

            if key in (readchar.key.CTRL_C, readchar.key.CTRL_D):
                break
            if key in (readchar.key.ENTER, "\n", "\r"):
                cmd = buf.strip()
                buf = ""
                if cmd == "1":
                    status = create_wallet(wallets, contract_address)
                elif cmd == "2":
                    status = refresh_balance(wallets)
                elif cmd == "3":
                    break
                elif cmd.startswith("adr-"):
                    status = copy_adress(wallets, cmd)
                elif cmd.startswith("key-"):
                    status = copy_key(wallets, cmd)
                else:
                    status = f"[red]Unknown command:[/red] '{cmd}'"
            elif key in (readchar.key.BACKSPACE, "\x7f"):
                buf = buf[:-1]
            elif key.isprintable():
                buf += key


if __name__ == "__main__":
    main()
