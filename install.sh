#!/bin/bash
set -e

echo "🏠 Installing airbnb-search..."

if command -v uv &>/dev/null; then
  echo "Using uv..."
  uv tool install airbnb-search
elif command -v pipx &>/dev/null; then
  echo "Using pipx..."
  pipx install airbnb-search
elif command -v pip3 &>/dev/null; then
  echo "Using pip3..."
  pip3 install --user airbnb-search
elif command -v pip &>/dev/null; then
  echo "Using pip..."
  pip install --user airbnb-search
else
  echo "❌ No Python package manager found (uv, pipx, or pip)"
  echo "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

echo ""
echo "✅ airbnb-search installed!"
echo ""
echo "Try it:"
echo "  airbnb-search \"Denver, CO\" --checkin 2025-03-01 --checkout 2025-03-03"
