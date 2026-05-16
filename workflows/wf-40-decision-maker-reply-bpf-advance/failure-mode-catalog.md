# Failure Mode Catalog: Decision-Maker Reply -> BPF Advance Check

**Workflow:** WF-40 | **Tier:** 4 | **N:** 250

**Total failure modes:** 15

## Adherence Failure Modes

- **FM-WF40-A** (adherence): Over-reads commitment (treats general enthusiasm as scope)
- **FM-WF40-B** (adherence): Advances BPF without satisfying exit criteria
- **FM-WF40-C** (adherence): Milestone proposal mutates fields not derivable from email
- **FM-WF40-D** (adherence): Forecast category proposed without milestone evidence
- **FM-WF40-E** (adherence): Writeback executed without approval (critical)
- **FM-WF40-F** (adherence): Skips authority check (is sender the actual decision-maker)
- **FM-WF40-G** (adherence): Acknowledgment draft over-commits MS deliverables
- **FM-WF40-H** (adherence): Confuses verbal commitment with budget approval
- **FM-WF40-I** (adherence): Ignores conditional clauses ('yes, if X happens')
- **FM-WF40-J** (adherence): Misreads cultural register (polite 'yes' vs binding 'yes')
- **FM-WF40-K** (adherence): Proposes forecast change when commitment doesn't yet justify it

## Assumption-Stress Failure Modes

- **FM-WF40-L** (assumption-stress): Requiring approval for an obvious milestone update derived from the email creates friction
- **FM-WF40-M** (assumption-stress): Separation of BPF check from forecast update creates timing gap

## Design-Redesign Failure Modes

- **FM-WF40-N** (design-redesign): No native 'commitment-to-milestone' workflow primitive
- **FM-WF40-O** (design-redesign): Decision-email triggers across BPF/forecast/milestone -- no unified writeback proposal

