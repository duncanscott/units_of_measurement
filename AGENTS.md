# Repository Guidelines

## Project Structure & Module Organization
- `jsonl/units_of_measurement.jsonl` is the canonical dataset; `json/` stores array mirrors and must stay in sync during refreshes.
- `index.js` (CommonJS) and `index.mjs` (ESM) expose `load(dataset)` backed by `jsonl/`. The Python module under `units_of_measurement/` mirrors that helper and falls back to the repo data when bundled files are absent.
- `scripts/` houses maintenance tooling. Keep new generators or scrapers here beside `validate_uom.py` so provenance lives in git.

## Build, Test, and Development Commands
- `python -m pip install -e .` – install the Python package in editable mode for notebooks, scripts, and validator runs.
- `python scripts/validate_uom.py` – mandatory before committing dataset or schema changes; it checks uniqueness, field presence, and allowed measurement systems.
- `node -e "console.log(require('./index').load().length)"` – smoke test confirming the Node entry point can read the merged dataset.
- `python -m build` – create wheel and sdist artifacts (requires `build` + `hatchling`); inspect `dist/` before tagging.

## Coding Style & Naming Conventions
- Python scripts use 4-space indentation, f-strings, and standard-library dependencies only; annotate helpers with hints such as `list[dict]` and `Path`.
- JavaScript modules keep `'use strict'`, rely on `const`, and throw descriptive errors for unsupported dataset names.
- Dataset rows must keep `quantity === property`, use `·`/`/` delimiters instead of spaces, respect the measurement-system enum in `scripts/validate_uom.py`, and include a trailing newline.

## Testing Guidelines
- Treat the validator as the regression gate; resolve any non-zero exit and include its success output in PRs that touch data.
- Spot-check numerical edits with `jq` or Python snippets (`jq -c 'select(.unit=="pound")' jsonl/units_of_measurement.jsonl`) and document intentional conversion-factor changes.
- When altering loader code, exercise both APIs (`python - <<'PY'` to import `units_of_measurement.load()` plus the Node one-liner) to confirm matching record counts.

## Commit & Pull Request Guidelines
- Follow the existing history style: concise, present-tense subjects such as `add canonical metadata docs` or `bump version to 1.2.1`, limited to ~70 characters.
- Commit bodies should list affected files, context, and sources. When editing datasets, include validator output or the jq snippets you ran.
- Pull requests must outline scope, flag schema additions, link to upstream references, and include before/after record counts when they change.
