# Failure Mode Catalog: Calendar Pre-Pack Automation

**Workflow:** WF-32 | **Tier:** 4 | **N:** 317

**Total failure modes:** 20

## Adherence Failure Modes

- **FM-WF32-A** (adherence): Classifies internal-only meeting as customer meeting
- **FM-WF32-B** (adherence): Misses customer meeting because attendee is on a non-customer email domain
- **FM-WF32-C** (adherence): Includes raw email/chat content rather than summary
- **FM-WF32-D** (adherence): Invents attendee role when context is absent
- **FM-WF32-E** (adherence): Pre-pack identical to last week's for a recurring meeting
- **FM-WF32-F** (adherence): Skips prior transcript when one exists for the series
- **FM-WF32-G** (adherence): Generic talking points unattached to this meeting's specifics
- **FM-WF32-H** (adherence): Likely-objections section invents objections not signaled
- **FM-WF32-I** (adherence): Exposes private internal-strategy notes in pre-pack the CSA might forward
- **FM-WF32-J** (adherence): Fails to surface time-since-last-contact for cold attendees
- **FM-WF32-K** (adherence): Over-includes context for a routine recurring meeting
- **FM-WF32-L** (adherence): ACR signal mentioned when meeting is not commercial-themed
- **FM-WF32-M** (adherence): Pre-pack arrives <30 min before meeting (timing failure)
- **FM-WF32-N** (adherence): Includes attendees not on the meeting invite
- **FM-WF32-O** (adherence): Confuses meeting series instance with new meeting

## Assumption-Stress Failure Modes

- **FM-WF32-P** (assumption-stress): Rigid 1-page constraint hurts an exec briefing that needed depth
- **FM-WF32-Q** (assumption-stress): Daily-Automation generating pre-packs for every meeting creates noise vs filtering to high-value-only
- **FM-WF32-R** (assumption-stress): Non-Microsoft attendee as the sole filter misses partner-led meetings with valuable customer context

## Design-Redesign Failure Modes

- **FM-WF32-S** (design-redesign): Separation of pre-pack from portfolio-planning means CSA gets pre-packs for meetings they should have declined
- **FM-WF32-T** (design-redesign): Calendar trigger should learn from CSA dismissals -- current design doesn't

