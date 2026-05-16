# PORT_0008 Canonical Migration Notes

This note records the canonical-layout full case migration pilot for `PORT_0008`.

## Scope

- One-case copy-first migration for `PORT_0008` only.
- Canonical layout was generated from the approved planning blueprint.
- Existing formal sanitized Spark plan evidence was reused.
- Raw Spark plan text files were not copied into public retained evidence.
- Raw `runs/` was not copied wholesale.
- Legacy files remain unchanged and mapped.

## Validation Assets

The scripts in `validation/` are copied legacy validation assets. They were not executed during this migration, are not yet canonical user runners, and future public runner output must not write to case-local `runs/` by default.

## Claim Boundary

This migration did not run DB engines, did not regenerate evidence, did not change denominator membership, did not change paper results, did not change Common-core membership, did not change case admission status, and creates no leaderboard.
