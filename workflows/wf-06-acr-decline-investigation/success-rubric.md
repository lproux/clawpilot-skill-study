# Success Rubric: ACR Decline Investigation

**Workflow:** WF-06 | **Mode:** Co-Work | **Actor:** CSA

## Expected Output

Ranked hypotheses for decline with evidence, recovery actions with owners, timeline, confidence labels

## Routing Requirements

- **Entry skill:** acr-signal-to-opportunity-coach
- **Modules:** acr-data-access, acr-health-forecast, signal-to-opportunity
- **Conditional handoffs:**
  - funding-partner-activation-coach (when: contract/billing is the driver)
  - pipeline-msx-hygiene-coach (when: opportunity records need updating)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
