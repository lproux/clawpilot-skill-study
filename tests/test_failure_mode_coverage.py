"""Tests for failure mode coverage across the scenario corpus."""
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"
WORKFLOWS_DIR = REPO_ROOT / "workflows"

MIN_ADHERENCE = 3
MIN_ASSUMPTION_STRESS = 2
MIN_DESIGN_REDESIGN = 2


def get_all_fm_codes() -> dict[str, str]:
    """Extract all FM codes from failure-mode-catalog.md files with their types."""
    all_fms = {}
    for wf_dir in sorted(WORKFLOWS_DIR.glob("wf-*")):
        catalog_path = wf_dir / "failure-mode-catalog.md"
        if not catalog_path.exists():
            continue
        content = catalog_path.read_text()
        current_type = None
        for line in content.split("\n"):
            if "## Adherence" in line:
                current_type = "A"
            elif "## Assumption-Stress" in line:
                current_type = "AS"
            elif "## Design-Redesign" in line:
                current_type = "DR"
            match = re.search(r"\*\*(FM-WF\d{2}-[A-Z]+)\*\*", line)
            if match and current_type:
                all_fms[match.group(1)] = current_type
    return all_fms


def count_fm_scenarios() -> dict[str, int]:
    """Count scenarios targeting each FM code."""
    fm_counts = {}
    for scenario_path in SCENARIOS_DIR.rglob("*.json"):
        if scenario_path.parent.name.startswith("_"):
            continue
        try:
            with open(scenario_path) as f:
                scenario = json.load(f)
            fm = scenario.get("targeted_failure_mode")
            if fm:
                fm_counts[fm] = fm_counts.get(fm, 0) + 1
        except (json.JSONDecodeError, KeyError):
            pass
    return fm_counts


class TestFailureModeCoverage:
    def test_all_fm_codes_exist_in_catalogs(self):
        """Every workflow must have a failure-mode-catalog.md with at least one FM code."""
        for wf_dir in sorted(WORKFLOWS_DIR.glob("wf-*")):
            catalog = wf_dir / "failure-mode-catalog.md"
            assert catalog.exists(), f"Missing failure-mode-catalog.md in {wf_dir.name}"
            content = catalog.read_text()
            fm_codes = re.findall(r"FM-WF\d{2}-[A-Z]+", content)
            assert len(fm_codes) > 0, f"No FM codes found in {wf_dir.name}/failure-mode-catalog.md"

    def test_fm_code_format_consistency(self):
        """All FM codes must follow the pattern FM-WFXX-[A-Z]+."""
        all_fms = get_all_fm_codes()
        for fm_code in all_fms:
            assert re.match(r"^FM-WF\d{2}-[A-Z]+$", fm_code), f"Invalid FM code format: {fm_code}"

    def test_adherence_fm_minimum_coverage(self):
        """Every adherence FM must have at least 3 targeting scenarios."""
        all_fms = get_all_fm_codes()
        fm_counts = count_fm_scenarios()

        if not fm_counts:
            pytest.skip("No scenarios generated yet (Deliverable 2.4)")

        adherence_fms = {code for code, typ in all_fms.items() if typ == "A"}
        undercovered = []
        for fm in sorted(adherence_fms):
            count = fm_counts.get(fm, 0)
            if count < MIN_ADHERENCE:
                undercovered.append(f"{fm}: {count} < {MIN_ADHERENCE}")

        assert not undercovered, (
            f"Adherence FM codes below minimum ({MIN_ADHERENCE}):\n" + "\n".join(undercovered)
        )

    def test_assumption_stress_fm_minimum_coverage(self):
        """Every assumption-stress FM must have at least 2 targeting scenarios."""
        all_fms = get_all_fm_codes()
        fm_counts = count_fm_scenarios()

        if not fm_counts:
            pytest.skip("No scenarios generated yet")

        stress_fms = {code for code, typ in all_fms.items() if typ == "AS"}
        undercovered = []
        for fm in sorted(stress_fms):
            count = fm_counts.get(fm, 0)
            if count < MIN_ASSUMPTION_STRESS:
                undercovered.append(f"{fm}: {count} < {MIN_ASSUMPTION_STRESS}")

        assert not undercovered, (
            f"Assumption-stress FM codes below minimum ({MIN_ASSUMPTION_STRESS}):\n" + "\n".join(undercovered)
        )

    def test_design_redesign_fm_minimum_coverage(self):
        """Every design-redesign FM must have at least 2 targeting scenarios."""
        all_fms = get_all_fm_codes()
        fm_counts = count_fm_scenarios()

        if not fm_counts:
            pytest.skip("No scenarios generated yet")

        dr_fms = {code for code, typ in all_fms.items() if typ == "DR"}
        undercovered = []
        for fm in sorted(dr_fms):
            count = fm_counts.get(fm, 0)
            if count < MIN_DESIGN_REDESIGN:
                undercovered.append(f"{fm}: {count} < {MIN_DESIGN_REDESIGN}")

        assert not undercovered, (
            f"Design-redesign FM codes below minimum ({MIN_DESIGN_REDESIGN}):\n" + "\n".join(undercovered)
        )

    def test_no_orphan_fm_codes_in_scenarios(self):
        """Every FM code referenced in a scenario must exist in the catalog."""
        all_fms = get_all_fm_codes()
        fm_counts = count_fm_scenarios()

        if not fm_counts:
            pytest.skip("No scenarios generated yet")

        orphans = set(fm_counts.keys()) - set(all_fms.keys())
        assert not orphans, f"FM codes in scenarios not in catalog: {orphans}"
