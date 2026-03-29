#!/usr/bin/env python3
"""
╔═══════════════════════════════════════╗
║         R E N Z O   O S               ║
║   The AI Agent Operating System       ║
║   $RNZO · Built on Solana             ║
╚═══════════════════════════════════════╝
"""

import os
import sys
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

load_dotenv()
console = Console()

BANNER = """[bold cyan]
██████╗ ███████╗███╗   ██╗███████╗ ██████╗      ██████╗ ███████╗
██╔══██╗██╔════╝████╗  ██║╚══███╔╝██╔═══██╗    ██╔═══██╗██╔════╝
██████╔╝█████╗  ██╔██╗ ██║  ███╔╝ ██║   ██║    ██║   ██║███████╗
██╔══██╗██╔══╝  ██║╚██╗██║ ███╔╝  ██║   ██║    ██║   ██║╚════██║
██║  ██║███████╗██║ ╚████║███████╗╚██████╔╝    ╚██████╔╝███████║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝ ╚═════╝      ╚═════╝ ╚══════╝
[/bold cyan]
[dim]The AI Agent Operating System · [bold]$RNZO[/bold] · Built on Solana[/dim]"""


def show_banner():
    console.print(BANNER)


def show_menu():
    table = Table(show_header=False, border_style="dim", padding=(0, 2))
    table.add_column("Key", style="bold cyan", width=6)
    table.add_column("Agent", style="bold white")
    table.add_column("Description", style="dim")

    table.add_row("1", "Chat Agent",     "Persistent AI assistant powered by Claude")
    table.add_row("2", "Onchain Agent",  "Monitor Solana wallets & track tokens")
    table.add_row("3", "Social Agent",   "Twitter/X automation — post, reply, monitor")
    table.add_row("4", "Research Agent", "Web scraper + AI summarizer")
    table.add_row("q", "Quit",           "Exit Renzo OS")

    console.print(Panel(table, title="[bold cyan]Select Agent[/bold cyan]", border_style="cyan"))


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Renzo OS — The AI Agent Operating System · $RNZO"""
    if ctx.invoked_subcommand is None:
        # Interactive menu mode
        show_banner()
        while True:
            show_menu()
            choice = Prompt.ask("\n[bold cyan]renzo[/bold cyan]", choices=["1", "2", "3", "4", "q"])
            if choice == "q":
                console.print("\n[dim]Renzo OS shutting down.[/dim]")
                break
            elif choice == "1":
                from agents.chat_agent import run
                run()
            elif choice == "2":
                from agents.onchain_agent import run
                run()
            elif choice == "3":
                from agents.social_agent import run
                run()
            elif choice == "4":
                from agents.research_agent import run
                run()


@cli.command()
def chat():
    """Launch Chat Agent — AI assistant powered by Claude"""
    show_banner()
    from agents.chat_agent import run
    run()


@cli.command()
def onchain():
    """Launch Onchain Agent — Solana wallet tracker & monitor"""
    show_banner()
    from agents.onchain_agent import run
    run()


@cli.command()
def social():
    """Launch Social Agent — Twitter/X automation"""
    show_banner()
    from agents.social_agent import run
    run()


@cli.command()
def research():
    """Launch Research Agent — web scraper + AI summarizer"""
    show_banner()
    from agents.research_agent import run
    run()


if __name__ == "__main__":
    cli()
