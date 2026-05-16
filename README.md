# ClawPilot SMB Skills Scientific Workflow Study

## Project Charter

**Goal:** Design a master orchestrator prompt for ClawPilot's seven aggregated SMB coaching skills, validated through a 14,006-scenario campaign that produces (1) a defensible best-of-class orchestrator and (2) an evidence-grounded skill-redesign report.

**Why this matters:** ClawPilot's orchestrator decides which of seven aggregated coaching skills to invoke when a CSA, DSSP, or Manager asks for help. Today there is no master prompt -- the orchestrator is greenfield. The right master prompt determines whether the product saves users hours of cross-tool research or wastes their time with misrouted outputs. The study is designed to answer not just "does the orchestrator work" but "where does the underlying skill design itself need to evolve."

**Owner:** LP -- Azure Cloud Architect, building ClawPilot.

**Target orchestrator model:** Claude Opus 4.7 with extended reasoning, 256k or 1M context.

**Statistical foundation:** 14,006 scenarios stratified across 52 workflows with floor-of-150 + frequency-weighted top-up + adversarial + golden-set anchors. Statistical power at n=150 produces a 95% CI half-width of approximately +/-8pp on proportions near 0.5.

## The Seven Aggregated Skills

| Skill | Primary Role | Default Posture |
|---|---|---|
| acr-signal-to-opportunity-coach | CSA primary, DSSP handoff | Read; hypotheses only |
| customer-meeting-prep-outreach-coach | CSA + DSSP | Draft-only, no send |
| forecast-business-review-coach | CSA, DSSP, Manager | Read-only by default |
| funding-partner-activation-coach | CSA + DSSP | Read; no commercial writeback in V1 |
| pipeline-msx-hygiene-coach | CSA + DSSP | The ONLY writeback owner (with explicit approval) |
| portfolio-account-planning-coach | CSA primary, DSSP secondary | Read; routes to siblings |
| solution-value-design-coach | CSA primary, DSSP value framing | Read |

## Study Phases

- **Phase 1:** Methodology design, workflow contracts, failure-mode catalogs (complete)
- **Phase 2:** Repo initialization, scenario schema, fixtures, generation prompt, full corpus generation
- **Phase 3:** Adversarial expansion, golden-set anchors, corpus lockdown
- **Phase 4:** Execution harness (Azure-native)
- **Phase 5:** v0 baseline campaign
- **Phase 6:** Judge protocol (multi-axis LLM-as-judge)
- **Phase 7:** Failure-mode clustering and analysis
- **Phase 8:** Master prompt iteration (v0 -> v1 -> v2)
- **Phase 9:** Full-corpus regression and statistical significance
- **Phase 10:** Gap report and V2 skill recommendations

## Repository Structure

```
clawpilot-skill-study/
  /docs/          - Methodology, taxonomy, scoring rubrics
  /workflows/     - 52 workflow contracts with failure-mode catalogs
  /personas/      - CSA, DSSP, Manager persona definitions
  /perturbations/ - Perturbation library for scenario variance
  /fixtures/      - 50 synthetic MSX account fixtures
  /scenarios/     - 14,006 scenario corpus
  /schemas/       - JSON Schema definitions
  /scripts/       - Generation, validation, reporting scripts
  /tests/         - Test suite
```

## Statistical References

- Cochran, W. G. (1977). Sampling Techniques, 3rd ed. Wiley. (Neyman allocation)
- Liang et al. (2022). Holistic Evaluation of Language Models (HELM).
- Srivastava et al. (2022). Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models (BIG-bench).
- Zheng et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS.
- Dubois et al. (2024). AlpacaEval 2.0: Length-Controlled AlpacaEval.
- Min et al. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision. EMNLP.
