"""
Renzo OS · Research Agent
Web scraping + AI summarization. Point it at any topic.
"""

import anthropic
import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

SEARCH_URL = "https://html.duckduckgo.com/html/"

SYSTEM_PROMPT = """You are a research assistant for Renzo OS.
You receive raw web content and a user query. Your job is to:
1. Extract only the relevant information
2. Summarize clearly and concisely
3. Highlight key facts, numbers, or insights
4. Format your response in clean markdown

Be direct. No fluff."""


def _scrape(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RenzoOS/1.0)"}
    try:
        resp = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script/style tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        # Limit to 8000 chars to stay within context
        return text[:8000]
    except Exception as e:
        return f"Error fetching {url}: {e}"


def _search_ddg(query: str, max_results: int = 5) -> list[dict]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RenzoOS/1.0; +https://github.com/RenzoOS/renzo-os)"}
    data = {"q": query, "b": ""}
    try:
        resp = httpx.post(SEARCH_URL, data=data, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for link in soup.select(".result__title a")[:max_results]:
            href = link.get("href", "")
            title = link.get_text(strip=True)
            if href.startswith("http"):
                results.append({"title": title, "url": href})
        return results
    except Exception as e:
        console.print(f"[red]Search error: {e}[/red]")
        return []


def research_topic(query: str, deep: bool = False):
    client = anthropic.Anthropic()

    console.print(f"\n[dim]Searching:[/dim] [cyan]{query}[/cyan]")

    with console.status("[dim]Fetching sources...[/dim]", spinner="dots"):
        results = _search_ddg(query, max_results=5 if deep else 3)

    if not results:
        console.print("[red]No results found.[/red]")
        return

    console.print(f"[dim]Found {len(results)} sources. Scraping...[/dim]")

    scraped_content = []
    for r in results:
        with console.status(f"[dim]Scraping: {r['title'][:50]}...[/dim]", spinner="dots"):
            content = _scrape(r["url"])
        scraped_content.append(f"SOURCE: {r['title']}\nURL: {r['url']}\n\n{content}")

    combined = "\n\n---\n\n".join(scraped_content)

    console.print(f"\n[dim]Analyzing with AI...[/dim]")

    with console.status("[dim]Generating summary...[/dim]", spinner="dots"):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # fast + cheap for research
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Research query: {query}\n\nWeb content:\n{combined}"
            }]
        )

    summary = response.content[0].text

    console.print(Panel(
        Markdown(summary),
        title=f"[bold]Research: {query}[/bold]",
        border_style="green"
    ))

    console.print("\n[dim]Sources:[/dim]")
    for r in results:
        console.print(f"  [dim]• {r['title']} → {r['url']}[/dim]")


def research_url(url: str, query: str):
    client = anthropic.Anthropic()

    console.print(f"\n[dim]Fetching:[/dim] [cyan]{url}[/cyan]")
    with console.status("[dim]Scraping page...[/dim]", spinner="dots"):
        content = _scrape(url)

    with console.status("[dim]Analyzing...[/dim]", spinner="dots"):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Query: {query}\n\nPage content from {url}:\n{content}"
            }]
        )

    console.print(Panel(
        Markdown(response.content[0].text),
        title=f"[bold]Analysis: {url}[/bold]",
        border_style="green"
    ))


def run():
    console.print(Panel.fit(
        "[bold cyan]Renzo OS[/bold cyan] · [green]Research Agent[/green]\n"
        "[dim]Web scraper + AI summarizer[/dim]",
        border_style="cyan"
    ))

    while True:
        console.print("\n[bold]Options:[/bold]")
        console.print("  [cyan]1[/cyan] Research a topic (auto search + summarize)")
        console.print("  [cyan]2[/cyan] Analyze a specific URL")
        console.print("  [cyan]q[/cyan] Quit")

        choice = Prompt.ask("\nChoose", choices=["1", "2", "q"])

        if choice == "q":
            break
        elif choice == "1":
            query = Prompt.ask("Research topic")
            deep = Prompt.ask("Deep search? (more sources)", choices=["y", "n"], default="n") == "y"
            research_topic(query, deep=deep)
        elif choice == "2":
            url = Prompt.ask("URL to analyze")
            query = Prompt.ask("What do you want to know about this page?")
            research_url(url, query)
