# Entrypoint Probe

## README Usage

The staged VeriEQL README documents:

- Python 3.10 or later, with Python 3.11 recommended.
- `pip install -r requirements.txt`.
- Optional replacement of z3 Python scripts with files from `z3py_libs/`.
- Toy example:

```text
python -m __main__
```

- Batch timeout CLI:

```text
python -m parallel.cli_within_timeout -f XX.jsonlines -t 600 -o XX.out
```

- Batch bound-size CLI:

```text
python -m parallel.cli_within_bound -f XX.jsonlines -s 10 -o XX.out
```

## Python Version

Probe command:

```bash
python --version
```

Result:

```text
Python 3.12.3
```

The `python` resolved to:

```text
/home/tianci_gao/code/sql-rewrite-bench/.venv/bin/python
```

## Help Probes

### `python -m __main__ --help`

Result:

```text
Error while finding module specification for '__main__' (ValueError: __main__.__spec__ is None)
```

This command did not run a verifier pair.

### `python -m parallel.cli_within_timeout --help`

Result:

```text
ModuleNotFoundError: No module named 'ujson'
```

This command failed before argparse help because dependencies are missing. It did not run a verifier pair.

## Entrypoint Shape

`parallel/cli_within_timeout.py` uses argparse with:

- `-f` / `--file`
- `-s` / `--bound_size`
- `-t` / `--timeout`
- `-m` / `--mode`
- `-c` / `--cores`
- `-i` / `--integrity_constraint`
- `-o` / `--out_file`

The CLI reads JSONL records containing at least:

- `index`
- `schema`
- `constraint`
- `pair`

This is a batch JSONL contract, not a direct two-SQL-file command contract.
