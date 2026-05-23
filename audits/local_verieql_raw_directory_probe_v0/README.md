# local_verieql_raw_directory_probe_v0

## Verdict

Audit verdict: `verieql_source_present_but_not_directly_reusable_by_current_wrapper`.

The raw directory `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql` is not itself the VeriEQL source root. It contains notes plus a nested staged source checkout at:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

That staged directory looks like VeriEQL source: it has `README.md`, `requirements.txt`, `__main__.py`, `parallel/`, `benchmarks/`, verifier modules, parser modules, and a nested Git checkout from `https://github.com/VeriEQL/VeriEQL.git`.

## Direct Reuse Status

The source tree is not currently usable as a direct `SQLRB_VERIEQL_CMD` for the existing release-repo wrapper.

Reasons:

- The active Python used for the probe is `/home/tianci_gao/code/sql-rewrite-bench/.venv/bin/python`.
- Required dependencies are missing in that environment, including `ujson`, `z3`, `ordered_set`, `lark`, `prettytable`, and `mysql.connector`.
- `python -m parallel.cli_within_timeout --help` fails before argparse help because `ujson` is missing.
- `python -m __main__ --help` fails with `ValueError: __main__.__spec__ is None`.
- VeriEQL's documented batch CLI expects `-f <jsonlines> -t <timeout> -o <out>`.
- The current release wrapper calls an available command as `command source.sql comparison.sql [--schema schema]`, which does not match the VeriEQL batch CLI contract.

## Answers

1. Does this directory look like VeriEQL source?
   Yes, under `staged/VeriEQL`.

2. Does it contain a runnable entrypoint?
   It contains entrypoint source files, especially `parallel/cli_within_timeout.py` and `__main__.py`, but the help probes do not currently run successfully in the active Python environment.

3. Does it require a Python environment or dependencies not currently installed?
   Yes. The current probe environment is missing several packages listed in `requirements.txt`.

4. What should `SQLRB_VERIEQL_ROOT` be?
   If a future adapter supports it, the root should be:

   ```text
   /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
   ```

5. What should `SQLRB_VERIEQL_CMD` be?
   No direct current value is sufficient for the existing wrapper. A future adapter could use a Python command similar to `python -m parallel.cli_within_timeout`, but only with the correct working directory, dependencies installed, generated JSONL input, and output parsing.

6. Can the current wrapper use it directly?
   No. A small adapter adjustment is needed to support `SQLRB_VERIEQL_ROOT`, generate VeriEQL JSONL pair input, run the module from the VeriEQL root, pass `-f/-t/-o`, and parse the JSONL output.

7. Was code changed?
   No.

## Boundary

No files were copied, no dependencies were installed, no verifier experiment was run, no Semantic Equivalence Rate was computed, and no reports/results/retained evidence/leaderboard output was updated or promoted.
