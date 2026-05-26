# Baseline Reproduction Manual

This manual explains local diagnostic reproduction paths for SQL-RewriteBench baseline routes. It is for fresh users, reviewers, and maintainers who want to reproduce candidate SQL capture, optional execution/checker status, optional timing, and local diagnostic summaries in a D035-aligned way.

This manual does not create official metrics. It does not update paper-facing reports/results. It does not promote retained evidence. No global leaderboard is produced. Outputs should use D035-style output roots:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

## First-Time Setup

Clone and enter the repository:

```bash
git clone https://github.com/TianciGao/Rewritebench_v0.git
cd Rewritebench_v0
git checkout feature/case-package-v2-external-schema
```

Use Python 3.10 or newer, then create and activate a virtual environment:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

Install optional SQLGlot support only if you will run SQLGlot routes:

```bash
python -m pip install -e ".[sqlglot]"
```

Commands are available through either installed or checkout mode:

```bash
sqlrb user show-output-schema
PYTHONPATH=src python -m cli.main user show-output-schema
```

Safe smoke commands that do not require DB engines:

```bash
PYTHONPATH=src python -m cli.main user list-cases \
  --case-set common_core_v0 \
  --engines postgres

PYTHONPATH=src python -m cli.main user explain-selection \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke

PYTHONPATH=src python -m cli.main user show-output-schema

PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_dry_run \
  --dry-run

PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_adapter_capture
```

External tools for full local diagnostics:

- PostgreSQL server/client and `psql` availability.
- MySQL server/client availability.
- Spark / PySpark availability.
- Java availability for Spark and Calcite.
- Calcite HEP runtime configuration if using Calcite:
  - `SQLRB_CALCITE_HEP_CMD`
  - `SQLRB_CALCITE_HEP_JAR`
  - `SQLRB_CALCITE_HEP_ROOT`
- SQLGlot optional dependency for SQLGlot routes.
- LLM/API configuration is not needed for deterministic baselines and should not be used by default.

If you document OS package installation commands locally, treat them as example Ubuntu/WSL setup notes, not benchmark commands.

## Preflight Checklist

Repository and CLI:

```bash
pwd
git branch --show-current
git status -sb
PYTHONPATH=src python -m cli.main user show-output-schema
python - <<'PY'
import sql_rewrite_bench
print("sql_rewrite_bench import ok")
PY
```

SQLGlot availability, if needed:

```bash
python - <<'PY'
import sqlglot
print(sqlglot.__version__)
PY
```

PostgreSQL availability:

```bash
psql "$SQLRB_POSTGRES_DSN" -c "SELECT 1;"
```

MySQL availability:

```bash
mysql -e "SELECT 1;"
```

Spark availability:

```bash
python - <<'PY'
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("sqlrb-preflight").getOrCreate()
spark.sql("SELECT 1").collect()
spark.stop()
print("spark ok")
PY
```

Java availability:

```bash
java -version
```

Calcite runtime environment, if needed:

```bash
python - <<'PY'
import os
for name in ("SQLRB_CALCITE_HEP_CMD", "SQLRB_CALCITE_HEP_JAR", "SQLRB_CALCITE_HEP_ROOT"):
    print(f"{name}={'set' if os.getenv(name) else 'missing'}")
PY
```

If DB engines are unavailable, you can still run adapter-capture smoke, but you cannot reproduce execution/checker/timing diagnostics. If Calcite runtime environment is missing, Calcite HEP must be reported as preflight-blocked, not fabricated.

## User Output Contract

User-facing outputs belong under:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

Do not commit output/. Do not write local user outputs to top-level `reports/` or top-level `results/`. Do not write new outputs into case-local `runs/`.

The current implementation may use internal transitional `runs/user/<run_id>/` staging before export. Treat `output/` as the public user-facing output surface.

## Common Command Pattern

Track A same-engine reproduction over Common-core v0 uses 40 cases x PostgreSQL/MySQL/Spark = 120 planned rows.

Generic deterministic baseline run:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "<adapter command>" \
  --output-root output \
  --run-id <run_id> \
  --enable-db-execution \
  --enable-checker \
  --collect-timing \
  --timing-repetitions 5 \
  --timing-timeout 30
```

With multiple engines, `user evaluate` creates per-engine source run ids named `<run_id>__postgres`, `<run_id>__mysql`, and `<run_id>__spark`. To compute aggregate non-official local diagnostics from those existing source runs:

```bash
PYTHONPATH=src python -m cli.main user compute-local-metrics \
  --run-id-prefix <run_id> \
  --engines postgres,mysql,spark \
  --aggregate-run-id <run_id> \
  --source-run-root runs/user \
  --output-root output
```

For a single-engine run:

```bash
PYTHONPATH=src python -m cli.main user compute-local-metrics \
  --run-id <run_id> \
  --source-run-root runs/user \
  --output-root output
```

These are local diagnostic metrics only. No paper-facing metric is promoted.

## Canonical Timing Policy

Performance is interpreted only over exact+timed rows.

Speedup direction is:

```text
source median runtime / candidate median runtime
```

Canonical SQLGlot deterministic runs used 5 measured repetitions. Use `--timing-repetitions 5` when reproducing canonical-compatible local diagnostics. Two-repetition runs can be useful pipeline smokes, but they should not replace canonical performance values because timing provenance differs.

## Baseline Routes

### Source / Native Controls

Source SQL controls are the case-local `sql/source.sql` queries. They are reference inputs for execution/checker comparisons and timing baselines. They are not method-generated rewrite candidates.

### Human Positive Controls

Human positive controls are case-local positive rewrites, usually `sql/pos_01.sql`. They are calibration/checker references and POCR control inputs. They are not automatic rewrite baselines and should not be merged into method route outputs.

### Hard-Negative Guard

Hard negatives, usually `sql/neg_01.sql`, are checker controls. They are not method-generated candidates and not POCR baselines.

### SQLGlot No-Op

Install SQLGlot support:

```bash
python -m pip install -e ".[sqlglot]"
```

Adapter command:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

Track A 120 local diagnostic pattern:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id sqlglot_noop_track_a_120_local \
  --enable-db-execution \
  --enable-checker \
  --collect-timing \
  --timing-repetitions 5 \
  --timing-timeout 30
```

Generated rows may be fewer than 120 if parse/emit fails. Missing rows must remain visible. Candidate outputs and metrics are local diagnostic unless separately promoted.

### SQLGlot Optimize Schema-Aware

Install SQLGlot support:

```bash
python -m pip install -e ".[sqlglot]"
```

Adapter command:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware
```

Track A 120 local diagnostic pattern:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware" \
  --output-root output \
  --run-id sqlglot_optimize_schema_aware_track_a_120_local \
  --enable-db-execution \
  --enable-checker \
  --collect-timing \
  --timing-repetitions 5 \
  --timing-timeout 30
```

This route must not silently downgrade to SQLGlot no-op or schema-unaware optimize. Missing and unsupported rows remain visible in manifests and local diagnostics.

### Calcite HEP Fail-Closed

Calcite HEP requires Java plus an external Calcite runtime. The repository adapter discovers runtime configuration through:

- `SQLRB_CALCITE_HEP_CMD`
- `SQLRB_CALCITE_HEP_JAR`
- `SQLRB_CALCITE_HEP_ROOT`
- `SQLRB_CALCITE_HEP_JAVA`
- `SQLRB_CALCITE_HEP_MODE`
- `SQLRB_CALCITE_HEP_TIMEOUT`

Adapter command:

```bash
python baselines/calcite_hep_fail_closed/adapter.py
```

If runtime environment is missing, Calcite HEP is preflight-blocked. Do not fabricate candidates.

### Direct LLM Original

Direct LLM original is an LLM SQL-in/SQL-out baseline route:

```bash
python baselines/direct_llm_original/adapter.py
```

Live generation requires explicit user-facing LLM/API configuration and an explicit live gate such as `SQLRB_LLM_ALLOW_LIVE=1`. Do not expose API keys. Rerunning LLM routes may change outputs unless model, prompt, decoding, provider, and call metadata are frozen. Existing candidate SQL artifacts may already exist in local `runs/user` or D035 `output/` roots. Any rerun is local diagnostic unless separately authorized.

### Direct LLM + Repair-1

Direct LLM Repair-1 is a feedback-enhanced LLM route:

```bash
python baselines/direct_llm_repair_1/adapter.py
```

It consumes explicit original-candidate and feedback context. It is a separate route and should not be merged with Direct LLM original. Exact/timed metrics must retain route identity.

### R-Bot Adapted GPT-5.4 PG40

R-Bot adapted GPT-5.4 is a PostgreSQL-only PG40 local diagnostic route in this repository. It is not original R-Bot paper reproduction unless the official runtime, RAG, Chroma, and CalciteRewrite stack are used under a separate authorization.

PG40 cannot fill Track A 120. Candidate roots from the inventory can support PostgreSQL-only diagnostic review, not tri-engine Track A replacement.

### LLM-R2 Adapted GPT-5.4 PG40

LLM-R2 adapted GPT-5.4 is a PostgreSQL-only PG40 local diagnostic route. It is not original LLM-R2 paper runtime unless the official runtime, checkpoints, rule system, and demonstration selector are used under a separate authorization.

PG40 cannot fill Track A 120.

### LearnedRewrite PG40

LearnedRewrite is currently a PostgreSQL-only external wrapper route in this repository. Current inventory found incomplete PG40 candidate coverage, with only 29 generated candidate files in the relevant manual-inspection rerun. Do not fabricate missing candidates. Incomplete routes must keep missing rows visible.

### SQLSolver / VeriEQL

SQLSolver and VeriEQL are verifier support paths, not rewrite-generation baselines. They do not produce candidate SQL for POCR and should not enter same-engine speedup or POCR baseline tables.

## Baseline Summary Table

| Baseline / route | Role | Scope | Requires DB? | Requires timing? | Requires SQLGlot? | Requires Java/Calcite? | Requires LLM/API? | Can produce candidate SQL? | Can be used for POCR diagnostic? | Paper-facing promotion status |
|---|---|---|---|---|---|---|---|---|---|---|
| Source / native controls | reference source | PG/MySQL/Spark by case | yes for execution | yes for source timing | no | Spark may need Java | no | no | no | reference only |
| Human positive controls | checker/calibration control | case-local | optional | optional | no | no | no | yes, as controls | yes, as controls | not method baseline |
| Hard-negative guard | checker control | case-local | optional | no | no | no | no | no | no | not method output |
| SQLGlot no-op | deterministic baseline | Track A 120 when engines available | yes for full diagnostics | yes for speedup | yes | no | no | yes | yes | local diagnostic unless promoted |
| SQLGlot optimize schema-aware | deterministic baseline | Track A 120 when engines/schema supported | yes for full diagnostics | yes for speedup | yes | no | no | yes | yes | local diagnostic unless promoted |
| Calcite HEP fail-closed | deterministic external baseline | Track A 120 only when runtime configured | yes for full diagnostics | yes for speedup | no | yes | no | yes if runtime succeeds | yes | blocked if runtime env missing |
| Direct LLM original | LLM baseline | route-specific; Track A possible with live config | yes for full diagnostics | yes for speedup | no | no | yes for generation | yes | yes | local diagnostic unless separately authorized |
| Direct LLM + Repair-1 | feedback LLM route | route-specific | yes for full diagnostics | yes for speedup | no | no | yes for generation | yes | yes | separate route only |
| R-Bot adapted GPT-5.4 PG40 | adapted prior method | PostgreSQL PG40 | yes for full diagnostics | yes for speedup | no | no | yes for live adapted route | yes | yes, PG40 only | not original paper reproduction |
| LLM-R2 adapted GPT-5.4 PG40 | adapted prior method | PostgreSQL PG40 | yes for full diagnostics | yes for speedup | no | no | yes for live adapted route | yes | yes, PG40 only | not original paper reproduction |
| LearnedRewrite PG40 | external prior method | PostgreSQL PG40, incomplete | yes for full diagnostics | yes for speedup | no | Java external runtime | no LLM/API in wrapper | partial currently | yes, if complete | incomplete coverage |
| SQLSolver / VeriEQL | verifier support | exact candidate subsets | no DB rerun for existing artifacts | no | no | Java/Python verifier env | no | no | no | support evidence only |

## POCR Relationship

Candidate SQL is input to POCR. Candidate SQL alone is not annotation JSONL. Annotation JSONL requires Stage A annotation. Stage B transformation-aware validation is required for diagnostic operation support. POCR remains diagnostic unless separately promoted.

## Troubleshooting

`sqlrb` command not found:

- Use checkout mode: `PYTHONPATH=src python -m cli.main user ...`.
- Or reinstall editable package: `python -m pip install -e .`.

Missing `PYTHONPATH`:

- Prefix checkout commands with `PYTHONPATH=src`.

SQLGlot not installed:

- Install optional dependency with `python -m pip install -e ".[sqlglot]"`.

PostgreSQL/MySQL/Spark unavailable:

- Adapter-capture smoke can still run.
- Full execution/checker/timing reproduction cannot run until engines are configured.

Calcite runtime missing:

- Report Calcite HEP as preflight-blocked.
- Do not fabricate missing candidates.

Zero generated candidates:

- Inspect adapter status files under the run workspace and D035 logs.
- Keep all missing rows visible in manifests and failure buckets.

Timed rows missing:

- Timing is exact-gated and requires `--collect-timing`, `--enable-db-execution`, and `--enable-checker`.

GM differs from canonical:

- Check timing repetitions, timeout, runtime provenance, exact+timed row eligibility, and engine environment. Canonical deterministic SQLGlot timing used 5 measured repetitions.

`output/` appears untracked:

- This is expected for local runs. Do not commit output/.

POCR replay route mismatch:

- Annotation JSONL artifacts are route-bound. A route mismatch must fail closed rather than silently reuse annotation evidence.

## Boundaries

- local diagnostic reproduction only.
- No paper-facing metric is promoted.
- No global leaderboard is produced.
- Performance is interpreted only over exact+timed rows.
- PG40 cannot fill Track A 120.
- Do not fabricate missing candidates.
- Do not commit output/.
