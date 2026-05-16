#!/bin/bash
# Recon113 - Quick Setup Script for Kali Linux
# Author: Megh

echo ""
echo "  Recon113 - Setup Script"
echo "  ========================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Install with: sudo apt install python3"
    exit 1
fi

# Setup virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv

echo "[*] Activating virtual environment..."
source venv/bin/activate

echo "[*] Installing Python dependencies..."
pip install -r requirements.txt

# Check/install SecLists
if [ -d "/usr/share/seclists" ]; then
    echo "[✓] SecLists found at /usr/share/seclists"
elif [ -d "$HOME/SecLists" ]; then
    echo "[✓] SecLists found at ~/SecLists"
else
    echo "[*] Installing SecLists (industry-standard wordlists)..."
    echo "    You can also install via: sudo apt install seclists"
    read -p "    Auto-download SecLists from GitHub? (y/n): " choice
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        git clone --depth 1 https://github.com/danielmiessler/SecLists.git ~/SecLists
        echo "[✓] SecLists installed to ~/SecLists"
    else
        echo "[!] Skipped. Install later with: sudo apt install seclists"
    fi
fi

echo ""
echo "[✓] Setup complete!"
echo ""
echo "  To use Recon113:"
echo "    source venv/bin/activate"
echo "    python3 recon113.py -t <target>"
echo ""
