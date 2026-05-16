"""Validate scenario JSON files against the scenario schema."""
import json
import sys
from pathlib import Path

import jsonschema


def load_schema() -> dict:
    schema_path = Path(__file__).parent.parent / "schemas" / "scenario.schema.json"
    with open(schema_path) as f:
        return json.load(f)


def validate_scenario(scenario_path: Path, schema: dict) -> list[str]:
    """Validate a single scenario file. Returns list of error messages (empty if valid)."""
    errors = []
    try:
        with open(scenario_path) as f:
            scenario = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    validator = jsonschema.Draft202012Validator(schema)
    for error in validator.iter_errors(scenario):
        errors.append(f"{error.json_path}: {error.message}")

    return errors


def main():
    schema = load_schema()
    scenario_dir = Path(__file__).parent.parent / "scenarios"

    if len(sys.argv) > 1:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        paths = list(scenario_dir.rglob("*.json"))

    if not paths:
        print("No scenario files found.")
        sys.exit(0)

    total = 0
    failed = 0
    for path in paths:
        total += 1
        errors = validate_scenario(path, schema)
        if errors:
            failed += 1
            print(f"FAIL: {path}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"PASS: {path}")

    print(f"\n--- Results: {total - failed}/{total} passed ---")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
