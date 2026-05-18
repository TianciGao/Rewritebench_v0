# Wave 003 Policy or Manual Questions

No new policy approval is required for the recommended wave 003 queue if the task migrates only `wave_003_policy_approved_candidate` rows and reuses the wave 002 policy record.

Manual questions that remain outside wave 003:

- Should `manual_review_required` rows with otherwise complete core assets, such as CONS_0003, CONS_0004, PERF_0005, PERF_0046, PERF_0048, and LONGTAIL_0002, be separately approved for package creation with explicit caveats?
- Should orphan or unregistered rows be added to a registry-governance queue before package standardization?
- Should rows with missing checker assets be blocked until checker templates are reconstructed, or may they be packaged as incomplete backlog assets with explicit `needs_checker_review` caveats?
- Should PORT rows with multiple negative SQL files require a separate hard-negative policy review before standardization?

For wave 003 itself, proceed under existing wave 002 policies and fail closed per case.
