# Contributing to Renzo OS

Thanks for your interest in contributing to Renzo OS. All contributions are welcome.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/renzo-os`
3. Create a branch: `git checkout -b feat/your-feature`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy env: `cp .env.example .env`

## Development

Run any agent directly:

```bash
python renzo.py chat
python renzo.py onchain
python renzo.py social
python renzo.py research
```

## Adding a New Agent

1. Create `agents/your_agent.py` with a `run()` function
2. Register it in `renzo.py` as a new CLI command
3. Document it in `README.md`

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Write clear commit messages
- Test your changes before submitting
- Update `README.md` if you add or change functionality

## Reporting Issues

Open an issue on GitHub with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your OS and Python version

## Code Style

- Follow PEP 8
- Use `rich` for all terminal output (consistent UI)
- Keep agent files self-contained

---

By contributing, you agree your code will be licensed under the MIT License.
