"""
Renzo OS · Onchain Agent
Monitor Solana wallets and track tokens in real-time.
"""

import os
import time
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
HELIUS_KEY = os.getenv("HELIUS_API_KEY", "")


def _rpc(method: str, params: list) -> dict:
    resp = httpx.post(RPC_URL, json={
        "jsonrpc": "2.0", "id": 1,
        "method": method, "params": params
    }, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise ValueError(f"RPC error: {data['error']}")
    return data


def get_sol_balance(wallet: str) -> float:
    data = _rpc("getBalance", [wallet])
    lamports = data.get("result", {}).get("value", 0)
    return lamports / 1_000_000_000


def get_token_accounts(wallet: str) -> list:
    data = _rpc("getTokenAccountsByOwner", [
        wallet,
        {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
        {"encoding": "jsonParsed"}
    ])
    accounts = data.get("result", {}).get("value", [])
    tokens = []
    for acc in accounts:
        info = acc["account"]["data"]["parsed"]["info"]
        mint = info["mint"]
        amount = float(info["tokenAmount"]["uiAmount"] or 0)
        if amount > 0:
            tokens.append({"mint": mint, "amount": amount})
    return tokens


def get_recent_transactions(wallet: str, limit: int = 5) -> list:
    data = _rpc("getSignaturesForAddress", [wallet, {"limit": limit}])
    sigs = data.get("result", [])
    return [s["signature"] for s in sigs]


def show_wallet(wallet: str):
    console.print(f"\n[dim]Fetching wallet:[/dim] [cyan]{wallet}[/cyan]")

    with console.status("[dim]Loading...[/dim]", spinner="dots"):
        sol = get_sol_balance(wallet)
        tokens = get_token_accounts(wallet)
        txs = get_recent_transactions(wallet)

    # SOL balance
    console.print(Panel(
        f"[bold yellow]◎ {sol:.4f} SOL[/bold yellow]",
        title="Balance", border_style="yellow"
    ))

    # Token holdings
    if tokens:
        table = Table(title="Token Holdings", border_style="cyan")
        table.add_column("Mint Address", style="dim", max_width=44)
        table.add_column("Amount", justify="right", style="green")
        for t in tokens[:10]:
            table.add_row(t["mint"], f"{t['amount']:,.2f}")
        console.print(table)
    else:
        console.print("[dim]No token holdings found.[/dim]")

    # Recent txs
    if txs:
        console.print("\n[bold]Recent Transactions:[/bold]")
        for sig in txs:
            console.print(f"  [dim]https://solscan.io/tx/{sig}[/dim]")


def monitor_wallet(wallet: str, interval: int = 30):
    console.print(Panel.fit(
        f"[bold cyan]Monitoring:[/bold cyan] {wallet}\n"
        f"[dim]Refresh every {interval}s · Ctrl+C to stop[/dim]",
        border_style="cyan"
    ))
    last_txs = set()
    while True:
        try:
            current_txs = set(get_recent_transactions(wallet, limit=10))
            new_txs = current_txs - last_txs
            if new_txs and last_txs:
                for sig in new_txs:
                    console.print(f"\n[bold green]⚡ New transaction detected![/bold green]")
                    console.print(f"   [cyan]https://solscan.io/tx/{sig}[/cyan]")
            last_txs = current_txs
            time.sleep(interval)
        except KeyboardInterrupt:
            console.print("\n[dim]Stopped monitoring.[/dim]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            time.sleep(interval)


def run():
    console.print(Panel.fit(
        "[bold cyan]Renzo OS[/bold cyan] · [yellow]Onchain Agent[/yellow]\n"
        "[dim]Solana wallet tracker & monitor[/dim]",
        border_style="cyan"
    ))

    default_wallet = os.getenv("DEFAULT_WALLET", "")

    while True:
        console.print("\n[bold]Options:[/bold]")
        console.print("  [cyan]1[/cyan] Check wallet balance & tokens")
        console.print("  [cyan]2[/cyan] Monitor wallet for new transactions")
        console.print("  [cyan]q[/cyan] Quit")

        choice = Prompt.ask("\nChoose", choices=["1", "2", "q"])

        if choice == "q":
            break

        wallet = Prompt.ask("Wallet address", default=default_wallet).strip()
        if not wallet:
            console.print("[red]No wallet address provided.[/red]")
            continue

        if choice == "1":
            show_wallet(wallet)
        elif choice == "2":
            interval = int(Prompt.ask("Refresh interval (seconds)", default="30"))
            monitor_wallet(wallet, interval)
