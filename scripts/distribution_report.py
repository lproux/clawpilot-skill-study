"""Generate distribution report for the scenario corpus.

Reports per-workflow scenario counts and compares against the allocation table.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"

# Allocation table from Phase 1 packet Section G
ALLOCATION = {
    "WF-01": 317, "WF-02": 250, "WF-03": 217, "WF-04": 167, "WF-05": 217,
    "WF-06": 250, "WF-07": 217, "WF-08": 250, "WF-09": 317, "WF-10": 217,
    "WF-11": 317, "WF-12": 317, "WF-13": 217, "WF-14": 250, "WF-15": 183,
    "WF-16": 317, "WF-17": 217, "WF-18": 217, "WF-19": 183, "WF-20": 183,
    "WF-21": 183, "WF-22": 167, "WF-23": 217, "WF-24": 250, "WF-25": 250,
    "WF-26": 183, "WF-27": 217, "WF-28": 183, "WF-29": 317, "WF-30": 250,
    "WF-31": 217, "WF-32": 317, "WF-33": 317, "WF-34": 250, "WF-35": 217,
    "WF-36": 183, "WF-37": 217, "WF-38": 217, "WF-39": 250, "WF-40": 250,
    "WF-41": 217, "WF-42": 217, "WF-43": 250, "WF-44": 217, "WF-45": 217,
    "WF-46": 183, "WF-47": 250, "WF-48": 217, "WF-49": 183, "WF-50": 183,
    "WF-51": 183, "WF-52": 217,
}

INTENT_TARGETS = {
    "happy": 0.40,
    "adherence": 0.35,
    "assumption-stress": 0.15,
    "design-redesign": 0.10,
}


def count_scenarios() -> dict:
    """Count scenarios per workflow and per intent."""
    counts = {}
    intent_counts = {}
    for wf_dir in sorted(SCENARIOS_DIR.glob("wf-*")):
        wf_num = wf_dir.name.replace("wf-", "")
        wf_id = f"WF-{wf_num}"
        scenarios = list(wf_dir.glob("*.json"))
        counts[wf_id] = len(scenarios)
        intent_counts[wf_id] = {"happy": 0, "adherence": 0, "assumption-stress": 0, "design-redesign": 0}
        for s_path in scenarios:
            try:
                with open(s_path) as f:
                    s = json.load(f)
                intent = s.get("intent", "unknown")
                if intent in intent_counts[wf_id]:
                    intent_counts[wf_id][intent] += 1
            except (json.JSONDecodeError, KeyError):
                pass
    return counts, intent_counts


def report():
    counts, intent_counts = count_scenarios()

    adversarial = len(list((SCENARIOS_DIR / "_adversarial").glob("*.json"))) if (SCENARIOS_DIR / "_adversarial").exists() else 0
    golden = len(list((SCENARIOS_DIR / "_golden").glob("*.json"))) if (SCENARIOS_DIR / "_golden").exists() else 0

    workflow_total = sum(counts.values())
    grand_total = workflow_total + adversarial + golden

    print("=" * 80)
    print("DISTRIBUTION REPORT")
    print("=" * 80)
    print(f"\nWorkflow-bound: {workflow_total} (target: 12,006)")
    print(f"Adversarial:    {adversarial} (target: 1,500)")
    print(f"Golden-set:     {golden} (target: 500)")
    print(f"Grand total:    {grand_total} (target: 14,006)")

    print(f"\n{'WF':<8} {'Actual':<8} {'Target':<8} {'Delta':<8} {'Pct':<8} {'Status'}")
    print("-" * 50)
    violations = 0
    for wf_id in sorted(ALLOCATION.keys()):
        actual = counts.get(wf_id, 0)
        target = ALLOCATION[wf_id]
        delta = actual - target
        pct = (actual / target * 100) if target > 0 else 0
        within = abs(delta) <= target * 0.05
        status = "OK" if within else "VIOLATION"
        if not within:
            violations += 1
        print(f"{wf_id:<8} {actual:<8} {target:<8} {delta:<+8} {pct:<7.1f}% {status}")

    print(f"\n--- Intent Distribution per Workflow ---")
    for wf_id in sorted(intent_counts.keys()):
        total = counts.get(wf_id, 0)
        if total == 0:
            continue
        ic = intent_counts[wf_id]
        print(f"\n{wf_id} (N={total}):")
        for intent, target_pct in INTENT_TARGETS.items():
            actual_pct = ic[intent] / total if total > 0 else 0
            status = "OK" if abs(actual_pct - target_pct) <= 0.02 else "CHECK"
            print(f"  {intent:<20} {ic[intent]:>4} ({actual_pct:.1%}) target={target_pct:.0%} [{status}]")

    print(f"\n--- Summary ---")
    print(f"Workflow violations (>5% off target): {violations}")
    if violations > 0:
        print("EXIT GATE BLOCKED: distribution violations detected")
        sys.exit(1)
    else:
        print("Distribution within tolerance.")


if __name__ == "__main__":
    report()
