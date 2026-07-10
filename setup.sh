#!/usr/bin/env bash
#
# ADK Orchestra Workshop — setup script
#
# Installs:
#   • Python virtual env + ADK dependencies
#   • Gemini CLI (via npm) — optional, prompted
#
# Re-run any time. Safe to run multiple times.
#
set -e

cd "$(dirname "$0")"

BOLD=$(tput bold 2>/dev/null || echo "")
DIM=$(tput dim 2>/dev/null || echo "")
GREEN=$(tput setaf 2 2>/dev/null || echo "")
YELLOW=$(tput setaf 3 2>/dev/null || echo "")
BLUE=$(tput setaf 4 2>/dev/null || echo "")
RESET=$(tput sgr0 2>/dev/null || echo "")

say()  { echo "${BLUE}▸${RESET} $*"; }
ok()   { echo "${GREEN}✓${RESET} $*"; }
warn() { echo "${YELLOW}!${RESET} $*"; }

# ── 1. Python version check ───────────────────────────────────────────────
say "Checking Python..."
if ! command -v python >/dev/null; then
    echo "${YELLOW}Python 3 not found. Install Python 3.10+ from python.org first.${RESET}"
    exit 1
fi
PY_VER=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
ok "Python ${PY_VER} detected"

# ── 2. Virtual environment ────────────────────────────────────────────────
if [ ! -d .venv ]; then
    say "Creating virtual environment (.venv/)..."
    python -m venv .venv
    ok "venv created"
else
    ok "venv already exists"
fi

# ── 3. Python dependencies ────────────────────────────────────────────────
say "Installing Python dependencies..."
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q
ok "ADK + dependencies installed"

# ── 4. .env file ──────────────────────────────────────────────────────────
if [ ! -f .env ]; then
    cp .env.example .env
    warn "Created .env from .env.example — edit it and add your GOOGLE_API_KEY"
    warn "Get a free key at: https://aistudio.google.com/apikey"
else
    ok ".env already configured"
fi

# ── 5. Gemini CLI ─────────────────────────────────────────────────────────
echo ""
say "Checking Gemini CLI (optional, for vibe-coding bonus step)..."
if command -v gemini >/dev/null 2>&1; then
    GEMINI_VER=$(gemini --version 2>/dev/null || echo "?")
    ok "Gemini CLI already installed (${GEMINI_VER})"
else
    if ! command -v npm >/dev/null 2>&1; then
        warn "npm not found — skipping Gemini CLI install."
        warn "Install Node.js from https://nodejs.org, then re-run ./setup.sh"
    else
        echo ""
        read -rp "Install Gemini CLI now via npm? [Y/n] " ans
        ans=${ans:-Y}
        if [[ "$ans" =~ ^[Yy]$ ]]; then
            say "Installing @google/gemini-cli globally..."
            npm install -g @google/gemini-cli
            ok "Gemini CLI installed — run 'gemini' to start"
        else
            warn "Skipped. Install later with: npm install -g @google/gemini-cli"
        fi
    fi
fi

# ── Done ──────────────────────────────────────────────────────────────────
echo ""
echo "${BOLD}Setup complete.${RESET}"
echo ""
echo "Next steps:"
echo "  ${DIM}1.${RESET} Edit ${BOLD}.env${RESET} and add your GOOGLE_API_KEY"
echo "  ${DIM}2.${RESET} ${BOLD}source .venv/bin/activate${RESET}"
echo "  ${DIM}3.${RESET} ${BOLD}adk web${RESET}     ${DIM}# launches the agent playground${RESET}"
echo ""
echo "Workshop: open ${BOLD}index.html${RESET} in your browser."
