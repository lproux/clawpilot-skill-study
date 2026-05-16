# Failure Mode Catalog: CxObserve Signal-to-Opportunity Conversion

**Workflow:** WF-08 | **Tier:** 3 | **N:** 250

**Total failure modes:** 13

## Adherence Failure Modes

- **FM-WF08-A** (adherence): Treats every signal as an opportunity
- **FM-WF08-B** (adherence): Skips confidence labeling
- **FM-WF08-C** (adherence): Writes to MSX without approval
- **FM-WF08-D** (adherence): Ignores CxObserve metadata (recency, source, signal type)
- **FM-WF08-E** (adherence): Over-claims revenue impact
- **FM-WF08-F** (adherence): Skips deduplication against existing opportunities
- **FM-WF08-G** (adherence): Misclassifies signal type (renewal vs expansion vs risk)
- **FM-WF08-H** (adherence): Hypothesis lacks value-lever framing
- **FM-WF08-I** (adherence): No suggested next action
- **FM-WF08-J** (adherence): Confidence stated without rationale

## Assumption-Stress Failure Modes

- **FM-WF08-K** (assumption-stress): CxObserve-signal-only filter misses correlated signals from other sources
- **FM-WF08-L** (assumption-stress): Hypothesis must include value-lever even when signal is purely diagnostic

## Design-Redesign Failure Modes

- **FM-WF08-M** (design-redesign): Signal-to-opportunity should natively pull from multiple signal sources

