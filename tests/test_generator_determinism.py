"""Tests for scenario generator determinism.

Same seed + same inputs must produce identical scenario output.
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from generate_scenarios import (
    generate_single_scenario,
    load_all_fixtures,
    load_failure_mode_catalog,
    load_workflow_contract,
)


@pytest.fixture(scope="module")
def fixtures():
    return load_all_fixtures()


@pytest.fixture(scope="module")
def wf01_contract():
    return load_workflow_contract("WF-01")


@pytest.fixture(scope="module")
def wf01_fms():
    _, fms = load_failure_mode_catalog("WF-01")
    return fms


class TestGeneratorDeterminism:
    def test_same_seed_produces_identical_output(self, fixtures, wf01_contract, wf01_fms):
        """Running the generator twice with the same seed must produce byte-identical output."""
        fm = wf01_fms[0]  # First adherence FM
        fixture = fixtures[0]

        result1 = generate_single_scenario(
            workflow_id="WF-01",
            intent="adherence",
            targeted_fm=fm,
            persona="CSA",
            fixture=fixture,
            seed=12345,
            sequence_num=1,
            contract=wf01_contract,
        )

        result2 = generate_single_scenario(
            workflow_id="WF-01",
            intent="adherence",
            targeted_fm=fm,
            persona="CSA",
            fixture=fixture,
            seed=12345,
            sequence_num=1,
            contract=wf01_contract,
        )

        # Compare as sorted-key JSON for determinism
        json1 = json.dumps(result1, sort_keys=True)
        json2 = json.dumps(result2, sort_keys=True)
        assert json1 == json2

    def test_different_seeds_produce_different_output(self, fixtures, wf01_contract, wf01_fms):
        """Different seeds must produce different scenarios for the same inputs."""
        fm = wf01_fms[0]
        fixture = fixtures[0]

        result1 = generate_single_scenario(
            workflow_id="WF-01",
            intent="adherence",
            targeted_fm=fm,
            persona="CSA",
            fixture=fixture,
            seed=12345,
            sequence_num=1,
            contract=wf01_contract,
        )

        result2 = generate_single_scenario(
            workflow_id="WF-01",
            intent="adherence",
            targeted_fm=fm,
            persona="CSA",
            fixture=fixture,
            seed=99999,
            sequence_num=2,
            contract=wf01_contract,
        )

        # At minimum user_message should differ
        assert result1["user_message"] != result2["user_message"] or result1["perturbations"] != result2["perturbations"]

    def test_seed_is_recorded_in_output(self, fixtures, wf01_contract, wf01_fms):
        """The seed used for generation must be recorded in the scenario JSON."""
        fm = wf01_fms[0]
        fixture = fixtures[0]

        result = generate_single_scenario(
            workflow_id="WF-01",
            intent="adherence",
            targeted_fm=fm,
            persona="CSA",
            fixture=fixture,
            seed=54321,
            sequence_num=1,
            contract=wf01_contract,
        )

        assert result["seed"] == 54321

    def test_canonical_json_serialization(self, fixtures, wf01_contract, wf01_fms):
        """Output JSON must use sorted keys and consistent formatting for hash stability."""
        fm = wf01_fms[0]
        fixture = fixtures[0]

        result = generate_single_scenario(
            workflow_id="WF-01",
            intent="adherence",
            targeted_fm=fm,
            persona="CSA",
            fixture=fixture,
            seed=11111,
            sequence_num=1,
            contract=wf01_contract,
        )

        # Serializing twice with sort_keys must produce identical bytes
        json_bytes1 = json.dumps(result, sort_keys=True, indent=2).encode()
        json_bytes2 = json.dumps(result, sort_keys=True, indent=2).encode()
        assert json_bytes1 == json_bytes2

        # Verify it's valid JSON
        parsed = json.loads(json_bytes1)
        assert parsed["scenario_id"] == "WF-01-00001"
