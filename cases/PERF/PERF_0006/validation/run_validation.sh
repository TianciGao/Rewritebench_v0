#!/usr/bin/env bash
set -euo pipefail

CASE_ID="PERF_0006"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<USAGE
Usage: $0 --engine <postgres|mysql|spark> --target <source|positive|negative|all> --out <local_output_dir>

Thin v2 validation wrapper for ${CASE_ID}.
This branch task does not run DB engines or checkers. Future implementation
should dispatch to shared repository logic and write only to the explicit
--out directory, never to case-local runs/.
USAGE
}

engine=""
target="all"
out_dir=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --engine) engine="${2:-}"; shift 2 ;;
    --target) target="${2:-}"; shift 2 ;;
    --out) out_dir="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "${engine}" in
  postgres|mysql|spark) ;;
  *) echo "Missing or unsupported --engine: ${engine}" >&2; usage >&2; exit 2 ;;
esac

case "${target}" in
  source|positive|negative|all) ;;
  *) echo "Unsupported --target: ${target}" >&2; usage >&2; exit 2 ;;
esac

if [[ -z "${out_dir}" ]]; then
  echo "Missing required --out <local_output_dir>" >&2
  usage >&2
  exit 2
fi

if [[ "${out_dir}" == "${CASE_DIR}/runs" || "${out_dir}" == "${CASE_DIR}/runs/"* ]]; then
  echo "Refusing to write validation output to case-local runs/." >&2
  exit 2
fi

echo "${CASE_ID}: v2 validation wrapper is present but shared validation execution is not implemented in this branch task." >&2
echo "No DB engines, checkers, official metrics, paper outputs, retained evidence, or leaderboard outputs were run or written." >&2
exit 2
