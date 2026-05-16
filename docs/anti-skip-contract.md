# Anti-Skip Contract

This document is the binding anti-skip contract for the ClawPilot SMB Skills Scientific Workflow Study. It governs all phase deliverables.

## Terms

1. When asked to generate 14,006 scenarios, you produce 14,006 scenario files. Not 100 with "extrapolate the rest." Not 500 with "this establishes the pattern." Fourteen thousand and six discrete files.

2. When asked to author 50 fixtures, you produce 50 files. Not 5 with "duplicate with variation."

3. When asked to validate distribution against the allocation table, you produce the actual count per workflow and per intent, not a sampled estimate.

4. You do not propose to the user that they "do the rest manually" or "run the generator in batches yourself." You run the generator. You produce the output. That is the job.

5. You do not skip failure modes. Every FM code in the catalog must have at least one targeted scenario generated against it. Coverage is verifiable and will be verified.

6. You do not produce structurally-valid but semantically-thin scenarios. Each scenario must reflect the specific failure mode it targets, the specific persona attributes, the specific perturbation vector, and the specific fixture state. Generic scenarios are detectable and unacceptable.

7. When you hit an actual technical limit (rate limits, context limits, API errors), you surface it explicitly and pause, you do not silently degrade output quality to fit the limit.

8. You produce progress reports at every batch checkpoint (defined below). The reports include counts, validation results, and any skipped items with explicit reasons.

9. If you find yourself reasoning "the user will probably be fine if I just do X% of this," that reasoning is the signal to do 100% instead.

10. You follow the system-prompt user preferences in effect for LP: full code when asked, no emoji in code, conservative on "final" claims, citations where research is invoked, 60% of effort focused on issue resolution and quality control.

## Enforcement

If at any point a deliverable is about to be produced that is incomplete, abbreviated, or sampled rather than full, STOP and surface the constraint that is forcing the reduction. Do not silently ship a reduced output.
