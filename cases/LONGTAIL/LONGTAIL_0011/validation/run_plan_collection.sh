#!/usr/bin/env bash
set -euo pipefail

CASE_ID="LONGTAIL_0011"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<USAGE
Usage: $0 --engine <postgres|mysql|spark> --target <source|positive|negative|all> --out <local_output_dir>

Thin v2 plan-collection wrapper for ${CASE_ID}.
Future shared plan collection must resolve executable schema through manifest
schema_ref.profile and the external schema package. This wrapper does not call
legacy engine-specific scripts and must not write to case-local runs/.
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
  echo "Refusing to write plan output to case-local runs/." >&2
  exit 2
fi

echo "${CASE_ID}: shared v2 plan collection runner not implemented; use future shared runner." >&2
echo "No legacy engine-specific scripts, case-local schema/<engine>/ paths, DB engines, plan collection, official metrics, paper outputs, retained evidence, or leaderboard outputs were run or written." >&2
exit 2
