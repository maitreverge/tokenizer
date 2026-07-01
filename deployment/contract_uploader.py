"""
Smart Contract Uploader - TUI version
"""

import os
import sys
import readchar

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.live import Live
from rich.layout import Layout

from web3 import Web3
from solcx import install_solc, compile_source
import solcx
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import SignAndSendRawMiddlewareBuilder
from pyperclip import copy as clipboard_cpy

from dotenv import load_dotenv

from utils import is_virtual_env_sys

load_dotenv()

SEPOLIA_ENTRYPOINT = os.getenv("SEPOLIA_ENTRYPOINT")
SMART_CONTRACT_PATH = os.getenv(
    "SMART_CONTRACT_PATH", "../code/contract/contract.sol"
)
MY_PRIVATE_KEY = os.getenv("MY_PRIVATE_KEY")
MY_PUBLIC_KEY = os.getenv("MY_PUBLIC_KEY")
SOLC_VERSION = "0.8.35"

console = Console()


class ContractState:
    """
    Holds the state of the contract upload process.
    """

    def __init__(self) -> None:
        self.w3: Web3 | None = None
        self.connected: bool = False
        self.compiler_installed: bool = False
        self.contract_path: str = SMART_CONTRACT_PATH or ""
        self.contract_source: str = ""
        # Application Binary interface => Used for front-end libraries
        self.abi = None
        # Binary for EVM (Etherum Virtual Machine) => send to the blockchain
        self.bytecode: str = ""
        # Contract transaction hash
        self.tx_hash: str = ""
        # Contract address
        self.contract_address: str = ""
        # Contract address
        self.gas_used: int = 0
        self.block_number: int = 0
        # Account 
        self.account_address: str = ""
        self.hello_world_result: str = ""

    def connect(self) -> str:
        """
        Connect to the Sepolia node. Also creates an account bases on MY_PRIVATE_KEY
        """
        try:
            self.w3 = Web3(Web3.HTTPProvider(SEPOLIA_ENTRYPOINT))
            if not self.w3.is_connected():
                self.connected = False
                return "[bold red]❌ Web3 node failed to connect[/bold red]"
            self.connected = True
            
            # Creates account
            if MY_PRIVATE_KEY:
                account: LocalAccount = Account.from_key(MY_PRIVATE_KEY)
                self.account_address = account.address
            return "[bold green]✓ Connected to Sepolia node[/bold green]"
        except Exception as e:
            self.connected = False
            return f"[bold red]❌ Connection error: {e}[/bold red]"

    def install_compiler(self) -> str:
        """
        Install the solc compiler if missing.
        """
        try:
            # Check if any compiler is already installed
            installed = solcx.get_installed_solc_versions()
            if any(str(v) == SOLC_VERSION for v in installed):
                self.compiler_installed = True
                return f"[bold green]✓ solc {SOLC_VERSION} already installed[/bold green]"
            
            # Install solc compiler
            install_solc(version=SOLC_VERSION)
            self.compiler_installed = True
            return f"[bold green]✓ Installed solc {SOLC_VERSION}[/bold green]"
        except Exception as e:
            return f"[bold red]❌ Compiler install error: {e}[/bold red]"

    def compile_contract(self) -> str:
        """
        Compile the smart contract source.
        """
        try:
            # Tries to read the contract in the path defined in the env
            if not os.path.isfile(self.contract_path):
                return f"[bold red]❌ Contract not found: {self.contract_path}[/bold red]"

            with open(self.contract_path, "r", encoding="utf-8") as f:
                self.contract_source = f.read()

            # Read the openzeppelin library
            openzeppelin_path = os.path.abspath("./node_modules")

            # Compile contract
            compiled = compile_source(
                self.contract_source,
                output_values=["abi", "bin"],
                solc_version=SOLC_VERSION,
                import_remappings=[
                    f"@openzeppelin/={openzeppelin_path}/@openzeppelin/"
                ],
                allow_paths=[openzeppelin_path],
            )

            _, contract_interface = compiled.popitem()
            
            # Saved both ABI and BIN into the class
            self.bytecode = contract_interface["bin"]
            self.abi = contract_interface["abi"]
            return "[bold green]✓ Contract compiled successfully[/bold green]"
        except Exception as e:
            return f"[bold red]❌ Compilation error: {e}[/bold red]"

    def deploy_contract(self) -> str:
        """
        Deploy the compiled contract to Sepolia.
        """
        try:
            # Pre-deployment checks
            if not self.connected or self.w3 is None:
                return "[bold red]❌ Not connected to Sepolia. Run step 1 first.[/bold red]"
            if not self.bytecode or self.abi is None:
                return "[bold red]❌ Contract not compiled. Run step 3 first.[/bold red]"
            if not MY_PRIVATE_KEY:
                return "[bold red]❌ MY_PRIVATE_KEY not configured[/bold red]"
            
            # Instanciate a local account based on the key.
            account: LocalAccount = Account.from_key(MY_PRIVATE_KEY)
            
            # AUTOMATED SIGNING (The "Onion" Middleware):
            # Remote nodes don't have our private key and cannot sign transactions.
            # This "onion" layer automatically signs our transactions locally right before sending.
            self.w3.middleware_onion.inject(
                SignAndSendRawMiddlewareBuilder.build(account), layer=0
            )

            # For future transactions, make our address default.
            self.w3.eth.default_account = account.address

            # Load the contract with both the ABI and the Binary code.
            Contract = self.w3.eth.contract(
                abi=self.abi, bytecode=self.bytecode
            )

            # Initiate the deployment transaction. 
            # Thanks to the middleware injected above, '.transact()' automatically 
            # handles the building, local signing, and broadcasting of this transaction!
            tx_hash = Contract.constructor().transact()
            
            # Pause and wait for the Sepolia network to mine the transaction and return a receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            # Store infos about the transaction
            self.tx_hash = tx_hash.hex()
            self.contract_address = tx_receipt.contractAddress or ""
            self.gas_used = tx_receipt.gasUsed or 0
            self.block_number = tx_receipt.blockNumber or 0

            return "[bold green]✓ Contract deployed successfully![/bold green]"
        except Exception as e:
            return f"[bold red]❌ Deployment error: {e}[/bold red]"
    
    def call_hello_world(self) -> str:
        """
        Calls the `helloWorld` method from the deployed smart contract.
        """
        try:
            # Pre-checks
            if not self.connected or self.w3 is None:
                return "[bold red]❌ Not connected to Sepolia. Run step 1 first.[/bold red]"
            if not self.contract_address:
                return "[bold red]❌ Contract not deployed. Run step 4 first.[/bold red]"
            if self.abi is None:
                return "[bold red]❌ ABI not available. Recompile the contract.[/bold red]"

            # Load the contract object from the contract adress
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=self.abi,
            )

            # Simply call the helloWorld function
            result: str = contract.functions.helloWorld().call()
            self.hello_world_result = result
            return f"[bold green]✓ helloWorld() → [/bold green][cyan]{result}[/cyan]"
        except Exception as e:
            return f"[bold red]❌ Call error: {e}[/bold red]"


def build_status_table(state: ContractState) -> Table:
    """
    Build a status table showing the current pipeline state.
    """
    table = Table(box=box.SIMPLE_HEAVY, expand=True, show_header=True)
    table.add_column("Step", style="bold yellow", width=6)
    table.add_column("Description", style="white")
    table.add_column("Status", justify="center")

    def status_cell(ok: bool) -> str:
        return (
            "[bold green]✓ OK[/bold green]"
            if ok
            else "[bold red]✗ Pending[/bold red]"
        )

    table.add_row("1", "Connect to Sepolia node", status_cell(state.connected))
    table.add_row(
        "2",
        f"Install solc {SOLC_VERSION}",
        status_cell(state.compiler_installed),
    )
    table.add_row("3", f"Compile contract", status_cell(bool(state.bytecode)))
    table.add_row(
        "4", "Deploy contract", status_cell(bool(state.contract_address))
    )

    table.add_section()
    table.add_row("📂", "Contract Path", f"[cyan]{state.contract_path}[/cyan]")
    table.add_row(
        "👤", "Deployer", f"[cyan]{state.account_address or 'N/A'}[/cyan]"
    )

    if state.contract_address:
        table.add_section()
        table.add_row(
            "📜",
            "Contract Address",
            f"[bold green]{state.contract_address}[/bold green]",
        )
        table.add_row("🔗", "Tx Hash", f"[green]{state.tx_hash}[/green]")
        table.add_row("⛽", "Gas Used", f"[white]{state.gas_used}[/white]")
        table.add_row("📦", "Block #", f"[white]{state.block_number}[/white]")

    return table


def build_layout(
    state: ContractState,
    input_buffer: str = "",
    status_msg: str = "",
) -> Layout:
    """
    Build the rich layout.
    """
    layout = Layout()
    layout.split_row(
        Layout(name="table", ratio=3),
        Layout(name="menu", ratio=2),
    )

    layout["table"].update(
        Panel(
            build_status_table(state),
            title="[bold cyan]Smart Contract Deployment[/bold cyan]",
            border_style="cyan",
        )
    )

    menu_text = Text()
    menu_text.append("Pipeline Steps:\n\n", style="bold white")
    menu_text.append("  1", style="bold yellow")
    menu_text.append(". Connect to Sepolia node\n", style="white")
    menu_text.append("  2", style="bold yellow")
    menu_text.append(". Install solc compiler\n", style="white")
    menu_text.append("  3", style="bold yellow")
    menu_text.append(". Compile contract\n", style="white")
    menu_text.append("  4", style="bold yellow")
    menu_text.append(". Deploy contract\n", style="white")
    menu_text.append("  5", style="bold yellow")
    menu_text.append(". Run all steps (1→4)\n", style="white")
    menu_text.append("  6", style="bold yellow")
    menu_text.append(". Call `helloWorld()` Smart Contract Method\n", style="white")
    menu_text.append("  q", style="bold yellow")
    menu_text.append(". Quit Program\n\n", style="white")

    menu_text.append("Copy Deployment Info:\n\n", style="bold white")
    menu_text.append("  Type `adr`", style="bold yellow")
    menu_text.append(". Copy contract address\n", style="white")
    menu_text.append("  Type `tx`", style="bold yellow")
    menu_text.append(". Copy transaction hash\n\n", style="white")

    if status_msg:
        menu_text.append("  → ", style="dim")
        menu_text.append_text(Text.from_markup(status_msg))
        menu_text.append("\n\n")

    menu_text.append("  > ", style="bold white")
    menu_text.append(input_buffer, style="bold yellow")
    menu_text.append("█", style="blink white")

    layout["menu"].update(
        Panel(
            menu_text,
            title="[bold cyan]Menu[/bold cyan]",
            border_style="cyan",
        )
    )

    return layout

def copy_address(state: ContractState) -> str:
    """
    Copies contract adress to the clipboard.
    """
    if not state.contract_address:
        return "[bold red]❌ No contract address available[/bold red]"
    try:
        clipboard_cpy(state.contract_address)
        return "[bold green]✓ Contract address copied[/bold green]"
    except Exception:
        # Fallback for Docker/Headless environments
        return f"[bold yellow]Manual Copy:[/bold yellow] {state.contract_address}"


def copy_tx(state: ContractState) -> str:
    """
    Copies transaction hash to the clipboard.
    """
    if not state.tx_hash:
        return "[bold red]❌ No transaction hash available[/bold red]"
    try:
        clipboard_cpy(state.tx_hash)
        return "[bold green]✓ Transaction hash copied[/bold green]"
    except Exception:
        # Fallback for Docker/Headless environments
        return f"[bold yellow]Manual Copy:[/bold yellow] {state.tx_hash}"


def run_all(state: ContractState) -> str:
    """
    Run all steps from 1 to 4
    """
    msg = state.connect()
    if not state.connected:
        return msg
    msg = state.install_compiler()
    if not state.compiler_installed:
        return msg
    msg = state.compile_contract()
    if not state.bytecode:
        return msg
    return state.deploy_contract()


def pass_init_checks() -> bool:
    """
    Checks if the scripts runs in a venv.
    """
    if not is_virtual_env_sys():
        console.print(
            "[bold red]You are not running inside a virtual environment[/bold red]"
        )
        return False
    return True


def main() -> None:
    """Main function"""
    if not pass_init_checks():
        sys.exit(1)

    state = ContractState()
    status = ""
    buf = ""

    with Live(
        build_layout(state),
        console=console,
        screen=True,
        refresh_per_second=10,
    ) as live:
        while True:
            live.update(build_layout(state, buf, status))

            key = readchar.readkey()

            if key in (readchar.key.CTRL_C, readchar.key.CTRL_D):
                break
            if key in (readchar.key.ENTER, "\n", "\r"):
                cmd = buf.strip().lower()
                buf = ""
                if cmd == "1":
                    status = "[yellow]⏳ Connecting...[/yellow]"
                    live.update(build_layout(state, buf, status))
                    status = state.connect()
                elif cmd == "2":
                    status = "[yellow]⏳ Installing compiler...[/yellow]"
                    live.update(build_layout(state, buf, status))
                    status = state.install_compiler()
                elif cmd == "3":
                    status = "[yellow]⏳ Compiling...[/yellow]"
                    live.update(build_layout(state, buf, status))
                    status = state.compile_contract()
                elif cmd == "4":
                    status = "[yellow]⏳ Deploying contract (this can take a while)...[/yellow]"
                    live.update(build_layout(state, buf, status))
                    status = state.deploy_contract()
                elif cmd == "5":
                    status = "[yellow]⏳ Running full pipeline...[/yellow]"
                    live.update(build_layout(state, buf, status))
                    status = run_all(state)
                elif cmd == "6":
                    status = "[yellow]⏳ Calling helloWord()...[/yellow]"
                    live.update(build_layout(state, buf, status))
                    status = state.call_hello_world()
                elif cmd == "q" or cmd == "quit" or cmd == "exit":
                    break
                elif cmd == "adr":
                    status = copy_address(state)
                elif cmd == "tx":
                    status = copy_tx(state)
                else:
                    status = f"[red]Unknown command:[/red] '{cmd}'"
            elif key in (readchar.key.BACKSPACE, "\x7f"):
                buf = buf[:-1]
            elif key.isprintable():
                buf += key


if __name__ == "__main__":
    main()
