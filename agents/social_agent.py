"""
Renzo OS · Social Agent
Twitter/X automation — schedule, post, and monitor.
"""

import os
import tweepy
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()


def _get_client() -> tweepy.Client:
    return tweepy.Client(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
        wait_on_rate_limit=True,
    )


def post_tweet(client: tweepy.Client, text: str):
    resp = client.create_tweet(text=text)
    tweet_id = resp.data["id"]
    console.print(f"[bold green]✓ Tweet posted![/bold green] ID: {tweet_id}")
    console.print(f"  [dim]https://twitter.com/i/web/status/{tweet_id}[/dim]")


def get_mentions(client: tweepy.Client, limit: int = 10):
    me = client.get_me()
    user_id = me.data.id
    mentions = client.get_users_mentions(id=user_id, max_results=min(limit, 100))

    if not mentions.data:
        console.print("[dim]No mentions found.[/dim]")
        return

    table = Table(title="Recent Mentions", border_style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Text", max_width=60)
    for m in mentions.data:
        table.add_row(str(m.id), m.text)
    console.print(table)


def reply_to_tweet(client: tweepy.Client, tweet_id: str, text: str):
    resp = client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
    console.print(f"[bold green]✓ Reply posted![/bold green] ID: {resp.data['id']}")


def search_tweets(client: tweepy.Client, query: str, limit: int = 10):
    results = client.search_recent_tweets(query=query, max_results=min(limit, 100))

    if not results.data:
        console.print(f"[dim]No tweets found for:[/dim] {query}")
        return

    table = Table(title=f'Search: "{query}"', border_style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Text", max_width=70)
    for t in results.data:
        table.add_row(str(t.id), t.text)
    console.print(table)


def run():
    console.print(Panel.fit(
        "[bold cyan]Renzo OS[/bold cyan] · [magenta]Social Agent[/magenta]\n"
        "[dim]Twitter/X automation interface[/dim]",
        border_style="cyan"
    ))

    try:
        client = _get_client()
        me = client.get_me()
        console.print(f"[green]✓ Connected as:[/green] @{me.data.username}")
    except Exception as e:
        console.print(f"[red]✗ Twitter auth failed: {e}[/red]")
        console.print("[dim]Check your Twitter API keys in .env[/dim]")
        return

    while True:
        console.print("\n[bold]Options:[/bold]")
        console.print("  [cyan]1[/cyan] Post a tweet")
        console.print("  [cyan]2[/cyan] View recent mentions")
        console.print("  [cyan]3[/cyan] Reply to a tweet")
        console.print("  [cyan]4[/cyan] Search tweets")
        console.print("  [cyan]q[/cyan] Quit")

        choice = Prompt.ask("\nChoose", choices=["1", "2", "3", "4", "q"])

        if choice == "q":
            break
        elif choice == "1":
            text = Prompt.ask("Tweet text")
            if len(text) > 280:
                console.print(f"[red]Too long ({len(text)}/280 chars)[/red]")
            else:
                confirm = Prompt.ask(f"Post this tweet? ({len(text)}/280)", choices=["y", "n"])
                if confirm == "y":
                    post_tweet(client, text)
        elif choice == "2":
            get_mentions(client)
        elif choice == "3":
            tweet_id = Prompt.ask("Tweet ID to reply to")
            text = Prompt.ask("Reply text")
            reply_to_tweet(client, tweet_id, text)
        elif choice == "4":
            query = Prompt.ask("Search query (e.g. $RNZO)")
            search_tweets(client, query)
