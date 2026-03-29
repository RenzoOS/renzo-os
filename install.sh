#!/usr/bin/env bash
# Renzo OS — One-line installer
# Usage: bash install.sh

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}  Renzo OS — The AI Agent Operating System${NC}"
echo -e "${CYAN}  $RNZO · Built on Solana${NC}"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_VERSION" -lt 11 ]; then
  echo -e "${RED}Error: Python 3.11+ is required.${NC}"
  exit 1
fi

echo -e "  ${GREEN}✓${NC} Python $(python3 --version) detected"

# Install dependencies
echo "  Installing dependencies..."
pip install -r requirements.txt --quiet

echo -e "  ${GREEN}✓${NC} Dependencies installed"

# Setup .env
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo -e "  ${GREEN}✓${NC} .env file created from template"
  echo ""
  echo -e "  ${CYAN}Next step:${NC} Open .env and add your API keys"
else
  echo -e "  ${GREEN}✓${NC} .env already exists"
fi

echo ""
echo -e "  ${GREEN}Setup complete.${NC}"
echo ""
echo "  Run Renzo OS:"
echo "    python renzo.py"
echo ""
