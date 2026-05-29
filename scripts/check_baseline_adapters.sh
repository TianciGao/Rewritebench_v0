#!/usr/bin/env bash
set -euo pipefail

PROFILE="core"
REPO_ROOT="$(pwd)"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/check_baseline_adapters.sh [options]

Options:
  --profile core|calcite|prior-adapted|all-safe
  --repo-root <path>
  -h, --help

Writes a local report under output/reports/baseline_env_check_<timestamp>/.
No API call, DB/checker/timing run, baseline execution, or Track A 120 run is performed.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="${2:?missing value for --profile}"
      shift 2
      ;;
    --repo-root)
      REPO_ROOT="${2:?missing value for --repo-root}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "${PROFILE}" in
  core|calcite|prior-adapted|all-safe) ;;
  *)
    echo "Invalid --profile: ${PROFILE}" >&2
    exit 2
    ;;
esac

REPO_ROOT="$(cd -- "${REPO_ROOT}" && pwd)"
cd "${REPO_ROOT}"

if [[ ! -f pyproject.toml || ! -d baselines || ! -d src/cli ]]; then
  echo "Not a Rewritebench_v0 repository root: ${REPO_ROOT}" >&2
  exit 1
fi

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT_DIR="${REPO_ROOT}/output/reports/baseline_env_check_${TIMESTAMP}"
REPORT_PATH="${REPORT_DIR}/baseline_report.txt"
mkdir -p "${REPORT_DIR}"

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

log() {
  printf "%s\n" "$*" | tee -a "${REPORT_PATH}"
}

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  log "PASS: $*"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  log "WARN: $*"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  log "FAIL: $*"
}

run_version() {
  local label="$1"
  shift
  log ""
  log "## ${label}"
  if "$@" >>"${REPORT_PATH}" 2>&1; then
    pass "${label} available"
  else
    warn "${label} unavailable"
  fi
}

check_file_required() {
  local path="$1"
  local label="$2"
  if [[ -f "${path}" ]]; then
    pass "${label}: ${path}"
  else
    fail "${label} missing: ${path}"
  fi
}

check_file_optional() {
  local path="$1"
  local label="$2"
  if [[ -e "${path}" ]]; then
    pass "${label}: ${path}"
  else
    warn "${label} missing: ${path}"
  fi
}

python_cmd() {
  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    command -v python
    return
  fi
  if [[ -f "${REPO_ROOT}/.venv/bin/python" ]]; then
    printf "%s\n" "${REPO_ROOT}/.venv/bin/python"
    return
  fi
  command -v python3 || command -v python
}

run_help_check() {
  local label="$1"
  shift
  log ""
  log "## ${label}"
  if "$@" >>"${REPORT_PATH}" 2>&1; then
    pass "${label}"
  else
    fail "${label}"
  fi
}

redacted_env_status() {
  local prefix="$1"
  local any=0
  while IFS='=' read -r name _; do
    if [[ "${name}" == "${prefix}"* ]]; then
      any=1
      if [[ "${name}" =~ (KEY|TOKEN|SECRET|PASSWORD|AUTHORIZATION|BEARER|API_KEY) ]]; then
        log "  ${name}=<REDACTED>"
      else
        log "  ${name}=<set>"
      fi
    fi
  done < <(env | sort)
  if [[ "${any}" -eq 0 ]]; then
    log "  ${prefix}*: <unset>"
  fi
}

check_sqlglot_version() {
  local py
  py="$(python_cmd)"
  log ""
  log "## SQLGlot version"
  if "${py}" - <<'PY' >>"${REPORT_PATH}" 2>&1
import sqlglot
print(sqlglot.__version__)
PY
  then
    pass "sqlglot import/version"
  else
    fail "sqlglot missing; run scripts/setup_baseline_adapters.sh --profile core"
  fi
}

check_core() {
  log ""
  log "# core profile"
  check_sqlglot_version
  check_file_required "baselines/sqlglot/sqlglot_user_adapter.py" "SQLGlot adapter"
  check_file_required "baselines/direct_llm_original/adapter.py" "Direct LLM original adapter"
  check_file_required "baselines/direct_llm_repair_1/adapter.py" "Direct LLM Repair-1 adapter"
  local py
  py="$(python_cmd)"
  run_help_check "python -m cli.main --help" env PYTHONPATH=src "${py}" -m cli.main --help
  run_help_check "pocr-diagnostic help" env PYTHONPATH=src "${py}" -m cli.main user pocr-diagnostic --help
  run_help_check "pocr-aggregate help" env PYTHONPATH=src "${py}" -m cli.main user pocr-aggregate --help
}

check_calcite() {
  log ""
  log "# calcite profile"
  check_file_required "baselines/calcite_hep_fail_closed/adapter.py" "Calcite HEP adapter"
  if command -v java >/dev/null 2>&1; then
    local version_text
    version_text="$(java -version 2>&1 | head -1)"
    log "java_version=${version_text}"
    if [[ "${version_text}" == *\"17* || "${version_text}" == *" 17"* ]]; then
      pass "Java 17"
    else
      warn "Java exists but is not clearly Java 17"
    fi
  else
    fail "java not found"
  fi
  local root="${SQLRB_CALCITE_HEP_ROOT:-}"
  if [[ -z "${root}" && -d "${HOME}/.local/share/sqlrb/calcite_hep" ]]; then
    root="${HOME}/.local/share/sqlrb/calcite_hep"
  fi
  if [[ -z "${root}" ]]; then
    warn "Calcite runtime root not configured or discovered"
  else
    log "calcite_runtime_root=${root}"
    check_file_optional "${root}/bin" "Calcite bin/"
    check_file_optional "${root}/classes" "Calcite classes/"
    check_file_optional "${root}/src" "Calcite src/"
    check_file_optional "${root}/classpath.txt" "Calcite classpath.txt"
  fi
  log "Calcite runtime env hints: SQLRB_CALCITE_HEP_ROOT, SQLRB_CALCITE_HEP_CMD, SQLRB_CALCITE_HEP_CLASSPATH"
}

check_prior_adapted() {
  log ""
  log "# prior-adapted profile"
  check_file_required "baselines/rbot/adapter.py" "R-Bot adapted wrapper"
  check_file_required "baselines/llm_r2/adapter.py" "LLM-R2 adapted wrapper"
  check_file_required "baselines/learnedrewrite/adapter.py" "LearnedRewrite wrapper"
  log "official_runtime_status=not_confirmed_for_rbot_llm_r2_learnedrewrite"
  log "adapted_wrapper_status=present"
  log ""
  log "## Redacted API/runtime env names"
  redacted_env_status "SQLRB_RBOT_"
  redacted_env_status "SQLRB_LLM_R2_"
  redacted_env_status "SQLRB_LEARNEDREWRITE_"
  redacted_env_status "SQLRB_LLM_"
}

log "Rewritebench baseline adapter environment check"
log "repository=${REPO_ROOT}"
log "profile=${PROFILE}"
log "report=${REPORT_PATH}"
log "No API call is made. No DB/checker/timing run is performed. No baseline execution is performed."

if [[ -r /etc/os-release ]]; then
  log ""
  log "## OS"
  sed -n '1,12p' /etc/os-release | tee -a "${REPORT_PATH}" >/dev/null
fi

run_version "kernel" uname -a
run_version "git" git --version
run_version "python" "$(python_cmd)" --version
run_version "pip" "$(python_cmd)" -m pip --version
run_version "java" java -version

case "${PROFILE}" in
  core)
    check_core
    ;;
  calcite)
    check_calcite
    ;;
  prior-adapted)
    check_prior_adapted
    ;;
  all-safe)
    check_core
    check_calcite
    check_prior_adapted
    ;;
esac

log ""
log "Summary: PASS=${PASS_COUNT} WARN=${WARN_COUNT} FAIL=${FAIL_COUNT}"
log "Local report written to: ${REPORT_PATH}"
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
  exit 1
fi
