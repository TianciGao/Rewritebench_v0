#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

if [[ ! -r /etc/os-release ]]; then
  echo "This setup script requires Ubuntu or WSL Ubuntu with /etc/os-release." >&2
  exit 1
fi

# shellcheck disable=SC1091
source /etc/os-release
if [[ "${ID:-}" != "ubuntu" ]]; then
  echo "This setup script requires Ubuntu or WSL Ubuntu. Detected ID=${ID:-unknown}." >&2
  exit 1
fi

if [[ "${EUID}" -eq 0 ]]; then
  SUDO=()
elif command -v sudo >/dev/null 2>&1; then
  SUDO=(sudo)
else
  echo "sudo is required when this script is not run as root." >&2
  exit 1
fi

echo "Repository: ${REPO_ROOT}"
echo "Detected Ubuntu: ${PRETTY_NAME:-unknown}"
if grep -qi microsoft /proc/version 2>/dev/null; then
  echo "Detected WSL Ubuntu environment."
fi

cd "${REPO_ROOT}"

APT_PACKAGES=(
  build-essential
  git
  curl
  wget
  unzip
  zip
  jq
  ripgrep
  tree
  python3
  python3-venv
  python3-pip
  openjdk-17-jdk
  postgresql-client
  mysql-client
)

echo "Installing apt packages..."
"${SUDO[@]}" apt-get update
"${SUDO[@]}" apt-get install -y "${APT_PACKAGES[@]}"

if [[ ! -d .venv ]]; then
  echo "Creating .venv..."
  python3 -m venv .venv
else
  echo ".venv already exists; reusing it."
fi

# shellcheck source=/dev/null
source .venv/bin/activate

echo "Upgrading Python packaging tools..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing Rewritebench developer Python dependencies..."
python -m pip install -e ".[sqlglot]"
python -m pip install pytest

cat <<'EOF'

Developer environment setup complete.

Next commands:
  source .venv/bin/activate
  PYTHONPATH=src python -m cli.main --help
  bash scripts/check_dev_env.sh

Notes:
  - API keys are not configured by this script.
  - Database servers and Spark runtime are optional advanced setup.
  - Local reports under output/ are not intended for commit.
EOF
