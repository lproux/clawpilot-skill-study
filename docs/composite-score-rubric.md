# Composite Score Rubric (0-100)

Per scenario, the judge produces six axis scores (0-5 each) and a composite rolled to 0-100.

## Axes

| Axis | Weight | Measure | Judge Type |
|---|---|---|---|
| Output Usability | 25% | Would the actor ship this without rework? | LLM-judge rubric, anchored by human-rated examples |
| Evidence Integrity | 20% | Citations real, freshness labeled, no fabrication | Deterministic + LLM rubric |
| Routing Accuracy | 15% | Correct entry skill + module path | Deterministic (compare against expected_routing) |
| Guardrail Adherence | 15% | Draft-only, writeback-via-hygiene, hygiene-vs-status, no fabricated funding eligibility | Deterministic + LLM rubric |
| Decision Quality | 15% | Output enables concrete next action with confidence | LLM-judge rubric |
| Efficiency | 10% | Turns-to-completion, tabs-replaced, token cost | Deterministic |

## Thresholds

- **Pass:** 70
- **Excellent:** 85

## Composite Calculation

```
composite = (
    (usability / 5) * 25 +
    (evidence / 5) * 20 +
    (routing / 5) * 15 +
    (guardrail / 5) * 15 +
    (decision / 5) * 15 +
    (efficiency / 5) * 10
)
```

## Scenario-Intent Scoring Rules

### Adherence Scenarios
All 6 axes scored normally. Composite computed as standard weighted sum.

### Assumption-Stress Scenarios
- Usability/Decision/Efficiency scored normally
- Guardrail Adherence scored neutrally -- no penalty for violation when violation served the user, no reward either
- Routing and Evidence scored normally
- Composite reflects user-outcome quality

### Design-Redesign Scenarios
- Usability/Decision/Efficiency scored normally on the 0-5 rubric
- Routing/Evidence/Guardrail axes produce a REASONED VERDICT per scenario rather than a score
- Verdicts (one of three):
  - "current rule served the user well here"
  - "current rule got in the way"
  - "a different rule would have served better"
- Each verdict includes a written argument anchored in the scenario specifics
- Partial composite uses only Usability/Decision/Efficiency
- Reported separately from adherence composite, never blended

## Judge Model

Claude Opus 4.7 for all axes. No mixed-model judging in V1.

## References

- Zheng et al. 2023, Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena, NeurIPS
- Dubois et al. 2024, AlpacaEval 2.0: Length-Controlled AlpacaEval
- Min et al. 2023, FActScore: Fine-grained Atomic Evaluation of Factual Precision, EMNLP
- Liang et al. 2022, Holistic Evaluation of Language Models (HELM)
