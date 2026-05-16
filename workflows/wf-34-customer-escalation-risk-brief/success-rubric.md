# Success Rubric: Customer Escalation Email -> Risk Brief + Manager Loop

**Workflow:** WF-34 | **Mode:** Co-Work | **Actor:** CSA/DSSP

## Expected Output

Severity assessment, manager risk brief, customer-facing draft response, stakeholder map delta, forecast/risk impact, next-step sequence with stop conditions

## Routing Requirements

- **Entry skill:** customer-meeting-prep-outreach-coach
- **Modules:** email-chat-context, follow-up-and-decisions, contact-stakeholder-map
- **Conditional handoffs:**
  - forecast-business-review-coach (when: escalation warrants forecast/risk update)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
