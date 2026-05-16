# Methodology

Consolidated methodology for the ClawPilot SMB Skills Scientific Workflow Study.

## A. Project Charter

Design a master orchestrator prompt for ClawPilot's seven aggregated SMB coaching skills, validated through a 14,006-scenario campaign that produces (1) a defensible best-of-class orchestrator and (2) an evidence-grounded skill-redesign report.

The orchestrator decides which of seven aggregated coaching skills to invoke when a CSA, DSSP, or Manager asks for help. The study answers not just "does the orchestrator work" but "where does the underlying skill design itself need to evolve."

Target orchestrator model: Claude Opus 4.7 with extended reasoning, 256k or 1M context.

Statistical foundation: 14,006 scenarios stratified across 52 workflows with floor-of-150 + frequency-weighted top-up + adversarial + golden-set anchors. Statistical power at n=150 produces a 95% CI half-width of approximately +/-8pp on proportions near 0.5.

Justification: Neyman allocation (Cochran, Sampling Techniques, 3rd ed., Wiley 1977) and operational ML evaluation practice (HELM, Liang et al. 2022; BIG-bench, Srivastava et al. 2022). Multi-axis LLM-as-judge methodology follows MT-Bench (Zheng et al. 2023, NeurIPS), AlpacaEval 2.0 (Dubois et al. 2024), and FActScore for factuality grounding (Min et al. 2023, EMNLP).

## B. The Seven Aggregated Skills

| Skill | Modules | Role Fit | Default Posture |
|---|---|---|---|
| acr-signal-to-opportunity-coach | acr-data-access, acr-health-forecast, signal-to-opportunity, spa-recommendation-triage | CSA primary, DSSP handoff | Read; hypotheses only |
| customer-meeting-prep-outreach-coach | meeting-prep, follow-up-and-decisions, email-chat-context, contact-stakeholder-map, dark-customer-outreach | CSA + DSSP | Draft-only, no send |
| forecast-business-review-coach | committed-milestone-forecast, gap-to-target-review, business-review-narrative, team-coaching-risk-review | CSA, DSSP, Manager | Read-only by default |
| funding-partner-activation-coach | funding-eligibility, macc-consumption-plan, partner-evaluation, contract-billing-lookup | CSA + DSSP | Read; no commercial writeback in V1 |
| pipeline-msx-hygiene-coach | crm-msx-data-access, opportunity-milestone-hygiene, pipeline-review-digest, stage-close-readiness, writeback-approval-guardrails | CSA + DSSP | The ONLY writeback owner (with explicit approval) |
| portfolio-account-planning-coach | account-review, account-health-prioritization, whitespace-growth-hypotheses, manager-portfolio-review, daily-weekly-planning | CSA primary, DSSP secondary | Read; routes to siblings |
| solution-value-design-coach | migration-architecture, security-posture-value, competitive-positioning, data-bi-analysis, solution-research | CSA primary, DSSP value framing | Read |

Shared references: clawpilot-v1-access-adapters, data-safety-guardrails, forecast-business-rules, hygiene-vs-status-classifier, msx-d365-field-contract, msx-mcp-access, msx-mcp-adapter, msx-mcp-tool-policy, msx-permission-matrix, product-boundaries, routing-policy, writeback-approval-guardrails.

## C. Personas

Three personas with stated positions:

1. **CSA** -- Customer Success Account Manager, NA, ~3yr tenure, 40-60 accounts, consumption growth + renewal protection
2. **DSSP** -- Digital Sales Specialist Partner, NA, ~2yr tenure, overlay across CSAs, opportunity qualification + solution-value framing
3. **Manager** -- CSA/DSSP people manager, 8-12 directs, forecast accuracy + team coaching + risk rollup

## D. Composite Score (0-100)

Six axes: Output Usability (25%), Evidence Integrity (20%), Routing Accuracy (15%), Guardrail Adherence (15%), Decision Quality (15%), Efficiency (10%).

Pass: 70. Excellent: 85.

Scoring varies by intent:
- Adherence: standard 6-axis
- Assumption-stress: guardrail axis neutral
- Design-redesign: partial composite (usability/decision/efficiency only) + verdicts on routing/evidence/guardrail

## E. Scenario Schema

JSON Schema Draft 2020-12. See /schemas/scenario.schema.json for authoritative definition.

Key fields: scenario_id (WF-XX-NNNNN), workflow_id, workflow_name, seed, tier, intent, targeted_failure_mode, persona, fixture_id, user_message, input_artifacts, perturbations, expected_routing, expected_output_shape, success_rubric, guardrail_checks, judge_instructions.

## F. Perturbation Library

Categories: persona, data-state, input-shape (email), input-shape (transcript), ambiguity, failure-injection, format. Each scenario applies 0-4 perturbations. See /perturbations/library.yaml for full catalog.

## G. Allocation

Total: 14,006 scenarios.
- 12,006 workflow-bound (52 workflows, floor-of-150, frequency-weighted top-up)
- 1,500 adversarial / cross-workflow
- 500 golden-set regression anchors

Within each workflow:
- 40% happy-path
- 35% adherence-failure
- 15% assumption-stress
- 10% design-redesign

Coverage rule: every FM code has at least 3 adherence scenarios, 2 assumption-stress scenarios, and 2 design-redesign scenarios targeting it.

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-05-15 | Initial methodology document created from Phase 1 packet | Phase 2 Deliverable 2.0 |
