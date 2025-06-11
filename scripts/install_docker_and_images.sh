#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# install_docker_and_images.sh
# Ubuntu/Debian 系 Linux 向け:
#   1. Docker Engine / CLI / Compose を公式リポジトリからインストール
#   2. オフライン開発で必要なイメージを事前に pull してキャッシュ
#
# オンライン環境で一度だけ実行してください。
# -----------------------------------------------------------------------------
set -euo pipefail

POSTGRES_IMAGE="postgres:15-alpine"
USER="${USER:-Pavarotti}"

# --------------------
# 1) Install Docker
# --------------------
if command -v docker >/dev/null 2>&1; then
  echo "Docker already installed: $(docker --version)"
else
  echo "==> Installing Docker Engine (requires sudo)"
  sudo apt-get update
  sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

  # Add Docker’s official GPG key
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg

  # Add the repository to Apt sources
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin

  echo "==> Docker installed successfully"
  sudo usermod -aG docker "$USER" || true
  echo "You may need to log out and log back in for group changes to take effect."
fi

# --------------------
# 2) Pull required images
# --------------------
echo "==> Pulling required Docker images..."
docker pull "${POSTGRES_IMAGE}"

echo "==> Done. Cached images:"
docker images "${POSTGRES_IMAGE}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
