# Success Rubric: Multi-Thread Customer Conversation Synthesis

**Workflow:** WF-39 | **Mode:** Co-Work | **Actor:** CSA/DSSP

## Expected Output

Consolidated decision log, cross-thread commitment inventory, action list with thread attribution, MSX update proposals, superseded-commitment identification

## Routing Requirements

- **Entry skill:** customer-meeting-prep-outreach-coach
- **Modules:** email-chat-context, follow-up-and-decisions
- **Conditional handoffs:**
  - pipeline-msx-hygiene-coach (when: MSX updates warranted from synthesis)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
