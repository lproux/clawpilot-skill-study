# Success Rubric: CST / Billing Lookup

**Workflow:** WF-24 | **Mode:** Prompt | **Actor:** CSA/DSSP

## Expected Output

Contract summary with freshness labels, subscription type, renewal date, MACC state if applicable, billing frequency

## Routing Requirements

- **Entry skill:** funding-partner-activation-coach
- **Modules:** contract-billing-lookup

## Quality Gates

- Output must be actionable (named owners, specific next steps)
- Evidence must be cited with freshness labels
- No fabricated data points
- Routing must match contract unless scenario is design-redesign intent
- Guardrails respected (draft-only, no unauthorized writeback)
