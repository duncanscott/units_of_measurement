# Repository Guidelines

## Project Structure & Module Organization
Data lives in `json/`, which holds three newline-delimited JSON files: `units_of_measurement.jsonl` (preferred merged dataset), `si_units.jsonl` (SI plus prefix expansions), and `uom.jsonl` (records imported from the Rust uom crate). Root-level `README.md` documents schema fields, while `LICENSE` and `THIRD-PARTY-LICENSES` cover legal obligations. Keep new datasets in `json/` and mirror the existing filename pattern so downstream consumers can glob consistently.

## Build, Test, and Development Commands
No build step exists; validation focuses on data quality.

```sh
jq -c '.' json/units_of_measurement.jsonl > /dev/null   # stream-validate JSONL
jq '.[].unit' json/units_of_measurement.jsonl | head     # spot-check entries
python - <<'PY'
import json, sys
with open("json/units_of_measurement.jsonl") as f:
    seen=set()
    for i,line in enumerate(f,1):
        unit=json.loads(line)["unit"]
        if unit in seen: sys.exit(f"duplicate unit {unit} on line {i}")
        seen.add(unit)
PY
```

Adapt the Python snippet when adding additional invariants (e.g., allowed `system` values).

## Coding Style & Naming Conventions
Entries are single-line JSON objects sorted lexicographically by `unit`. Preserve the field order shown in `README.md` to reduce churn. Use US English spellings (`meter`, `liter`) unless an `alternate_unit` explicitly records the variant. Symbols stay lowercase unless internationally capitalized (e.g., `Pa`). New files should use LF line endings and UTF-8; escapes are required for non-ASCII characters.

## Testing Guidelines
Every contribution must re-run the validation commands above on all three JSONL files. When introducing new properties or systems, augment a lightweight verifier and capture it in the pull request description. Provide at least two sample conversions demonstrating the `conversion_factor` and `reference_unit` pair for tricky units (temperature, logarithmic measures) to help reviewers reason about correctness.

## Commit & Pull Request Guidelines
Follow the existing imperative, single-sentence commit style (e.g., `add Martian gravity units`). Each commit should bundle a logically complete dataset change plus regenerated documentation, if required. Pull requests need a checklist covering: summary of changes, mention of validation commands run, data source links, and any schema impacts. Include diffs or screenshots when comparing before/after rows to make review faster, and link related issues whenever possible.
