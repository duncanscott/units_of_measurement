"""Validate every JSONL file against its JSON Schema.

Requires the ``jsonschema`` package::

    pip install jsonschema

Usage::

    python3 scripts/validate_schemas.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("jsonschema is required: pip install jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"
JSONL_DIR = ROOT / "jsonl"

# Map each JSONL file to its schema file.
# Files that share a schema are mapped to the same schema path.
SCHEMA_MAP: dict[str, str] = {
    "jsonl/units_of_measurement.jsonl": "schema/units_of_measurement.schema.json",
    "jsonl/units_with_ontologies.jsonl": "schema/units_of_measurement.schema.json",
    "jsonl/si_units.jsonl": "schema/si_units.schema.json",
    "jsonl/uom.jsonl": "schema/uom.schema.json",
    "jsonl/ontology_crosswalk_base_units.jsonl": "schema/ontology_crosswalk_base_units.schema.json",
    "jsonl/focused/si_base_units.jsonl": "schema/focused/si_base_units.schema.json",
    "jsonl/focused/biomedical_units.jsonl": "schema/focused/si_base_units.schema.json",
    "jsonl/focused/uo_units.jsonl": "schema/focused/uo_units.schema.json",
    "jsonl/focused/ucum_units.jsonl": "schema/focused/ucum_units.schema.json",
    "jsonl/focused/property_summary.jsonl": "schema/focused/property_summary.schema.json",
}


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def validate_file(jsonl_rel: str, schema_rel: str) -> list[str]:
    jsonl_path = ROOT / jsonl_rel
    schema_path = ROOT / schema_rel

    if not jsonl_path.exists():
        return [f"{jsonl_rel}: file not found"]
    if not schema_path.exists():
        return [f"{schema_rel}: schema not found"]

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    records = load_jsonl(jsonl_path)
    errors: list[str] = []
    for idx, record in enumerate(records, start=1):
        for error in validator.iter_errors(record):
            path = ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "(root)"
            errors.append(f"{jsonl_rel} line {idx}: {path}: {error.message}")
    return errors


def main() -> int:
    total_files = 0
    total_records = 0
    all_errors: list[str] = []

    for jsonl_rel, schema_rel in sorted(SCHEMA_MAP.items()):
        jsonl_path = ROOT / jsonl_rel
        if not jsonl_path.exists():
            all_errors.append(f"{jsonl_rel}: file not found")
            continue

        records = load_jsonl(jsonl_path)
        errors = validate_file(jsonl_rel, schema_rel)
        total_files += 1
        total_records += len(records)

        if errors:
            all_errors.extend(errors)
            print(f"  FAIL  {jsonl_rel} ({len(records)} records, {len(errors)} errors)")
        else:
            print(f"  OK    {jsonl_rel} ({len(records)} records)")

    print()
    if all_errors:
        print(f"Schema validation failed ({len(all_errors)} errors across {total_files} files):")
        for err in all_errors[:20]:
            print(f"  - {err}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more")
        return 1

    print(f"All {total_files} files validated ({total_records} total records).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
