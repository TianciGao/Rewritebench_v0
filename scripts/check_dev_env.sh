#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT_DIR="${REPO_ROOT}/output/reports/dev_env_check_${TIMESTAMP}"
REPORT_PATH="${REPORT_DIR}/environment_report.txt"

mkdir -p "${REPORT_DIR}"
cd "${REPO_ROOT}"

log_line() {
  printf "%s\n" "$*" | tee -a "${REPORT_PATH}"
}

run_command() {
  log_line ""
  log_line "$ $*"
  "$@" 2>&1 | tee -a "${REPORT_PATH}"
  local status
  status=${PIPESTATUS[0]}
  if [[ "${status}" -ne 0 ]]; then
    log_line "Command failed with exit status ${status}: $*"
    exit "${status}"
  fi
}

run_shell() {
  log_line ""
  log_line "$ $*"
  bash -lc "$*" 2>&1 | tee -a "${REPORT_PATH}"
  local status
  status=${PIPESTATUS[0]}
  if [[ "${status}" -ne 0 ]]; then
    log_line "Command failed with exit status ${status}: $*"
    exit "${status}"
  fi
}

log_line "Rewritebench developer environment check"
log_line "Repository: ${REPO_ROOT}"
log_line "Report: ${REPORT_PATH}"

if [[ -r /etc/os-release ]]; then
  log_line ""
  log_line "## OS"
  sed -n '1,12p' /etc/os-release | tee -a "${REPORT_PATH}"
else
  log_line "OS: /etc/os-release not found"
fi

run_command uname -a
run_command git --version
run_command java -version
run_command psql --version
run_command mysql --version

if [[ ! -f .venv/bin/activate ]]; then
  log_line ".venv is missing. Run: bash scripts/setup_dev_env_ubuntu.sh"
  exit 1
fi

# shellcheck source=/dev/null
source .venv/bin/activate

run_command python --version
run_command pip --version
run_shell "PYTHONPATH=src python -m cli.main --help"
run_shell "PYTHONPATH=src python -m cli.main user pocr-diagnostic --help"
run_shell "PYTHONPATH=src python -m cli.main user pocr-aggregate --help"
run_command pytest tests/pocr -q
run_command pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q

log_line ""
log_line "Environment check complete."
log_line "Local report written to: ${REPORT_PATH}"
