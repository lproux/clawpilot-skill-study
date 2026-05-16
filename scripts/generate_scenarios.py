"""Scenario generation entrypoint.

Usage:
    python scripts/generate_scenarios.py --workflow WF-XX --intent adherence --count N --seed-base S
    python scripts/generate_scenarios.py --campaign full

Generates scenario JSON files from the Jinja2 prompt template and workflow contracts.
"""
import argparse
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"
SCHEMAS_DIR = REPO_ROOT / "schemas"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
FIXTURES_DIR = REPO_ROOT / "fixtures"
TEMPLATE_PATH = Path(__file__).parent / "scenario_generation_prompt.j2"


def parse_args():
    parser = argparse.ArgumentParser(description="Generate evaluation scenarios")
    parser.add_argument("--workflow", type=str, help="Workflow ID (e.g., WF-01)")
    parser.add_argument("--intent", type=str, choices=["happy", "adherence", "assumption-stress", "design-redesign"])
    parser.add_argument("--count", type=int, default=10, help="Number of scenarios to generate")
    parser.add_argument("--seed-base", type=int, default=42, help="Base seed for reproducibility")
    parser.add_argument("--campaign", type=str, choices=["full"], help="Run full campaign generation")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scenarios")
    parser.add_argument("--parallelism", type=int, default=4, help="Max parallel generation calls")
    return parser.parse_args()


def load_workflow_contract(workflow_id: str) -> dict:
    """Load the contract.yaml for a given workflow ID."""
    wf_num = workflow_id.replace("WF-", "")
    wf_dirs = list(WORKFLOWS_DIR.glob(f"wf-{wf_num}-*"))
    if not wf_dirs:
        raise FileNotFoundError(f"No workflow directory found for {workflow_id}")
    import yaml
    with open(wf_dirs[0] / "contract.yaml") as f:
        return yaml.safe_load(f)


def load_failure_mode_catalog(workflow_id: str) -> str:
    """Load the failure-mode-catalog.md for a given workflow ID."""
    wf_num = workflow_id.replace("WF-", "")
    wf_dirs = list(WORKFLOWS_DIR.glob(f"wf-{wf_num}-*"))
    if not wf_dirs:
        raise FileNotFoundError(f"No workflow directory found for {workflow_id}")
    with open(wf_dirs[0] / "failure-mode-catalog.md") as f:
        return f.read()


def load_schema() -> dict:
    """Load the scenario schema for validation."""
    with open(SCHEMAS_DIR / "scenario.schema.json") as f:
        return json.load(f)


def validate_scenario(scenario: dict, schema: dict) -> list[str]:
    """Validate a scenario against the schema. Returns errors."""
    import jsonschema
    validator = jsonschema.Draft202012Validator(schema)
    return [f"{e.json_path}: {e.message}" for e in validator.iter_errors(scenario)]


def generate_single_scenario(
    workflow_id: str,
    intent: str,
    targeted_fm: str | None,
    persona: str,
    fixture_id: str,
    perturbations: list[str],
    seed: int,
) -> dict:
    """Generate a single scenario. Stub -- will use Jinja2 template + LLM in Deliverable 2.3."""
    raise NotImplementedError(
        "Scenario generation requires the Jinja2 prompt template and LLM call. "
        "This will be implemented in Deliverable 2.3."
    )


def main():
    args = parse_args()

    if args.campaign == "full":
        logger.info("Full campaign mode -- generating all 14,006 scenarios")
        logger.info("This requires Deliverable 2.3 (prompt template) to be complete.")
        sys.exit(1)

    if not args.workflow:
        logger.error("--workflow is required when not running --campaign full")
        sys.exit(1)

    logger.info(f"Generating {args.count} scenarios for {args.workflow} intent={args.intent} seed_base={args.seed_base}")

    # Stub: actual generation logic implemented in Deliverable 2.3
    logger.info("Generation stub complete. Implement Deliverable 2.3 for actual generation.")


if __name__ == "__main__":
    main()
