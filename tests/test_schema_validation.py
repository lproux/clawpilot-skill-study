"""Tests for schema validation of scenarios and fixtures."""
import json
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"


@pytest.fixture
def scenario_schema():
    with open(SCHEMAS_DIR / "scenario.schema.json") as f:
        return json.load(f)


@pytest.fixture
def fixture_schema():
    with open(SCHEMAS_DIR / "fixture.schema.json") as f:
        return json.load(f)


@pytest.fixture
def write_proposal_schema():
    with open(SCHEMAS_DIR / "write-proposal.schema.json") as f:
        return json.load(f)


class TestScenarioSchema:
    def test_schema_is_valid_json_schema(self, scenario_schema):
        """The scenario schema itself must be a valid JSON Schema Draft 2020-12 document."""
        validator = jsonschema.Draft202012Validator
        validator.check_schema(scenario_schema)

    def test_schema_requires_mandatory_fields(self, scenario_schema):
        """All required fields must be declared in the schema."""
        required = scenario_schema["required"]
        assert "scenario_id" in required
        assert "workflow_id" in required
        assert "workflow_name" in required
        assert "seed" in required
        assert "tier" in required
        assert "intent" in required
        assert "persona" in required
        assert "fixture_id" in required
        assert "user_message" in required
        assert "expected_routing" in required
        assert "expected_output_shape" in required
        assert "success_rubric" in required
        assert "judge_instructions" in required

    def test_scenario_id_pattern(self, scenario_schema):
        """scenario_id must match WF-XX-NNNNN pattern."""
        pattern = scenario_schema["properties"]["scenario_id"]["pattern"]
        assert pattern == "^WF-[0-9]{2}-[0-9]{5}$"

    def test_intent_enum_values(self, scenario_schema):
        """Intent must be one of the four valid types."""
        enum = scenario_schema["properties"]["intent"]["enum"]
        assert set(enum) == {"happy", "adherence", "assumption-stress", "design-redesign"}

    def test_persona_enum_values(self, scenario_schema):
        """Persona must be CSA, DSSP, or Manager."""
        enum = scenario_schema["properties"]["persona"]["enum"]
        assert set(enum) == {"CSA", "DSSP", "Manager"}

    def test_tier_enum_values(self, scenario_schema):
        """Tier must be 1, 2, 3, or 4."""
        enum = scenario_schema["properties"]["tier"]["enum"]
        assert set(enum) == {1, 2, 3, 4}


class TestFixtureSchema:
    def test_schema_is_valid_json_schema(self, fixture_schema):
        """The fixture schema itself must be a valid JSON Schema Draft 2020-12 document."""
        validator = jsonschema.Draft202012Validator
        validator.check_schema(fixture_schema)

    def test_schema_requires_mandatory_fields(self, fixture_schema):
        """All required fields must be declared in the schema."""
        required = fixture_schema["required"]
        assert "fixture_id" in required
        assert "fixture_class" in required
        assert "account" in required
        assert "opportunities" in required
        assert "contacts" in required
        assert "acr_trend" in required

    def test_fixture_class_enum(self, fixture_schema):
        """fixture_class must be one of the five valid types."""
        enum = fixture_schema["properties"]["fixture_class"]["enum"]
        assert set(enum) == {"clean", "stale", "missing", "inconsistent", "contradictory"}


class TestWriteProposalSchema:
    def test_schema_is_valid_json_schema(self, write_proposal_schema):
        validator = jsonschema.Draft202012Validator
        validator.check_schema(write_proposal_schema)

    def test_must_require_approval_is_const_true(self, write_proposal_schema):
        """must_require_approval must always be true."""
        prop = write_proposal_schema["properties"]["must_require_approval"]
        assert prop["const"] is True


class TestValidationScenarios:
    """Tests that run against hand-crafted validation scenarios (Deliverable 2.1)."""

    def test_validation_scenarios_exist_and_are_valid(self, scenario_schema):
        """All scenarios in _validation/ must be schema-valid."""
        validation_dir = REPO_ROOT / "scenarios" / "_validation"
        if not validation_dir.exists():
            pytest.skip("No validation scenarios yet (Deliverable 2.1)")
        scenarios = list(validation_dir.glob("*.json"))
        if not scenarios:
            pytest.skip("No validation scenarios yet")
        validator = jsonschema.Draft202012Validator(scenario_schema)
        for path in scenarios:
            with open(path) as f:
                scenario = json.load(f)
            errors = list(validator.iter_errors(scenario))
            assert not errors, f"{path.name}: {[e.message for e in errors]}"
