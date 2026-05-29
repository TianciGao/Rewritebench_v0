# Validation

Validation commands for this packet:

| check | result |
| --- | --- |
| audit CSV parse | passed |
| audit JSON parse | passed |
| Markdown non-empty check | passed |
| `git diff --check` | passed |
| changed-file secret scan | passed |
| staged-file secret scan | passed |
| protected staged path check | passed |
| `git status -sb` review | passed; two unrelated pre-existing untracked audit dirs remain untouched |
