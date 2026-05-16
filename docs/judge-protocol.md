# Judge Protocol

This document defines the LLM-as-judge methodology for the ClawPilot SMB Skills Scientific Workflow Study. Full implementation occurs in Phase 6; this is the design contract.

## Architecture

Each axis gets its own judge call. Six calls per scenario. Separation eliminates inter-axis halo bias (Zheng et al. 2023).

## Per-Axis Judge Type

| Axis | Primary Judge | Structural Check |
|---|---|---|
| Output Usability | LLM rubric (5 anchored examples) | None |
| Evidence Integrity | LLM rubric + structural | FActScore-style atomic factuality |
| Routing Accuracy | Deterministic | Compare observed vs expected entry_skill and modules |
| Guardrail Adherence | LLM rubric + structural | Predicate battery from guardrail_checks list |
| Decision Quality | LLM rubric (5 anchored examples) | None |
| Efficiency | Deterministic | Turns, tokens, tool calls vs tier expectations |

## Bias Mitigations

- **Position bias:** Anchored examples shuffled across batches; ordering recorded
- **Verbosity bias:** Explicit "do not reward length" instruction; AlpacaEval 2.0 length-controlled adjustment as post-hoc check
- **Self-enhancement bias:** Judge evaluates against scenario-specific rubric anchors, not abstract quality; 5% human calibration validates
- **Drift across batches:** Rotating calibration scenarios with known scores; batch rejected if drift exceeds 1 axis-point

## Human Calibration

- 5% of scenarios (~700) scored by human raters in parallel
- Two raters per scenario; third for disagreements over 1 axis-point
- Krippendorff's alpha computed per axis
- Alpha < 0.6: axis scoring rejected, rubric revised
- Alpha 0.6-0.8: scores reported with bias correction
- Alpha > 0.8: scores used as-is

## Scoring Mode Variants

Three prompt variants per axis:
- `standard` -- used for happy and adherence scenarios
- `guardrail-neutral` -- used for assumption-stress scenarios (guardrail axis neutral)
- `verdict-on-structural` -- used for design-redesign scenarios (routing/evidence/guardrail produce verdicts)

## References

- Zheng et al. 2023, NeurIPS (LLM-as-judge, position bias)
- Dubois et al. 2024 (length-controlled scoring)
- Min et al. 2023, EMNLP (atomic factuality)
- Krippendorff 2018 (inter-rater agreement)
