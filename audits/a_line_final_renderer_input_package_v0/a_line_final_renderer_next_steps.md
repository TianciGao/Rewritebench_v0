# A-line Final Renderer Next Steps

## Handoff State

A-line v0 is ready to hand off to B-line after this package.

This package gives future renderer work a stable metric-state manifest with official limited metrics, blocked metrics, an N.A. record, audit-only support, post-release backlog records, denominator caveats, and no-global-leaderboard requirements.

## Renderer Boundary

A future renderer task may consume this package only with separate authorization. It must not render paper tables, write `reports/` or `results/`, compute metrics, or change denominators unless those actions are explicitly approved.

Reports/results outputs remain unauthorized.

Timing and performance work remains outside A-line v0 and should be handled as post-A-line or separate future work.

## B-line Candidate Tasks

- `b_line_reproduction_report_renderer_design_v0`: define renderer inputs, output boundaries, validation gates, and caveat handling without rendering tables.
- `b_line_dev_only_reproduce_smoke_v0`: design or run a dev-only retained-evidence smoke path if separately authorized.
- `b_line_user_runner_output_policy_implementation_v0`: implement public runner output policy after renderer and reproduction boundaries are stable.

## Later C-line Work

C-line non-Common-core case expansion remains later. It should not begin until B-line reproduction and public-output boundaries are clear.

## Exact Next Safe Action

Run `b_line_reproduction_report_renderer_design_v0` to design the reproduction/report renderer boundary and validation gates without rendering paper tables, writing `reports/` or `results/`, computing metrics, or changing denominators.
