# Success Rubric: Monday Morning Portfolio Triage

**Workflow:** WF-01 | **Mode:** Automation | **Actor:** CSA

## Expected Output

Top 5-10 accounts ranked by urgency x impact, reason per account, named next action with owner, time-block plan for the week, populated handoff queue

## Routing Requirements

- **Entry skill:** portfolio-account-planning-coach
- **Modules:** daily-weekly-planning, account-health-prioritization
- **Conditional handoffs:**
  - customer-meeting-prep-outreach-coach (when: customer meetings exist this week)
  - pipeline-msx-hygiene-coach (when: stale records detected)
  - acr-signal-to-opportunity-coach (when: ACR signals match top accounts)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
