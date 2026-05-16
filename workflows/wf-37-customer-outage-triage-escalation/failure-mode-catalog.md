# Failure Mode Catalog: Customer Outage/Complaint Email -> Triage + Escalation

**Workflow:** WF-37 | **Tier:** 4 | **N:** 217

**Total failure modes:** 13

## Adherence Failure Modes

- **FM-WF37-A** (adherence): Presents root-cause inference as confirmed
- **FM-WF37-B** (adherence): Over-escalates a routine service complaint
- **FM-WF37-C** (adherence): Under-routes a serious outage
- **FM-WF37-D** (adherence): Customer draft admits fault prematurely
- **FM-WF37-E** (adherence): No ACR risk flag when outage is on a major workload
- **FM-WF37-F** (adherence): Skips prior-similar-incident check
- **FM-WF37-G** (adherence): Confuses support-ticket scope with CSA scope
- **FM-WF37-H** (adherence): Recommends commitments outside CSA authority
- **FM-WF37-I** (adherence): Invents customer impact numbers not in source
- **FM-WF37-J** (adherence): Confuses planned maintenance with unplanned outage

## Assumption-Stress Failure Modes

- **FM-WF37-K** (assumption-stress): Strict read-only when fast MSX risk-flag update would matter

## Design-Redesign Failure Modes

- **FM-WF37-L** (design-redesign): No native support-handoff routing in the skill set
- **FM-WF37-M** (design-redesign): Outage-handling distributed across email-chat-context and ACR signals -- no first-class workflow primitive

