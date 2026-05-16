# Success Rubric: Cross-Sell Trigger Email

**Workflow:** WF-42 | **Mode:** Co-Work | **Actor:** CSA/DSSP

## Expected Output

Signal assessment, opportunity hypothesis with confidence, ownership routing, response draft, next-step sequence with timing

## Routing Requirements

- **Entry skill:** customer-meeting-prep-outreach-coach
- **Modules:** email-chat-context
- **Conditional handoffs:**
  - acr-signal-to-opportunity-coach (when: cross-sell signal warrants opportunity assessment)
  - pipeline-msx-hygiene-coach (when: opportunity creation warranted)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
