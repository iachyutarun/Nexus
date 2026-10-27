#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH:-}"
python3 "${SCRIPT_DIR}/nexus/app/bootstrap.py"
if [ $? -ne 0 ]; then
    echo "Failed to start NEXUS. Ensure Python 3 is installed."
    read -p "Press Enter to exit..."
fi
