# Normalized Status-Only Metrics Dry-Run v4 Report

## Purpose And Scope

This is an audit-only dry run over the combined candidate status overlay v2.
It includes sanitized SQLGlot projection inputs where parser v1 produced row-level non-timing status fields.

## Inputs

- Combined candidate status overlay v2
- Combined metric-input authorization overlay v1
- Status inference overlay v0 for previously authorized inferred_generated rows
- Track-A same-engine denominator scaffold

## Summary

- Combined filled rows: 312
- Combined unresolved rows: 288
- SQLGlot rows filled: 137
- SQLGlot rows unresolved: 103
- Dry-run input rows: 312

## Boundary Confirmation

- Official metrics computed: false
- Paper tables rendered: false
- Timing metrics computed: false
- Reports/results changed: false
- Denominator changed: false

## Next Safe Action

Review SQLGlot projection/parser coverage and decide whether to authorize additional sanitized non-timing SQLGlot sources or keep SQLGlot partial coverage explicit.
