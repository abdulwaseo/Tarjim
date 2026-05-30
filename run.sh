#!/bin/bash

# ─────────────────────────────────────────────────────────────────────────────
# TARJIM STARTUP AUTOMATION SCRIPT
# ─────────────────────────────────────────────────────────────────────────────

# 1. Clean the terminal window
clear

echo -e "\033[36m"
echo "  ════════════════════════════════════════════════════════════"
echo "   🌍  Tarjim · Arabic → English Real-Time Voice Web Launcher"
echo "  ════════════════════════════════════════════════════════════"
echo -e "\033[0m"

# 2. Check if a local .env file exists, otherwise look for system variables
if [ -f .env ]; then
    echo -e "  [+] Found \033[32m.env\033[0m file configuration. Injecting keys..."
    export $(cat .env | xargs)
fi

# 3. Guard rail validation check for active Deepgram Credentials
if [ -z "$DEEPGRAM_API_KEY" ]; then
    echo -e "  \033[31m[ERROR] DEEPGRAM_API_KEY is not defined anywhere!\033[0m"
    echo "  Please provide your key directly below."
    read -p "  Enter Deepgram API Key: " user_key
    if [ -z "$user_key" ]; then
        echo "  Exiting initialization..."
        exit 1
    fi
    export DEEPGRAM_API_KEY=$user_key
fi

# 4. Spin up the FastAPI Web Infrastructure
echo -e "  [+] Initializing asynchronous web engine...\n"
python3 server.py