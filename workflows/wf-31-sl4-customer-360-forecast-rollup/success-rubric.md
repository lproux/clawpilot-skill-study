# Success Rubric: SL4 Customer 360 Forecast Roll-Up

**Workflow:** WF-31 | **Mode:** Co-Work | **Actor:** CSA/DSSP/Manager

## Expected Output

SL4-level forecast rollup with source attribution, hierarchy alignment, period boundary reconciliation

## Routing Requirements

- **Entry skill:** forecast-business-review-coach
- **Modules:** committed-milestone-forecast
- **Conditional handoffs:**
  - solution-value-design-coach (when: Customer 360 unavailable, Kusto BI fallback needed)

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
