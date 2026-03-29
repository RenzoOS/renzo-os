# Renzo OS 🖥️

> **The AI Agent Operating System**
> 4 autonomous agents. 1 unified OS. Built on Solana.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Solana](https://img.shields.io/badge/chain-Solana-purple.svg)](https://solana.com)
[![Token](https://img.shields.io/badge/token-%24RNZO-orange.svg)](https://pump.fun)
[![Contributing](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Security](https://img.shields.io/badge/security-policy-red.svg)](SECURITY.md)

---

## What is Renzo OS?

Renzo OS is an open-source AI agent framework with 4 modular, autonomous agents that you can run locally from a single CLI. No cloud lock-in. No walled garden. Just agents that work.

> *"If LLMs are the brain — Renzo OS is the body."*

---

## Agents

| Agent | Description |
|-------|-------------|
| 🧠 **Chat Agent** | Persistent AI assistant powered by Claude. Remembers full context. |
| 🔗 **Onchain Agent** | Monitor Solana wallets, track token holdings, get real-time tx alerts. |
| 📡 **Social Agent** | Twitter/X automation — post, reply, search, monitor mentions. |
| 🔍 **Research Agent** | Point it at any topic. It scrapes the web, summarizes with AI, delivers clean intel. |

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/renzo-os/renzo-os
cd renzo-os
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys:

```env
ANTHROPIC_API_KEY=your_key_here     # Chat + Research agents
TWITTER_API_KEY=...                  # Social agent
TWITTER_BEARER_TOKEN=...
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com   # Onchain agent
HELIUS_API_KEY=your_key_here        # (optional, for enhanced Solana data)
```

### 4. Run Renzo OS

```bash
# Interactive menu (recommended)
python renzo.py

# Or launch a specific agent directly
python renzo.py chat        # Chat Agent
python renzo.py onchain     # Onchain Agent
python renzo.py social      # Social Agent
python renzo.py research    # Research Agent
```

---

## Usage Examples

### Chat Agent
```
You: what's happening with Solana today?
Renzo: [concise AI response with context memory]
```

### Onchain Agent
```
1 → Check wallet balance & tokens
2 → Monitor wallet for new transactions
```

### Social Agent
```
1 → Post a tweet
2 → View recent mentions
3 → Reply to a tweet
4 → Search tweets (e.g. $RNZO)
```

### Research Agent
```
1 → Research a topic     (e.g. "Solana AI agent tokens 2025")
2 → Analyze a URL        (paste any link, ask a question)
```

---

## Project Structure

```
renzo-os/
├── renzo.py                  ← CLI entry point
├── agents/
│   ├── chat_agent.py         ← Claude-powered chat
│   ├── onchain_agent.py      ← Solana wallet tracker
│   ├── social_agent.py       ← Twitter/X automation
│   └── research_agent.py     ← Web scraper + summarizer
├── .env.example              ← Environment template
└── requirements.txt
```

---

## API Keys You Need

| Key | Where to get | Required for |
|-----|-------------|--------------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Chat + Research |
| `TWITTER_*` | [developer.twitter.com](https://developer.twitter.com) | Social Agent |
| `HELIUS_API_KEY` | [helius.dev](https://helius.dev) | Enhanced Solana data |
| `SOLANA_RPC_URL` | Public or [Helius](https://helius.dev)/[QuickNode](https://quicknode.com) | Onchain Agent |

---

## Roadmap

- [x] Chat Agent — Claude-powered persistent assistant
- [x] Onchain Agent — Solana wallet monitor
- [x] Social Agent — Twitter/X automation
- [x] Research Agent — Web scraper + AI summarizer
- [ ] Agent memory persistence (SQLite)
- [ ] Multi-agent orchestration (agents talking to each other)
- [ ] Telegram interface
- [ ] Discord integration
- [ ] On-chain data feed from $RNZO token activity

---

## Token

**$RNZO** is the native token of the Renzo OS ecosystem, launched on [pump.fun](https://pump.fun).

---

## License

MIT — do whatever you want with it.

---

<div align="center">
  <strong>Renzo OS</strong> · The AI Agent Operating System<br>
  <code>$RNZO</code> · Built on Solana
</div>
