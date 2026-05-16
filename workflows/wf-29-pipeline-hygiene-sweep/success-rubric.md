# Success Rubric: Pipeline Hygiene Sweep

**Workflow:** WF-29 | **Mode:** Automation (daily) | **Actor:** CSA/DSSP

## Expected Output

Delta digest of hygiene defects (not status issues), writeback proposals with evidence_source per field, approval queue

## Routing Requirements

- **Entry skill:** pipeline-msx-hygiene-coach
- **Modules:** opportunity-milestone-hygiene, pipeline-review-digest, writeback-approval-guardrails

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
