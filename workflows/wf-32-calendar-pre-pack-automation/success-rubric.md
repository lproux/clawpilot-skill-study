# Success Rubric: Calendar Pre-Pack Automation

**Workflow:** WF-32 | **Mode:** Automation | **Actor:** CSA/DSSP

## Expected Output

Pre-pack brief with attendee context, account snapshot, talking points, likely objections, open items, time-since-last-contact, meeting classification

## Routing Requirements

- **Entry skill:** customer-meeting-prep-outreach-coach
- **Modules:** meeting-prep, contact-stakeholder-map, email-chat-context
- **Conditional handoffs:**
  - portfolio-account-planning-coach (when: meeting is for account CSA should have declined)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
