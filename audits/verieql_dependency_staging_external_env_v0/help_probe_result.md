# Help Probe Result

Command:

```bash
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
```

Working directory:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

Exit code: `0`.

Output:

```text
usage: cli_within_timeout.py [-h] [-f FILE] [-s BOUND_SIZE] [-t TIMEOUT]
                             [-m {train,eval}]
                             [-c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32}]
                             [-i {0,1}] [-o OUT_FILE]

VeriEQL cli

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE
  -s BOUND_SIZE, --bound_size BOUND_SIZE
  -t TIMEOUT, --timeout TIMEOUT
  -m {train,eval}, --mode {train,eval}
  -c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32}, --cores {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32}
  -i {0,1}, --integrity_constraint {0,1}
  -o OUT_FILE, --out_file OUT_FILE
```

Interpretation:

- The staged VeriEQL batch CLI is importable and reaches argparse help under the external venv.
- This confirms the dependency gap that previously blocked help display is resolved for non-experiment probing.
- This does not prove any SQL verification pair succeeds. No pair file was passed and no verifier experiment was run.
