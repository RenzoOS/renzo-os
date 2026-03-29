# Renzo OS · Makefile

.PHONY: install run chat onchain social research clean help

help:
	@echo ""
	@echo "  Renzo OS — The AI Agent Operating System"
	@echo ""
	@echo "  Usage:"
	@echo "    make install    Install dependencies"
	@echo "    make run        Launch Renzo OS interactive menu"
	@echo "    make chat       Launch Chat Agent"
	@echo "    make onchain    Launch Onchain Agent"
	@echo "    make social     Launch Social Agent"
	@echo "    make research   Launch Research Agent"
	@echo "    make clean      Remove cache files"
	@echo ""

install:
	@echo "Installing Renzo OS dependencies..."
	pip install -r requirements.txt
	@echo "Done. Copy .env.example to .env and add your API keys."

run:
	python renzo.py

chat:
	python renzo.py chat

onchain:
	python renzo.py onchain

social:
	python renzo.py social

research:
	python renzo.py research

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cache cleared."
