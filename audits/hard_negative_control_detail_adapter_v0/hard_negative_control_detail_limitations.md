# hard_negative_control_detail_adapter_v0 Limitations

- This adapter only indexes release case-package hard-negative metadata and evidence pointers.
- It does not rerun hard-negative validation.
- It does not compute false-accept rate.
- It does not parse legacy retained evidence.
- It does not prove semantic equivalence.
- It does not create official `results/retained` or `reports/evaluation` outputs.
- Future metrics and reporting require separate authorization.
