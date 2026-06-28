#!/usr/bin/env python3
"""Validate all docs/schemas/v1/*.json files as JSON Schema Draft 2020-12."""
import json
import sys
from pathlib import Path

import jsonschema

schemas_dir = Path(__file__).parent.parent / "schemas" / "v1"
errors = []

for path in sorted(schemas_dir.glob("*.json")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(data)
        print(f"  OK  {path.name}")
    except jsonschema.exceptions.SchemaError as e:
        errors.append((path.name, e.message))
        print(f"  FAIL {path.name}: {e.message}")
    except json.JSONDecodeError as e:
        errors.append((path.name, f"Invalid JSON: {e}"))
        print(f"  FAIL {path.name}: Invalid JSON: {e}")

if errors:
    print(f"\n{len(errors)} schema(s) failed validation.", file=sys.stderr)
    sys.exit(1)

print(f"\nAll {len(list(schemas_dir.glob('*.json')))} schemas valid.")
