
## 9. Machine Layer

The `machine/` directory is the source of truth for all DKP content. The OKF layer (§10) is generated from it. All required machine-layer assets MUST be present and non-empty.

### 9.1 `system_prompt.md`

A Markdown document providing a complete system prompt for use as the primary context injection into an LLM or agent.

**Requirements:**

- MUST be valid Markdown
- MUST contain at minimum: a role declaration, the pack's domain scope, and guidance on how to use the pack's knowledge
- SHOULD be structured for direct copy-paste injection into an LLM system prompt field
- SHOULD reference the pack's `name` and `domain`

### 9.2 `rules.json`

A JSON object enumerating operational rules for the domain — what agents MUST do and MUST NOT do when acting in this domain.

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `rules` | array of Rule objects | REQUIRED. One or more rule definitions. |

**Rule object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier within this pack (e.g., `"rule-001"`) |
| `title` | string | REQUIRED | Short human-readable label |
| `description` | string | REQUIRED | The actionable rule statement. SHOULD be a discrete, actionable statement, not a paragraph of prose. |
| `polarity` | string | REQUIRED | One of `"affirmative"` (things to do) or `"prohibitive"` (things to avoid) |
| `source_ref` | string | OPTIONAL | `id` of a record in `evidence/sources.csv` |
| `ttl_days` | integer | OPTIONAL | Days until this rule should be reviewed for staleness |
| `review_date` | string | OPTIONAL | ISO 8601 date for next review |
| `stability` | string | OPTIONAL | One of `"stable"`, `"volatile"`, `"experimental"` |
| `audience` | array of strings | OPTIONAL | Audience profile scoping (see §6.6) |

The `rules` array MUST contain at least one entry with `polarity: "affirmative"` and at least one entry with `polarity: "prohibitive"`.

Normative JSON Schema: see Appendix B §B.4.

### 9.3 `ontology.json`

A JSON object defining the entity types relevant to this domain, their attributes, and relationships between types.

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `entity_types` | array of EntityType objects | REQUIRED. One or more entity type definitions. |

**EntityType object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier within this pack (e.g., `"food-item"`) |
| `name` | string | REQUIRED | Human-readable name |
| `description` | string | REQUIRED | What this entity type represents |
| `attributes` | array of strings | REQUIRED | List of attribute names this entity type carries |
| `relationships` | array of Relationship objects | OPTIONAL | Named relationships to other entity types |

**Relationship object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | REQUIRED | Relationship name (e.g., `"contains"`) |
| `target_type` | string | REQUIRED | `id` of the target EntityType |
| `cardinality` | string | OPTIONAL | `"one-to-one"`, `"one-to-many"`, `"many-to-many"` |

Normative JSON Schema: see Appendix B §B.1.

### 9.4 `glossary.json`

A JSON object defining domain terminology.

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `terms` | array of Term objects | REQUIRED. One or more term definitions. |

**Term object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier (e.g., `"term-001"` style slug) |
| `term` | string | REQUIRED | The canonical term |
| `definition` | string | REQUIRED | Clear, concise definition |
| `aliases` | array of strings | OPTIONAL | Alternative names or abbreviations |
| `related_terms` | array of strings | OPTIONAL | `id` values of related Term objects |
| `source_ref` | string | OPTIONAL | `id` of a record in `evidence/sources.csv` |
| `ttl_days` | integer | OPTIONAL | Days until this term's content should be reviewed for staleness |
| `review_date` | string | OPTIONAL | ISO 8601 date by which this term SHOULD be reviewed |
| `stability` | string | OPTIONAL | One of `"stable"`, `"volatile"`, `"experimental"` |
| `audience` | array of strings | OPTIONAL | Profile IDs from `manifest.json` `audience_profiles`. If absent, visible to all profiles. |

Normative JSON Schema: see Appendix B §B.2.

### 9.5 `constraints.json`

A JSON object enumerating edge cases, anti-patterns, and hard limits for the domain.

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `edge_cases` | array of Constraint objects | REQUIRED. Situations requiring special handling. |
| `anti_patterns` | array of Constraint objects | REQUIRED. Common mistakes to avoid. |
| `hard_limits` | array of Constraint objects | REQUIRED. Absolute prohibitions or non-negotiable boundaries. |

**Constraint object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier |
| `title` | string | REQUIRED | Short label |
| `description` | string | REQUIRED | What the constraint is and why it matters |
| `source_ref` | string | OPTIONAL | `id` of a record in `evidence/sources.csv` |
| `ttl_days` | integer | OPTIONAL | Days until this constraint should be reviewed |
| `review_date` | string | OPTIONAL | ISO 8601 date for next review |
| `stability` | string | OPTIONAL | One of `"stable"`, `"volatile"`, `"experimental"` |
| `audience` | array of strings | OPTIONAL | Audience profile scoping (see §6.6) |

Normative JSON Schema: see Appendix B §B.3.

### 9.6 `decision_trees.json`

A JSON object defining traversable decision procedures — structured logic an agent follows to arrive at a domain-specific answer or recommendation.

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `trees` | array of DecisionTree objects | REQUIRED. One or more decision trees. |

**DecisionTree object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier |
| `title` | string | REQUIRED | Human-readable name |
| `description` | string | REQUIRED | What decision this tree handles |
| `root` | Node object | REQUIRED | The root node of the tree |

**Node object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `question` | string | REQUIRED | The question or decision point at this node |
| `branches` | array of Branch objects | CONDITIONAL | REQUIRED if node is not a leaf |
| `answer` | string | CONDITIONAL | REQUIRED if node is a leaf (terminal answer) |

**Branch object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `condition` | string | REQUIRED | The condition that leads to the child node |
| `next` | Node object | REQUIRED | The child node |

Normative JSON Schema: see Appendix B §B.5.

### 9.7 `retrieval_chunks.jsonl`

A JSONL file where each line is a JSON object representing one self-contained knowledge unit optimized for retrieval-augmented generation (RAG) or direct context injection.

Each line MUST be a valid JSON object with the following fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier within this pack |
| `title` | string | REQUIRED | Short descriptive title |
| `chunk_text` | string | REQUIRED | The self-contained knowledge content. MUST be standalone — no external reference needed to interpret it. |
| `tags` | array of strings | REQUIRED | Non-empty list of tags for search and filtering |
| `source_ref` | string | REQUIRED | `id` of a record in `evidence/sources.csv` |
| `confidence` | number | OPTIONAL | Float in `[0.0, 1.0]`. Producer's confidence in this chunk's accuracy. |
| `summary` | string | OPTIONAL | ≤100-token extractive or abstractive summary for two-stage retrieval. |
| `embedding_model` | string | OPTIONAL | Model used to pre-compute an embedding for this chunk (e.g., `"text-embedding-3-large"`). |
| `token_count` | integer | OPTIONAL | Pre-computed token count for context-budget planning. |
| `retrieval_priority` | string | OPTIONAL | One of `"critical"`, `"high"`, `"normal"`, `"low"`. `"critical"` chunks SHOULD always be included in context regardless of similarity score. |
| `asset_refs` | array of strings | OPTIONAL | `id` values of entries in `machine/assets.json` associated with this chunk. |
| `ttl_days` | integer | OPTIONAL | Days until this chunk should be reviewed for staleness. |
| `review_date` | string | OPTIONAL | ISO 8601 date for next review. |
| `stability` | string | OPTIONAL | One of `"stable"`, `"volatile"`, `"experimental"`. |
| `audience` | array of strings | OPTIONAL | Audience profile scoping (see §6.6). |

Processors validating `retrieval_chunks.jsonl` MUST reject files where any line is not valid JSON. **Because JSON Schema evaluates whole documents, processors MUST validate JSONL files line-by-line: each line MUST be extracted and validated independently against the schema in Appendix B §B.6.** A file is valid only if every line passes individually. If present, `confidence` MUST be a float in `[0.0, 1.0]` inclusive. Bundles containing a `confidence` value outside this range fail schema validation (Gate 4 — Machine Usability).

Normative JSON Schema: see Appendix B §B.6.

### 9.8 `eval_set.jsonl` (Recommended)

A JSONL file where each line is a JSON object representing one evaluation case — a question, expected answer dimensions, and scoring rubric used to measure pack quality empirically. This file is RECOMMENDED. Packs that omit it are still conformant, but Gate 7 will be skipped rather than evaluated.

Each line MUST be a valid JSON object with the following fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | REQUIRED | The evaluation question |
| `expected_dimensions` | array of strings | REQUIRED | Non-empty list of answer dimensions that a correct response must address |
| `critical_must_include` | array of strings | REQUIRED | Non-empty list of specific facts, terms, or statements that MUST appear in a correct answer |
| `scoring_rubric` | string | REQUIRED | Prose or structured rubric for judging response quality |
| `version_meta` | object | REQUIRED | Versioning metadata (see below) |

**`version_meta` object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `prompt_hash` | string | REQUIRED | SHA-256 of the system prompt used when this eval case was generated |
| `model_version` | string | REQUIRED | Model identifier used for generation (e.g., `"claude-sonnet-4-6"`) |
| `dataset_version` | string | REQUIRED | Semver version of the eval dataset |

Normative JSON Schema: see Appendix B §B.7.

### 9.9 `knowledge_graph.json` (Recommended)

A JSON object declaring typed edges between concepts within this bundle, enabling GraphRAG-style multi-hop retrieval and concept deprecation tracking without prose parsing.

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `nodes` | array of Node objects | REQUIRED. One entry per concept referenced in the graph. |
| `edges` | array of Edge objects | REQUIRED. One entry per typed relationship. |

**Node object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | The `id` of a concept in any machine-layer asset (e.g., a glossary term id, chunk id) |
| `type` | string | REQUIRED | The DKP type of this concept (`"DomainTerm"`, `"KnowledgeChunk"`, etc.) |

**Edge object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `from` | string | REQUIRED | Node `id` of the source concept |
| `to` | string | REQUIRED | Node `id` of the target concept |
| `relation` | string | REQUIRED | Relationship type. MUST be one of the defined relation types (see below). |
| `weight` | number | OPTIONAL | Float in `[0.0, 1.0]`. Strength or confidence of the relationship. |

**Defined relation types:**

| Relation | Description |
|---|---|
| `requires` | Source concept requires target concept to be understood or applied |
| `contradicts` | Source concept contradicts or is in tension with target concept |
| `elaborates` | Source concept expands on or provides detail for target concept |
| `supersedes` | Source concept replaces target concept; target SHOULD be treated as deprecated |
| `part-of` | Source concept is a component of target concept |
| `depends-on` | Source concept's correctness or validity depends on target concept |
| `see-also` | Non-directional association; target may be relevant when using source |
| `measured-by` | Source concept (an entity) is quantified using target concept (a metric or term) |
| `defined-by` | Source concept's meaning is given by target concept |
| `specializes` | Source concept is a narrower subtype or specialization of target concept |

Processors building knowledge graphs from this bundle SHOULD load `knowledge_graph.json` before performing multi-hop retrieval. Processors MUST flag edges whose `from` or `to` values do not resolve to a node in the `nodes` array as errors (this check is part of Gate 4 — Machine Usability). Processors MUST also verify that every `id` in the `nodes` array resolves to a valid concept `id` present in one of the bundle's machine-layer JSON/JSONL assets (e.g., `glossary.json`, `retrieval_chunks.jsonl`, `rules.json`, `constraints.json`, `assets.json`, `decision_trees.json`). Nodes that do not resolve to any machine-layer concept MUST be flagged as errors (this check is part of Gate 4 — Machine Usability). Producers are responsible for eliminating dangling edges before release, particularly when removing chunks due to source rights expiry (see §12.2).

Normative JSON Schema: see Appendix B §B.9.

### 9.10 `taxonomy.json` (Optional)

A JSON object mapping DKP concepts to external controlled vocabularies, enabling interoperability with enterprise knowledge graphs (SKOS), structured data systems (Schema.org), and linked data networks (Wikidata).

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `concept_scheme` | object | OPTIONAL. Metadata about this bundle as a SKOS ConceptScheme. |
| `mappings` | array of Mapping objects | REQUIRED. One or more concept mappings. |

**ConceptScheme object fields:**

| Field | Type | Description |
|---|---|---|
| `uri` | string | Canonical URI for this bundle as a SKOS ConceptScheme |
| `skos_type` | string | Always `"skos:ConceptScheme"` |
| `dc_title` | string | Dublin Core title |
| `dc_creator` | string | Dublin Core creator |

**Mapping object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `dkp_id` | string | REQUIRED | `id` of the concept in any machine-layer asset |
| `skos_exactMatch` | string | OPTIONAL | URI of an exactly equivalent SKOS concept in an external vocabulary |
| `skos_closeMatch` | string | OPTIONAL | URI of a closely related SKOS concept |
| `schema_org_type` | string | OPTIONAL | Schema.org type URI this concept maps to |
| `wikidata` | string | OPTIONAL | Wikidata QID (e.g., `"Q178661"`) |

Processors exporting to SKOS or RDF SHOULD use `taxonomy.json` as the authoritative mapping source. Processors that do not support vocabulary alignment MUST silently ignore this file.

Normative JSON Schema: see Appendix B §B.10.

### 9.11 `assets.json` and `assets/` (Optional)

`machine/assets.json` declares multi-modal assets (images, structured tables, audio transcripts) that augment the text content of the bundle. Binary assets reside in `machine/assets/`.

**Required top-level keys of `assets.json`:**

| Key | Type | Description |
|---|---|---|
| `assets` | array of Asset objects | REQUIRED. One or more asset entries. |

**Asset object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier referenced by `asset_refs` in retrieval chunks and concept files |
| `type` | string | REQUIRED | One of `"image"`, `"table"`, `"audio"`, `"video"` |
| `path` | string | REQUIRED | Relative file path of the asset, originating from within the `machine/assets/` directory |
| `source_ref` | string | REQUIRED | `id` of a record in `evidence/sources.csv` |
| `alt_text` | string | CONDITIONAL | REQUIRED for `type: "image"`. Screen-reader and LLM-facing description. |
| `caption` | string | OPTIONAL | Human-readable caption |
| `description` | string | OPTIONAL | Semantic description of the asset's content and relevance |
| `columns` | array of strings | CONDITIONAL | REQUIRED for `type: "table"`. Column names in order. Enables row-level semantic decomposition for tabular RAG. |
| `transcript` | string | OPTIONAL | For `type: "audio"` or `"video"`. Text transcript of spoken content. |

Processors that support multi-modal retrieval SHOULD index asset `alt_text`, `description`, and `transcript` alongside retrieval chunks, making them searchable via the `search` MCP tool when `asset_types` includes `"assets"` (see Appendix B §B.16). Processors that do not support multi-modal content MUST silently ignore `assets.json` and `machine/assets/`.

Normative JSON Schema: see Appendix B §B.11.

### 9.12 `procedures/` (Optional)

> **Note:** `machine/procedures/` contains *executable* procedures (WASM binaries or scripts). For the declarative *decision procedure* concept files, see `okf/procedures/` (§10) and the `DecisionProcedure` type (§4).

The `machine/procedures/` directory contains runnable modules that implement decision logic too complex for static JSON decision trees. Each procedure is represented by three files sharing a common `{procedure-id}` stem:

| File | Required | Description |
|---|---|---|
| `{procedure-id}.wasm` | OPTIONAL | WebAssembly binary compiled to the WASI (WebAssembly System Interface) target. RECOMMENDED execution format for maximum portability and sandboxing. When absent, the producer MUST supply an alternative executable alongside `{procedure-id}.schema.json` and MUST declare the entry point in `{procedure-id}.schema.json` as described below. |
| `{procedure-id}.schema.json` | REQUIRED | JSON Schema for the procedure's input and output objects. When `{procedure-id}.wasm` is absent, MUST also contain a top-level `entry_point` object with two fields: `filename` (string — the exact filename of the alternative executable, including extension, e.g., `"macro_calculator.py"`) and `command` (string — the full execution command string, e.g., `"python3 macro_calculator.py"`). Processors MUST read `entry_point` from this file to locate and invoke the alternative executable; processors MUST NOT scan `machine/procedures/` by file extension to guess the entry point. |
| `{procedure-id}.md` | REQUIRED | Human-readable description, usage examples, and parameter documentation |

> **Note:** When `{procedure-id}.wasm` is absent, `procedure_capabilities.sandbox` (§6.4) SHOULD be set to `"none"` or a value appropriate for the alternative runtime.

> **Security Warning:** Non-WASM executables (e.g., Python scripts, shell scripts) do not provide the sandboxing guarantees of the WASM/WASI target. Processors executing non-WASM procedures MUST apply their host environment's native sandboxing mechanisms. Processors SHOULD refuse to execute non-WASM procedures from bundles where `procedure_capabilities.sandbox` (§6.4) is not explicitly declared, or where the bundle lacks a valid `bundle.sig`. The security risks of arbitrary code execution in non-sandboxed environments remain the responsibility of the processor implementation.

Producers MUST declare `procedure_capabilities` in `manifest.json` (see §6.4) when `machine/procedures/` is non-empty. The `procedure_capabilities.sandbox` value SHOULD be `"wasm"` for bundles using the standard WASM entry point. Processors that execute procedures SHOULD honor the constraints declared in `procedure_capabilities` or SHOULD delegate enforcement to their host environment's native execution sandbox. Processors MUST warn users before executing any procedure from a bundle lacking a valid `bundle.sig`.

Normative JSON Schema for `{procedure-id}.schema.json`: see Appendix B §B.23.

### 9.13 `cross_refs.json` (Optional)

A JSON object declaring cross-pack concept references — links from concepts in this bundle to concepts in declared dependency packs. Requires at least one entry in `manifest.json` `dependencies`.

**Required top-level keys:**

| Key | Type | Description |
|---|---|---|
| `cross_refs` | array of CrossRef objects | REQUIRED. One or more cross-pack references. |

**CrossRef object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `local_id` | string | REQUIRED | `id` of the concept in this bundle |
| `remote_pack` | string | REQUIRED | `name` of the dependency bundle |
| `remote_id` | string | REQUIRED | `id` of the concept in the dependency bundle |
| `relation` | string | REQUIRED | One of the relation types defined in §9.9 |

Processors resolving cross-pack references MUST verify that the named `remote_pack` appears in `manifest.json` `dependencies`. If `cross_refs.json` is present, processors MUST verify that each `local_id` value resolves to a concept present in the current bundle — i.e., exists as a node `id` in `knowledge_graph.json`, or as an `id` in `glossary.json`, `retrieval_chunks.jsonl`, `ontology.json`, `constraints.json`, `rules.json`, or `decision_trees.json`. Processors MUST warn (but MUST NOT error) when the referenced dependency bundle is unavailable.

Normative JSON Schema: see Appendix B §B.12.
