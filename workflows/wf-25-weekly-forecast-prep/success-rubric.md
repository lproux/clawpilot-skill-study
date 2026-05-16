# Success Rubric: Weekly Forecast Prep

**Workflow:** WF-25 | **Mode:** Automation | **Actor:** CSA/DSSP

## Expected Output

Forecast summary with week-over-week delta, per-opportunity category assessment, gap analysis, uncommitted-upside identification, ask section

## Routing Requirements

- **Entry skill:** forecast-business-review-coach
- **Modules:** committed-milestone-forecast, gap-to-target-review
- **Conditional handoffs:**
  - pipeline-msx-hygiene-coach (when: hygiene issues discovered during forecast prep)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
