# JSON Schemas

[JSON Schema](https://json-schema.org/) (draft 2020-12) definitions for every JSONL dataset in this repository.

## Schema Files

| Schema | Validates |
|--------|-----------|
| `units_of_measurement.schema.json` | `jsonl/units_of_measurement.jsonl` and `jsonl/units_with_ontologies.jsonl` |
| `si_units.schema.json` | `jsonl/si_units.jsonl` |
| `uom.schema.json` | `jsonl/uom.jsonl` |
| `ontology_crosswalk_base_units.schema.json` | `jsonl/ontology_crosswalk_base_units.jsonl` |
| `focused/si_base_units.schema.json` | `jsonl/focused/si_base_units.jsonl` and `jsonl/focused/biomedical_units.jsonl` |
| `focused/uo_units.schema.json` | `jsonl/focused/uo_units.jsonl` |
| `focused/ucum_units.schema.json` | `jsonl/focused/ucum_units.jsonl` |
| `focused/property_summary.schema.json` | `jsonl/focused/property_summary.jsonl` |

### Shared Schemas

- **`units_of_measurement.schema.json`** covers both `units_of_measurement.jsonl` (the canonical dataset) and `units_with_ontologies.jsonl` (the intermediate annotated copy). They share the same field structure.
- **`focused/si_base_units.schema.json`** covers both `si_base_units.jsonl` and `biomedical_units.jsonl`. Both contain units with ontology cross-references using the same fields (`unit`, `property`, `symbol`, `system`, `external_ids`, `ontology_metadata`).

## Validation

```sh
pip install jsonschema
python3 scripts/validate_schemas.py
```

The script validates every record in each JSONL file against its corresponding schema and reports errors with line numbers.
