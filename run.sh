#!/bin/bash
# Script to run the web scraper and start the Flask dashboard

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"

echo "========================================="
echo "Starting Web Scraper & Dashboard"
echo "========================================="
echo ""

# Step 1: Run the scraper
echo "Step 1: Running scraper (main.py)..."
$VENV_PYTHON main.py

if [ $? -eq 0 ]; then
    echo "✓ Scraping completed successfully"
    echo ""
else
    echo "✗ Scraping failed"
    exit 1
fi

# Step 2: Start Flask app
echo "Step 2: Starting Flask dashboard..."
echo ""
echo "========================================="
echo "Dashboard will be available at:"
echo "  http://127.0.0.1:5000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================="
echo ""

$VENV_PYTHON web/app.py
