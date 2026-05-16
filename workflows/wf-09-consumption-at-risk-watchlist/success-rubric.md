# Success Rubric: Consumption-at-Risk Watchlist

**Workflow:** WF-09 | **Mode:** Automation | **Actor:** CSA

## Expected Output

Prioritized watchlist (max 15 accounts) with risk driver, confidence, recovery actions, delta from yesterday, owner per account

## Routing Requirements

- **Entry skill:** acr-signal-to-opportunity-coach
- **Modules:** acr-data-access, acr-health-forecast
- **Conditional handoffs:**
  - pipeline-msx-hygiene-coach (when: at-risk account has stale records)
  - customer-meeting-prep-outreach-coach (when: outreach needed for at-risk account)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
