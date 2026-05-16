# Failure Mode Catalog: Gap-to-Target Diagnostic

**Workflow:** WF-27 | **Tier:** 3 | **N:** 217

**Total failure modes:** 13

## Adherence Failure Modes

- **FM-WF27-A** (adherence): Reports gap without decomposition
- **FM-WF27-B** (adherence): Invents target value when source is missing
- **FM-WF27-C** (adherence): Confuses coverage gap with conversion gap
- **FM-WF27-D** (adherence): Recovery options without probability estimates
- **FM-WF27-E** (adherence): Proposes recovery requiring resources not signaled available
- **FM-WF27-F** (adherence): Over-weights recent month vs cumulative pattern
- **FM-WF27-G** (adherence): Fails to handoff to ACR when consumption is the driver
- **FM-WF27-H** (adherence): Exposes IC-level performance in a CSA-scoped diagnostic
- **FM-WF27-I** (adherence): Skips comparable-period delta entirely
- **FM-WF27-J** (adherence): Claims 'on track' when masking a category gap

## Assumption-Stress Failure Modes

- **FM-WF27-K** (assumption-stress): Strict read-only posture even when stating a forecast comment would have been more useful
- **FM-WF27-L** (assumption-stress): Deferring to pipeline-hygiene for record fixes when CSA could have triaged inline

## Design-Redesign Failure Modes

- **FM-WF27-M** (design-redesign): Separation of gap-to-target from portfolio-planning produces fragmented narrative

