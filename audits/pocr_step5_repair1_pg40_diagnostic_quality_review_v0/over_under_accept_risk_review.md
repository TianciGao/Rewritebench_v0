# Over/Under-Accept Risk Review

## 1. Signs of Over-Accept

Possible over-accept count: 0.

The review found no transformation-supported operation atom accepted without the D037-required pattern of `source_candidate_diff:changed` paired with candidate-specific, candidate-token, or positive-aligned span evidence. This suggests Stage B did not accept operation atoms based only on static span presence in this run.

## 2. Signs of Under-Accept

Possible under-accept / strict-span rejection count: 10.

These are operation atoms that Stage A marked `implemented` with both `source_candidate_diff:changed` and candidate/positive/token evidence, but Stage B still rejected as `presence_only` or `insufficient_transformation_evidence`. The likely cause is conservative span validation: the cited text did not prove candidate-specific or positive-aligned transformation under the current normalized text checks.

## 3. Failure Mode Classification

The 5 fail-closed rows are provider-output/runtime issues rather than case membership or candidate-root issues: 3 malformed JSON rows and 2 timeout rows. The malformed rows indicate provider JSON robustness / prompt formatting risk. The timeout rows indicate provider/runtime reliability risk. The 10 under-accept candidates indicate Stage B-policy or evidence-ref quoting sensitivity rather than official metric instability.

## 4. Improvements Before Next Baseline

Before another baseline, improve provider JSON robustness, add targeted retry for fail-closed malformed/timeout rows, tighten evidence_ref formatting, and add manual review hooks for transformation-supported and strict-span-rejected atoms. Do not promote these counts as official POCR.
