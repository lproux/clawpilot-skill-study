"""Validate fixture JSON files against the fixture schema."""
import json
import sys
from pathlib import Path

import jsonschema


def load_schema() -> dict:
    schema_path = Path(__file__).parent.parent / "schemas" / "fixture.schema.json"
    with open(schema_path) as f:
        return json.load(f)


def validate_fixture(fixture_path: Path, schema: dict) -> list[str]:
    """Validate a single fixture file. Returns list of error messages (empty if valid)."""
    errors = []
    try:
        with open(fixture_path) as f:
            fixture = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    validator = jsonschema.Draft202012Validator(schema)
    for error in validator.iter_errors(fixture):
        errors.append(f"{error.json_path}: {error.message}")

    return errors


def report_distribution(fixture_dir: Path) -> dict:
    """Report fixture class distribution."""
    distribution = {"clean": 0, "stale": 0, "missing": 0, "inconsistent": 0, "contradictory": 0}
    for path in sorted(fixture_dir.glob("fx-*.json")):
        try:
            with open(path) as f:
                fixture = json.load(f)
            fixture_class = fixture.get("fixture_class", "unknown")
            if fixture_class in distribution:
                distribution[fixture_class] += 1
        except (json.JSONDecodeError, KeyError):
            pass
    return distribution


def main():
    schema = load_schema()
    fixture_dir = Path(__file__).parent.parent / "fixtures"

    if len(sys.argv) > 1:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        paths = sorted(fixture_dir.glob("fx-*.json"))

    if not paths:
        print("No fixture files found.")
        sys.exit(0)

    total = 0
    failed = 0
    for path in paths:
        total += 1
        errors = validate_fixture(path, schema)
        if errors:
            failed += 1
            print(f"FAIL: {path.name}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"PASS: {path.name}")

    print(f"\n--- Results: {total - failed}/{total} passed ---")

    distribution = report_distribution(fixture_dir)
    print(f"\n--- Distribution ---")
    for cls, count in distribution.items():
        print(f"  {cls}: {count}")

    expected = {"clean": 10, "stale": 15, "missing": 10, "inconsistent": 10, "contradictory": 5}
    print(f"\n--- Expected vs Actual ---")
    for cls in expected:
        status = "OK" if distribution[cls] == expected[cls] else "MISMATCH"
        print(f"  {cls}: expected={expected[cls]}, actual={distribution[cls]} [{status}]")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
