from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.live import Live
from rich.layout import Layout
import time

console = Console()

# --- Mock data ---
WALLETS = [
    {"name": "Cranberry", "number": 0, "address": "0x2hd73dF9aB3c...", "balance": "0.012 ETH"},
    {"name": "Banana",    "number": 1, "address": "0x9chdu3aA1D2e...", "balance": "0.047 ETH"},
    {"name": "Kiwi",      "number": 2, "address": "0xcKdH63bB9f0a...", "balance": "0.003 ETH"},
]

# --- Mock actions ---
def action_refresh():
    return "[green]✓ Wallets refreshed.[/green]"

def action_private_key():
    return "[yellow]⚠  Enter wallet number to reveal its private key (mock).[/yellow]"

# --- Build the table ---
def build_table() -> Table:
    table = Table(
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold cyan",
        expand=True,
    )
    table.add_column("Wallet Name", style="bold white", min_width=14)
    table.add_column("Number",      style="dim",        min_width=8,  justify="center")
    table.add_column("Public Address", style="cyan",    min_width=18)
    table.add_column("Solde (SepoliaETH)", style="green", min_width=18, justify="right")

    for w in WALLETS:
        table.add_row(
            w["name"],
            str(w["number"]),
            w["address"],
            w["balance"],
        )
    return table

# --- Build the full layout ---
def build_layout(status_msg: str = "") -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="table",  ratio=3),
        Layout(name="menu",   ratio=2),
    )

    layout["table"].update(
        Panel(build_table(), title="[bold cyan]Wallets[/bold cyan]", border_style="cyan")
    )

    menu_text = Text()
    menu_text.append("Type:\n\n", style="bold white")
    menu_text.append("  1", style="bold yellow")
    menu_text.append(". To refresh\n", style="white")
    menu_text.append("  2", style="bold yellow")
    menu_text.append(". Access private key of selected wallet\n", style="white")
    if status_msg:
        menu_text.append(f"\n  → ", style="dim")
        menu_text.append_text(Text.from_markup(status_msg))

    layout["menu"].update(
        Panel(menu_text, title="[bold cyan]Menu[/bold cyan]", border_style="cyan")
    )

    return layout

# --- Main loop ---
def main():
    status = ""

    with Live(build_layout(status), console=console, screen=True, refresh_per_second=4) as live:
        while True:
            live.update(build_layout(status))

            # Move cursor to input zone (bottom of terminal)
            console.file.write("\033[999;0H")  # go to last line
            console.file.flush()

            try:
                raw = input("  > ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if raw == "1":
                status = action_refresh()
            elif raw == "2":
                status = action_private_key()
            elif raw.lower() in ("q", "quit", "exit"):
                break
            else:
                status = f"[red]Unknown command:[/red] '{raw}'"

if __name__ == "__main__":
    main()