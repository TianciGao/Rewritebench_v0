# Protected Path Review

Protected paths reviewed:

- `cases/`
- case-local `skills.md`
- `output/`
- top-level `reports/`
- top-level `results/`
- case-local `runs/`
- `runs/user` candidate roots

Expected result:

- No case packages modified.
- No `skills.md` files modified.
- No candidate SQL files modified.
- No `runs/user` files modified.
- No top-level `reports/` or `results/` files modified.
- Local `output/` remains untracked and uncommitted.

Validation notes:

- `git diff --name-only -- cases output reports results runs/user` returned no tracked modifications.
- `git diff --name-only -- ':(glob)runs/user/**/candidate_sql/**'` returned no tracked modifications.
- `git status --short -- cases ':(glob)cases/**/skills.md' output reports results runs/user` showed the pre-existing untracked `output/` directory only.
- No files were found under the planned Step 5 annotation output path or replay `/tmp` path after the interrupted attempt.
- Final command validation records concrete git status and diff output.
