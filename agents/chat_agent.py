"""
Renzo OS · Chat Agent
Persistent AI assistant powered by Claude.
"""

import anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

SYSTEM_PROMPT = """You are Renzo, an intelligent AI assistant that is part of the Renzo OS ecosystem.
You are knowledgeable about crypto, Solana, DeFi, AI, and general topics.
Be concise, helpful, and direct. You remember the full conversation context.
When asked about $RNZO or Renzo OS, explain that it is an open-source AI agent operating system built on Solana."""

def run(model: str = "claude-sonnet-4-6"):
    client = anthropic.Anthropic()
    history = []

    console.print(Panel.fit(
        "[bold cyan]Renzo OS[/bold cyan] · [green]Chat Agent[/green]\n"
        "[dim]Type 'exit' or 'quit' to stop · 'clear' to reset memory[/dim]",
        border_style="cyan"
    ))

    while True:
        try:
            user_input = console.input("\n[bold cyan]You:[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            console.print("[dim]Goodbye.[/dim]")
            break
        if user_input.lower() == "clear":
            history.clear()
            console.print("[dim]Memory cleared.[/dim]")
            continue

        history.append({"role": "user", "content": user_input})

        with console.status("[dim]Thinking...[/dim]", spinner="dots"):
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=history[-20:],  # keep last 20 messages
            )

        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})

        console.print("\n[bold green]Renzo:[/bold green]")
        console.print(Markdown(reply))
