# Failure Mode Catalog: Customer Renewal Email -> Forecast Impact + Path

**Workflow:** WF-35 | **Tier:** 4 | **N:** 217

**Total failure modes:** 14

## Adherence Failure Modes

- **FM-WF35-A** (adherence): Assumes contract state without lookup
- **FM-WF35-B** (adherence): No freshness label on contract data
- **FM-WF35-C** (adherence): Forecast impact stated without confidence
- **FM-WF35-D** (adherence): Funding eligibility asserted as approved
- **FM-WF35-E** (adherence): MACC plan proposed without consumption signal
- **FM-WF35-F** (adherence): Draft response commits commercial terms
- **FM-WF35-G** (adherence): Skips ACR trajectory check
- **FM-WF35-H** (adherence): Invents renewal date when not in source
- **FM-WF35-I** (adherence): Confuses CSP vs MCA renewal mechanics
- **FM-WF35-J** (adherence): Proposes MACC expansion when contraction signal is present

## Assumption-Stress Failure Modes

- **FM-WF35-K** (assumption-stress): Strict read-only on contract data when staging an obvious update would help
- **FM-WF35-L** (assumption-stress): Funding-eligibility-likely caveat creates over-hedging in low-risk cases

## Design-Redesign Failure Modes

- **FM-WF35-M** (design-redesign): Separation of renewal handling across 4 skills means CSA gets fragmented narrative
- **FM-WF35-N** (design-redesign): No native 'renewal motion' workflow in skill set -- current design synthesizes

