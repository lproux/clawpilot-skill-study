# Success Rubric: SPA Triage Friday

**Workflow:** WF-07 | **Mode:** Automation | **Actor:** CSA

## Expected Output

Per-SPA disposition (accept/decline/escalate) with rationale, proposed opportunities for accepted SPAs

## Routing Requirements

- **Entry skill:** acr-signal-to-opportunity-coach
- **Modules:** spa-recommendation-triage, signal-to-opportunity
- **Conditional handoffs:**
  - pipeline-msx-hygiene-coach (when: accepted SPA creates opportunity needing MSX write)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
