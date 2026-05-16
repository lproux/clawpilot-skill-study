"""Tests for scenario generator determinism.

Same seed + same inputs must produce identical scenario output.
"""
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent


class TestGeneratorDeterminism:
    def test_same_seed_produces_identical_output(self):
        """Running the generator twice with the same seed must produce byte-identical output."""
        # This test will be implemented when the generator (Deliverable 2.3) is complete.
        # It will:
        # 1. Generate a scenario with seed=12345, workflow=WF-01, intent=happy
        # 2. Generate the same scenario again with identical parameters
        # 3. Assert the two outputs are identical JSON (sorted keys, deterministic)
        pytest.skip("Generator not yet implemented (Deliverable 2.3)")

    def test_different_seeds_produce_different_output(self):
        """Different seeds must produce different scenarios for the same inputs."""
        pytest.skip("Generator not yet implemented (Deliverable 2.3)")

    def test_seed_is_recorded_in_output(self):
        """The seed used for generation must be recorded in the scenario JSON."""
        pytest.skip("Generator not yet implemented (Deliverable 2.3)")

    def test_canonical_json_serialization(self):
        """Output JSON must use sorted keys and consistent formatting for hash stability."""
        pytest.skip("Generator not yet implemented (Deliverable 2.3)")
