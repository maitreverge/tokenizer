from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.live import Live
from rich.layout import Layout
import readchar
import json

from dotenv import load_dotenv
import os
import sys

from eth_account import Account

load_dotenv()

WALLETS_JSON = os.getenv("WALLETS_JSON")

console = Console()

class Wallet():
    def __init__(self, key: str) -> None:

        self.account = Account.from_key(key)
        # self._private_key = 
    
    def get_private_key(self) -> int:
        return self.account.key()
    
    def get_public_key(self) -> int:
        return self.account.address()
    

# --- Mock data ---
WALLETS = [
    {
        "name": "Cranberry",
        "number": 0,
        "address": "0x2hd73dF9aB3c...",
        "balance": "0.012 ETH",
    },
    {
        "name": "Banana",
        "number": 1,
        "address": "0x9chdu3aA1D2e...",
        "balance": "0.047 ETH",
    },
    {
        "name": "Kiwi",
        "number": 2,
        "address": "0xcKdH63bB9f0a...",
        "balance": "0.003 ETH",
    },
]


def action_refresh():
    return "[green]✓ Wallets refreshed.[/green]"


def action_private_key():
    return "[yellow]⚠  Private key (mock): 0xDEADBEEF...CAFEBABE[/yellow]"


def build_table() -> Table:
    table = Table(
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold cyan",
        expand=True,
    )
    table.add_column("Wallet Name", style="bold white", min_width=14)
    table.add_column("Number", style="dim", min_width=8, justify="center")
    table.add_column("Public Address", style="cyan", min_width=20)
    table.add_column(
        "Solde (SepoliaETH)", style="green", min_width=18, justify="right"
    )

    for w in WALLETS:
        table.add_row(w["name"], str(w["number"]), w["address"], w["balance"])
    return table


def build_layout(input_buffer: str = "", status_msg: str = "") -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="table", ratio=3),
        Layout(name="menu", ratio=2),
    )

    layout["table"].update(
        Panel(
            build_table(),
            title="[bold cyan]Wallets[/bold cyan]",
            border_style="cyan",
        )
    )

    menu_text = Text()
    menu_text.append("Type:\n\n", style="bold white")
    menu_text.append("  1", style="bold yellow")
    menu_text.append(". Refresh\n", style="white")
    menu_text.append("  2", style="bold yellow")
    menu_text.append(
        ". Access private key of selected wallet\n", style="white"
    )
    menu_text.append("  3", style="bold yellow")
    menu_text.append(". Quit Program\n\n", style="white")

    if status_msg:
        menu_text.append("  → ", style="dim")
        menu_text.append_text(Text.from_markup(status_msg))
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

def load_wallets(wallets_json) -> list[Wallet]:
# def load_wallets(wallets_json) -> None:
    result = list()
    with open(wallets_json, "r") as wallets:
        # Strip '\n' from realines()
        wallets = [w.strip('\n') for w in wallets.readlines()]
        # print(f"{wallets}")
        for key in wallets:
            try:
                w = Wallet(key)
                print(f"Current private key wallet = {w.get_private_key()}")
                print(f"Current public adress wallet = {w.get_public_key()}")
            except Exception as e:
                print(f"Error in init wallets : {e}")
            else:
                result.append(w)
    return result

def main() -> None:
    """
    _Main function_
    """
    status = ""
    buf = ""
    try:
        wallets = load_wallets(WALLETS_JSON)
    except Exception as e:
        print(f"Error while loading wallets from {WALLETS_JSON}.\nError= {e}\nAborting")
        sys.exit(1)
    
    # with Live(
    #     build_layout(), console=console, screen=True, refresh_per_second=10
    # ) as live:
    #     while True:
    #         live.update(build_layout(buf, status))

    #         key = readchar.readkey()

    #         if key in (readchar.key.CTRL_C, readchar.key.CTRL_D):
    #             break
    #         elif key in (readchar.key.ENTER, "\n", "\r"):
    #             cmd = buf.strip()
    #             buf = ""
    #             if cmd == "1":
    #                 status = action_refresh()
    #             elif cmd == "2":
    #                 status = action_private_key()
    #             elif cmd == "3":
    #                 break
    #             else:
    #                 status = f"[red]Unknown command:[/red] '{cmd}'"
    #         elif key in (readchar.key.BACKSPACE, "\x7f"):
    #             buf = buf[:-1]
    #         elif key.isprintable():
    #             buf += key

if __name__ == "__main__":
    main()