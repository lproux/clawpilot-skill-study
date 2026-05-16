# Success Rubric: Discovery Call Transcript -> Opportunity Build

**Workflow:** WF-43 | **Mode:** Co-Work | **Actor:** CSA/DSSP

## Expected Output

BANT signal extraction with evidence quotes, opportunity proposal with stage/value/close-date, confidence labels, solution sketch suggestion, follow-up actions

## Routing Requirements

- **Entry skill:** customer-meeting-prep-outreach-coach
- **Modules:** follow-up-and-decisions
- **Conditional handoffs:**
  - pipeline-msx-hygiene-coach (when: opportunity creation warranted)
  - solution-value-design-coach (when: solution sketch needed from discovery signals)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
