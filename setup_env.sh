#!/usr/bin/env bash
# ----------------------------------------
# setup_env.sh
# 仮想環境の作成・有効化と依存関係インストールを行うスクリプト
# ----------------------------------------
set -euo pipefail

PYTHON="${PYTHON:-python3}"
VENV_DIR=".venv"

echo "==> Checking virtual environment..."
if [[ ! -d "${VENV_DIR}" ]]; then
  echo "    Creating virtual environment at ${VENV_DIR}"
  "${PYTHON}" -m venv "${VENV_DIR}"
fi

echo "==> Activating virtual environment"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "==> Preparing dependencies (online first run / offline thereafter)"
VENDOR_DIR="vendor"
mkdir -p "${VENDOR_DIR}"

# If wheels are already cached, install offline; otherwise download first
if [[ -n "$(ls -A "${VENDOR_DIR}" 2>/dev/null)" ]]; then
  echo "    Found cached wheels in ${VENDOR_DIR}. Installing offline..."
  pip install --no-index --find-links="${VENDOR_DIR}" -r requirements.txt
else
  echo "    No cached wheels found. Downloading now (requires internet)..."
  pip install --upgrade pip
  pip download -r requirements.txt -d "${VENDOR_DIR}"
  echo "    Installing from freshly downloaded wheels..."
  pip install --no-index --find-links="${VENDOR_DIR}" -r requirements.txt
fi

echo
echo "Environment ready. Activate with: source ${VENV_DIR}/bin/activate"
echo "Run the server separately, e.g.: uvicorn app.main:app --reload"
