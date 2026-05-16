# Success Rubric: Customer Outage/Complaint Email -> Triage + Escalation

**Workflow:** WF-37 | **Mode:** Co-Work | **Actor:** CSA/DSSP

## Expected Output

Severity triage, root-cause hypothesis (labeled as hypothesis), customer response draft, ACR risk flag, escalation routing, prior-incident comparison

## Routing Requirements

- **Entry skill:** customer-meeting-prep-outreach-coach
- **Modules:** email-chat-context
- **Conditional handoffs:**
  - acr-signal-to-opportunity-coach (when: outage impacts major workload ACR)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
