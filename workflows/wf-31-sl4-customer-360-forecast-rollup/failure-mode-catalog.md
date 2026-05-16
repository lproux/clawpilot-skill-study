# Failure Mode Catalog: SL4 Customer 360 Forecast Roll-Up

**Workflow:** WF-31 | **Tier:** 3 | **N:** 217

**Total failure modes:** 13

## Adherence Failure Modes

- **FM-WF31-A** (adherence): Reports SL4 numbers without source attribution
- **FM-WF31-B** (adherence): Rolls up SL4 to L1 silently when SL4 data is sparse
- **FM-WF31-C** (adherence): Uses Kusto fallback without first attempting Customer 360
- **FM-WF31-D** (adherence): Fallback used silently -- user doesn't know which source the numbers came from
- **FM-WF31-E** (adherence): Confuses SL4 hierarchy levels (parent/child reversed)
- **FM-WF31-F** (adherence): Mismatches milestone-record SL4 alignment to consumption SL4
- **FM-WF31-G** (adherence): SL4 expansion pattern misread as anomaly
- **FM-WF31-H** (adherence): Invents SL4 nodes that don't exist in the hierarchy
- **FM-WF31-I** (adherence): Skips period boundary alignment between Customer 360 and Kusto
- **FM-WF31-J** (adherence): Fallback BI query joins on mismatched dimensions

## Assumption-Stress Failure Modes

- **FM-WF31-K** (assumption-stress): Rigid Customer-360-first policy fails when BI is known to have fresher data
- **FM-WF31-L** (assumption-stress): Reporting SL4 detail when a higher-level summary would be more useful

## Design-Redesign Failure Modes

- **FM-WF31-M** (design-redesign): No native SL4 module in the skill set forces awkward handoff into data-bi-analysis

