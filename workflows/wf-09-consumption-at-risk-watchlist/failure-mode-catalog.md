# Failure Mode Catalog: Consumption-at-Risk Watchlist

**Workflow:** WF-09 | **Tier:** 3 | **N:** 317

**Total failure modes:** 14

## Adherence Failure Modes

- **FM-WF09-A** (adherence): Repeats yesterday's watchlist without delta indicator
- **FM-WF09-B** (adherence): Projects risk without confidence
- **FM-WF09-C** (adherence): Over-flags seasonal variation as risk
- **FM-WF09-D** (adherence): Skips contract-event check
- **FM-WF09-E** (adherence): Lists accounts without driver
- **FM-WF09-F** (adherence): Exceeds 15 accounts (loses prioritization)
- **FM-WF09-G** (adherence): Misses accounts that newly entered risk window
- **FM-WF09-H** (adherence): Ignores recovery actions already in flight
- **FM-WF09-I** (adherence): Confuses risk severity bands
- **FM-WF09-J** (adherence): No owner assigned per at-risk account

## Assumption-Stress Failure Modes

- **FM-WF09-K** (assumption-stress): Daily cadence wastes value for stable accounts
- **FM-WF09-L** (assumption-stress): 15-account cap suppresses tail risk

## Design-Redesign Failure Modes

- **FM-WF09-M** (design-redesign): Consumption-at-risk and pipeline-at-risk should be unified primitive
- **FM-WF09-N** (design-redesign): Watchlist format doesn't natively support shared-owner accounts

