"""Generate focused JSONL subsets for quick reference."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "jsonl" / "units_of_measurement.jsonl"
FOCUSED_DIR = ROOT / "jsonl" / "focused"

SI_BASE_UNITS = {
    "length": {"meter"},
    "mass": {"kilogram"},
    "time": {"second"},
    "electric current": {"ampere"},
    "thermodynamic temperature": {"kelvin"},
    "temperature interval": {"kelvin"},
    "amount of substance": {"mole"},
    "luminous intensity": {"candela"},
}


def load_records() -> List[dict]:
    return [
        json.loads(line)
        for line in DATA_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, records: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(rec, ensure_ascii=False) for rec in records) + "\n", encoding="utf-8")


def build_si_base_units(records: List[dict]) -> List[dict]:
    keep = []
    for record in records:
        property_name = record.get("property")
        unit_name = record.get("unit")
        if property_name in SI_BASE_UNITS and unit_name in SI_BASE_UNITS[property_name]:
            keep.append({
                "unit": unit_name,
                "property": property_name,
                "symbol": record.get("symbol"),
                "system": record.get("system"),
                "external_ids": record.get("external_ids"),
                "ontology_metadata": record.get("ontology_metadata"),
            })
    return keep


def build_property_summary(records: List[dict]) -> List[dict]:
    summary: Dict[str, dict] = {}
    for record in records:
        prop = record.get("property")
        data = summary.setdefault(
            prop,
            {
                "property": prop,
                "count": 0,
                "systems": set(),
                "reference_units": set(),
                "has_external_ids": 0,
            },
        )
        data["count"] += 1
        if record.get("system"):
            data["systems"].add(record["system"])
        if record.get("reference_unit"):
            data["reference_units"].add(record["reference_unit"])
        if record.get("external_ids"):
            data["has_external_ids"] += 1
    output = []
    for prop, data in sorted(summary.items(), key=lambda item: item[0]):
        output.append(
            {
                "property": prop,
                "count": data["count"],
                "systems": sorted(data["systems"]),
                "reference_units": sorted(data["reference_units"]),
                "annotated_records": data["has_external_ids"],
            }
        )
    return output


def main() -> None:
    records = load_records()
    si_base = build_si_base_units(records)
    property_summary = build_property_summary(records)
    write_jsonl(FOCUSED_DIR / "si_base_units.jsonl", si_base)
    write_jsonl(FOCUSED_DIR / "property_summary.jsonl", property_summary)
    print(
        f"Wrote {len(si_base)} SI base units and {len(property_summary)} property summaries to {FOCUSED_DIR}"
    )


if __name__ == "__main__":
    main()
