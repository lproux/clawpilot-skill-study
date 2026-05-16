"""Tests for scenario distribution against the allocation table."""
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"

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

TOTAL_WORKFLOW_BOUND = 12006
TOTAL_ADVERSARIAL = 1500
TOTAL_GOLDEN = 500
GRAND_TOTAL = 14006


class TestDistribution:
    def _count_workflow_scenarios(self):
        counts = {}
        for wf_num in range(1, 53):
            wf_dir = SCENARIOS_DIR / f"wf-{wf_num:02d}"
            if wf_dir.exists():
                counts[f"WF-{wf_num:02d}"] = len(list(wf_dir.glob("*.json")))
            else:
                counts[f"WF-{wf_num:02d}"] = 0
        return counts

    def test_per_workflow_within_5_percent(self):
        """Each workflow's scenario count must be within +/-5% of target."""
        counts = self._count_workflow_scenarios()
        total = sum(counts.values())
        if total == 0:
            pytest.skip("No scenarios generated yet (Deliverable 2.4)")

        violations = []
        for wf_id, target in ALLOCATION.items():
            actual = counts.get(wf_id, 0)
            if abs(actual - target) > target * 0.05:
                violations.append(f"{wf_id}: actual={actual}, target={target}")

        assert not violations, f"Distribution violations:\n" + "\n".join(violations)

    def test_grand_total(self):
        """Grand total must be exactly 14,006."""
        counts = self._count_workflow_scenarios()
        workflow_total = sum(counts.values())
        adversarial_dir = SCENARIOS_DIR / "_adversarial"
        golden_dir = SCENARIOS_DIR / "_golden"
        adversarial = len(list(adversarial_dir.glob("*.json"))) if adversarial_dir.exists() else 0
        golden = len(list(golden_dir.glob("*.json"))) if golden_dir.exists() else 0
        grand_total = workflow_total + adversarial + golden

        if grand_total == 0:
            pytest.skip("No scenarios generated yet")
        assert grand_total == GRAND_TOTAL, f"Grand total {grand_total} != {GRAND_TOTAL}"

    def test_intent_distribution_per_workflow(self):
        """Within each workflow, intent distribution should match targets within +/-2pp."""
        counts = self._count_workflow_scenarios()
        if sum(counts.values()) == 0:
            pytest.skip("No scenarios generated yet")

        intent_targets = {"happy": 0.40, "adherence": 0.35, "assumption-stress": 0.15, "design-redesign": 0.10}
        violations = []

        for wf_num in range(1, 53):
            wf_dir = SCENARIOS_DIR / f"wf-{wf_num:02d}"
            if not wf_dir.exists():
                continue
            scenarios = list(wf_dir.glob("*.json"))
            if not scenarios:
                continue
            total = len(scenarios)
            intent_counts = {"happy": 0, "adherence": 0, "assumption-stress": 0, "design-redesign": 0}
            for s_path in scenarios:
                with open(s_path) as f:
                    s = json.load(f)
                intent = s.get("intent", "")
                if intent in intent_counts:
                    intent_counts[intent] += 1

            for intent, target_pct in intent_targets.items():
                actual_pct = intent_counts[intent] / total
                if abs(actual_pct - target_pct) > 0.02:
                    violations.append(
                        f"WF-{wf_num:02d} {intent}: {actual_pct:.2f} vs target {target_pct:.2f}"
                    )

        assert not violations, f"Intent distribution violations:\n" + "\n".join(violations)
