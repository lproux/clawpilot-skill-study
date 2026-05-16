"""Generate FM coverage report for the scenario corpus.

Verifies that every failure mode code has the minimum required scenario count:
- Adherence FMs: at least 3 scenarios
- Assumption-stress FMs: at least 2 scenarios
- Design-redesign FMs: at least 2 scenarios
"""
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"
WORKFLOWS_DIR = REPO_ROOT / "workflows"

# Minimum coverage per FM type
MIN_COVERAGE = {
    "A": 3,   # adherence
    "AS": 2,  # assumption-stress
    "DR": 2,  # design-redesign
}


def extract_fm_codes_from_catalog(catalog_path: Path) -> dict[str, str]:
    """Extract FM codes and their types from a failure-mode-catalog.md file."""
    fm_codes = {}
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
            fm_codes[match.group(1)] = current_type
    return fm_codes


def get_all_fm_codes() -> dict[str, str]:
    """Get all FM codes across all workflows with their types."""
    all_fms = {}
    for wf_dir in sorted(WORKFLOWS_DIR.glob("wf-*")):
        catalog_path = wf_dir / "failure-mode-catalog.md"
        if catalog_path.exists():
            fms = extract_fm_codes_from_catalog(catalog_path)
            all_fms.update(fms)
    return all_fms


def count_fm_coverage() -> dict[str, int]:
    """Count how many scenarios target each FM code."""
    fm_counts = {}
    for scenario_path in SCENARIOS_DIR.rglob("*.json"):
        if scenario_path.parent.name.startswith("_"):
            continue  # skip _validation, _adversarial, _golden for this count
        try:
            with open(scenario_path) as f:
                scenario = json.load(f)
            fm = scenario.get("targeted_failure_mode")
            if fm:
                fm_counts[fm] = fm_counts.get(fm, 0) + 1
        except (json.JSONDecodeError, KeyError):
            pass
    return fm_counts


def report():
    all_fms = get_all_fm_codes()
    fm_counts = count_fm_coverage()

    print("=" * 80)
    print("FAILURE MODE COVERAGE REPORT")
    print("=" * 80)
    print(f"\nTotal FM codes in catalog: {len(all_fms)}")
    print(f"FM codes with at least 1 scenario: {sum(1 for fm in all_fms if fm_counts.get(fm, 0) > 0)}")

    uncovered = []
    undercovered = []
    covered = []

    for fm_code, fm_type in sorted(all_fms.items()):
        count = fm_counts.get(fm_code, 0)
        min_required = MIN_COVERAGE.get(fm_type, 2)
        if count == 0:
            uncovered.append((fm_code, fm_type, min_required))
        elif count < min_required:
            undercovered.append((fm_code, fm_type, count, min_required))
        else:
            covered.append((fm_code, fm_type, count, min_required))

    if uncovered:
        print(f"\n--- UNCOVERED ({len(uncovered)} FM codes with 0 scenarios) ---")
        for fm_code, fm_type, min_req in uncovered:
            print(f"  {fm_code} ({fm_type}) -- needs at least {min_req}")

    if undercovered:
        print(f"\n--- UNDERCOVERED ({len(undercovered)} FM codes below minimum) ---")
        for fm_code, fm_type, count, min_req in undercovered:
            print(f"  {fm_code} ({fm_type}) -- has {count}, needs {min_req}")

    print(f"\n--- SUMMARY ---")
    print(f"  Fully covered:  {len(covered)}/{len(all_fms)}")
    print(f"  Undercovered:   {len(undercovered)}/{len(all_fms)}")
    print(f"  Uncovered:      {len(uncovered)}/{len(all_fms)}")

    coverage_pct = len(covered) / len(all_fms) * 100 if all_fms else 0
    print(f"  Coverage:       {coverage_pct:.1f}%")

    if uncovered or undercovered:
        print("\nEXIT GATE BLOCKED: not all FM codes have minimum coverage")
        sys.exit(1)
    else:
        print("\n100% FM coverage achieved.")


if __name__ == "__main__":
    report()
