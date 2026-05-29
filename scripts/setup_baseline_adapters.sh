#!/usr/bin/env bash
set -euo pipefail

PROFILE="core"
REPO_ROOT="$(pwd)"
CALCITE_RUNTIME_ROOT=""
CALCITE_RUNTIME_ARCHIVE=""
NO_INSTALL=0
FORCE=0

usage() {
  cat <<'EOF'
Usage:
  bash scripts/setup_baseline_adapters.sh [options]

Options:
  --profile core|calcite|prior-adapted|all-safe
  --repo-root <path>
  --calcite-runtime-root <path>
  --calcite-runtime-archive <tar.gz>
  --no-install
  --force
  -h, --help

This script installs/checks adapter prerequisites only. It does not call APIs,
run baselines, run DB/checker/timing, run Track A 120, or update reports/results.
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
    --calcite-runtime-root)
      CALCITE_RUNTIME_ROOT="${2:?missing value for --calcite-runtime-root}"
      shift 2
      ;;
    --calcite-runtime-archive)
      CALCITE_RUNTIME_ARCHIVE="${2:?missing value for --calcite-runtime-archive}"
      shift 2
      ;;
    --no-install)
      NO_INSTALL=1
      shift
      ;;
    --force)
      FORCE=1
      shift
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

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  printf "PASS: %s\n" "$*"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  printf "WARN: %s\n" "$*"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  printf "FAIL: %s\n" "$*"
}

require_path() {
  local path="$1"
  local label="$2"
  if [[ -e "${path}" ]]; then
    pass "${label}: ${path}"
  else
    fail "${label} missing: ${path}"
  fi
}

optional_path() {
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

activate_venv_if_available() {
  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    pass "Using active virtualenv: ${VIRTUAL_ENV}"
  elif [[ -f "${REPO_ROOT}/.venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "${REPO_ROOT}/.venv/bin/activate"
    pass "Activated repo .venv"
  else
    warn "No active venv and no repo .venv; run scripts/setup_dev_env_ubuntu.sh before installing Python deps"
  fi
}

run_python_check() {
  local py
  py="$(python_cmd)"
  "${py}" - <<'PY'
import importlib
import sys

for name in ("sqlglot", "pytest"):
    module = importlib.import_module(name)
    version = getattr(module, "__version__", "unknown")
    print(f"{name}={version}")
print(f"python={sys.executable}")
PY
}

run_cli_help_check() {
  local py
  py="$(python_cmd)"
  PYTHONPATH=src "${py}" -m cli.main --help >/dev/null
  PYTHONPATH=src "${py}" -m cli.main user pocr-diagnostic --help >/dev/null
  PYTHONPATH=src "${py}" -m cli.main user pocr-aggregate --help >/dev/null
  pass "CLI help checks passed"
}

install_core_python_deps() {
  activate_venv_if_available
  if [[ "${NO_INSTALL}" -eq 1 ]]; then
    warn "--no-install set; skipping pip install"
    return
  fi
  if [[ -z "${VIRTUAL_ENV:-}" && ! -f "${REPO_ROOT}/.venv/bin/python" ]]; then
    warn "Skipping pip install because no venv is active or available"
    return
  fi
  local py
  py="$(python_cmd)"
  "${py}" -m pip install -e ".[sqlglot]"
  "${py}" -m pip install pytest
  pass "Python adapter dependencies installed"
}

profile_core() {
  echo "== core profile =="
  install_core_python_deps
  run_python_check && pass "Python package checks passed" || fail "Python package checks failed"
  run_cli_help_check || fail "CLI help checks failed"
  require_path "baselines/sqlglot/sqlglot_user_adapter.py" "SQLGlot adapter"
  require_path "baselines/direct_llm_original/adapter.py" "Direct LLM original adapter"
  require_path "baselines/direct_llm_repair_1/adapter.py" "Direct LLM Repair-1 adapter"
  echo "No API call is made. No baseline execution is performed."
}

verify_calcite_root() {
  local root="$1"
  if [[ -z "${root}" ]]; then
    root="${SQLRB_CALCITE_HEP_ROOT:-}"
  fi
  if [[ -z "${root}" && -d "${HOME}/.local/share/sqlrb/calcite_hep" ]]; then
    root="${HOME}/.local/share/sqlrb/calcite_hep"
  fi
  if [[ -z "${root}" ]]; then
    warn "No Calcite runtime root provided or discovered"
    return
  fi
  optional_path "${root}" "Calcite runtime root"
  optional_path "${root}/bin" "Calcite runtime bin/"
  optional_path "${root}/classes" "Calcite runtime classes/"
  optional_path "${root}/src" "Calcite runtime src/"
  optional_path "${root}/classpath.txt" "Calcite runtime classpath.txt"
  echo "Calcite env hints:"
  echo "  export SQLRB_CALCITE_HEP_ROOT=\"${root}\""
  echo "  export SQLRB_CALCITE_HEP_CMD=\"${root}/bin/calcite-hep-rewrite-smoke\""
  echo "  export SQLRB_CALCITE_HEP_CLASSPATH=\"\$(cat \"${root}/classpath.txt\")\""
}

maybe_unpack_calcite_archive() {
  if [[ -z "${CALCITE_RUNTIME_ARCHIVE}" ]]; then
    return
  fi
  if [[ ! -f "${CALCITE_RUNTIME_ARCHIVE}" ]]; then
    fail "Calcite runtime archive not found: ${CALCITE_RUNTIME_ARCHIVE}"
    return
  fi
  local target_base="${HOME}/.local/share/sqlrb"
  local target_dir="${target_base}/calcite_hep"
  mkdir -p "${target_base}"
  if [[ -e "${target_dir}" && "${FORCE}" -ne 1 ]]; then
    fail "Calcite runtime target already exists; use --force to allow archive extraction: ${target_dir}"
    return
  fi
  tar -xzf "${CALCITE_RUNTIME_ARCHIVE}" -C "${target_base}"
  pass "Calcite runtime archive extracted under ${target_base}"
}

profile_calcite() {
  echo "== calcite profile =="
  require_path "baselines/calcite_hep_fail_closed/adapter.py" "Calcite HEP adapter"
  if command -v java >/dev/null 2>&1; then
    local version_text
    version_text="$(java -version 2>&1 | head -1)"
    if [[ "${version_text}" == *\"17* || "${version_text}" == *" 17"* ]]; then
      pass "Java 17 check: ${version_text}"
    else
      warn "Java found but not clearly Java 17: ${version_text}"
    fi
  else
    fail "java not found"
  fi
  maybe_unpack_calcite_archive
  verify_calcite_root "${CALCITE_RUNTIME_ROOT}"
  echo "Calcite is optional/external. This script does not build Calcite or download Calcite source/JARs."
}

redacted_env_status() {
  local prefix="$1"
  local any=0
  while IFS='=' read -r name _; do
    if [[ "${name}" == "${prefix}"* ]]; then
      any=1
      if [[ "${name}" =~ (KEY|TOKEN|SECRET|PASSWORD|AUTHORIZATION|BEARER|API_KEY) ]]; then
        printf "  %s=<REDACTED>\n" "${name}"
      else
        printf "  %s=<set>\n" "${name}"
      fi
    fi
  done < <(env | sort)
  if [[ "${any}" -eq 0 ]]; then
    printf "  %s*: <unset>\n" "${prefix}"
  fi
}

profile_prior_adapted() {
  echo "== prior-adapted profile =="
  require_path "baselines/rbot/adapter.py" "R-Bot adapted wrapper"
  require_path "baselines/llm_r2/adapter.py" "LLM-R2 adapted wrapper"
  require_path "baselines/learnedrewrite/adapter.py" "LearnedRewrite wrapper"
  echo "Status: adapted wrapper present; official upstream runtime not confirmed."
  echo "Redacted optional env names:"
  redacted_env_status "SQLRB_RBOT_"
  redacted_env_status "SQLRB_LLM_R2_"
  redacted_env_status "SQLRB_LEARNEDREWRITE_"
  redacted_env_status "SQLRB_LLM_"
  echo "No API call is made. No official upstream runtime is installed."
}

case "${PROFILE}" in
  core)
    profile_core
    ;;
  calcite)
    profile_calcite
    ;;
  prior-adapted)
    profile_prior_adapted
    ;;
  all-safe)
    profile_core
    profile_calcite
    profile_prior_adapted
    ;;
esac

echo "Summary: PASS=${PASS_COUNT} WARN=${WARN_COUNT} FAIL=${FAIL_COUNT}"
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
  exit 1
fi
