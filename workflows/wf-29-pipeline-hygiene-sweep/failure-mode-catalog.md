# Failure Mode Catalog: Pipeline Hygiene Sweep

**Workflow:** WF-29 | **Tier:** 3 | **N:** 317

**Total failure modes:** 16

## Adherence Failure Modes

- **FM-WF29-A** (adherence): Produces full pipeline list instead of delta digest
- **FM-WF29-B** (adherence): Includes 'At Risk' status as hygiene defect (classifier violation)
- **FM-WF29-C** (adherence): Writeback proposal without evidence_source
- **FM-WF29-D** (adherence): Writeback proposal mutates a field not derivable from evidence
- **FM-WF29-E** (adherence): Executes writeback without explicit user confirmation (critical guardrail)
- **FM-WF29-F** (adherence): Confuses BPF-stage staleness with milestone staleness
- **FM-WF29-G** (adherence): Fails to surface close-date-vs-stage inconsistency
- **FM-WF29-H** (adherence): Skips opportunities lacking required fields (silently drops)
- **FM-WF29-I** (adherence): Proposes fix in user's nighttime hours without flagging timezone
- **FM-WF29-J** (adherence): Produces opportunity hypothesis when hygiene was the request
- **FM-WF29-K** (adherence): Re-flags yesterday's still-open defects without acknowledging persistence

## Assumption-Stress Failure Modes

- **FM-WF29-L** (assumption-stress): Daily-Automation overhead exceeds the cleanup value for some accounts
- **FM-WF29-M** (assumption-stress): Requiring approval for low-stakes obvious fixes creates friction
- **FM-WF29-N** (assumption-stress): Strict hygiene-vs-status separation hides status risks caused by stale fields

## Design-Redesign Failure Modes

- **FM-WF29-O** (design-redesign): Pipeline-msx-hygiene as sole writeback owner forces awkward handoffs from meeting-prep and ACR
- **FM-WF29-P** (design-redesign): Delta digest format loses signal for accounts that need a full re-scan

