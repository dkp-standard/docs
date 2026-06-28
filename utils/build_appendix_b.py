#!/usr/bin/env python3
"""Regenerate sections/appendix_b_json_schemas.md from docs/schemas/v1/*.json."""
import json
from pathlib import Path

docs_dir = Path(__file__).parent.parent
schemas_dir = docs_dir / "schemas" / "v1"
output_path = docs_dir / "sections" / "appendix_b_json_schemas.md"

SCHEMAS = [
    ("ontology.json",          "B.1 `ontology.json` Schema"),
    ("glossary.json",          "B.2 `glossary.json` Schema"),
    ("constraints.json",       "B.3 `constraints.json` Schema"),
    ("rules.json",             "B.4 `rules.json` Schema"),
    ("decision_trees.json",    "B.5 `decision_trees.json` Schema"),
    ("retrieval_chunk.json",   "B.6 `retrieval_chunks.jsonl` Line Schema"),
    ("eval_entry.json",        "B.7 `eval_set.jsonl` Line Schema"),
    ("concept_frontmatter.json", "B.8 OKF Concept File Frontmatter Schema"),
    ("knowledge_graph.json",   "B.9 `knowledge_graph.json` Schema"),
    ("taxonomy.json",          "B.10 `taxonomy.json` Schema"),
    ("assets.json",            "B.11 `assets.json` Schema"),
    ("cross_refs.json",        "B.12 `cross_refs.json` Schema"),
    ("eval_summary.json",      "B.13 `eval_results/eval_summary.json` Schema"),
    ("mcp_manifest.json",      "B.14 `machine/mcp_manifest.json` Schema"),
    ("mcp_tool_inject.json",          "B.15 `inject` Tool Input Schema"),
    ("mcp_tool_search.json",          "B.16 `search` Tool Input Schema"),
    ("mcp_tool_chunk.json",           "B.17 `chunk` Tool Input Schema"),
    ("mcp_tool_get.json",             "B.18 `get` Tool Input Schema"),
    ("mcp_tool_list_procedures.json", "B.19 `list_procedures` Tool Input Schema"),
    ("mcp_tool_run_procedure.json",   "B.20 `run_procedure` Tool Input Schema"),
    ("mcp_response.json",             "B.21 MCP Resource Response Envelope Schema"),
    ("manifest.json",          "B.22 `manifest.json` Schema"),
    ("procedure_schema.json",  "B.23 `{procedure-id}.schema.json` Schema"),
    ("sources_csv_schema.json",    "B.24 `evidence/sources.csv` Frictionless Table Schema"),
    ("rights_log_csv_schema.json", "B.25 `evidence/rights_log.csv` Frictionless Table Schema"),
]

PREAMBLE = """\
<!-- AUTO-GENERATED — edit docs/schemas/v1/*.json, then run build_spec.py -->
## Appendix B — JSON Schemas (Normative)

The schemas in this appendix are normative. Conformant DKP bundles MUST produce assets that validate against these schemas. Conformant processors MUST reject assets that fail validation.

Schemas use [JSON Schema Draft 2020-12](https://json-schema.org/specification).
"""

blocks = [PREAMBLE]
for filename, header in SCHEMAS:
    schema_path = schemas_dir / filename
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    pretty = json.dumps(data, indent=2)
    blocks.append(f"\n### {header}\n\n```json\n{pretty}\n```\n")

output_path.write_text("".join(blocks), encoding="utf-8")
print(f"Built {output_path} ({output_path.stat().st_size} bytes)")
