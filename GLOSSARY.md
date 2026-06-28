# DKP Glossary

Definitions of terms used in the [Domain Knowledge Pack Specification](SPEC.md). Terms are listed in alphabetical order. Cross-references to other entries in this glossary are indicated in *italics*.

---

**8-Gate Quality Standard**
The DKP quality framework consisting of eight named gates that determine a bundle's conformance tier. Gates 4 (Machine Usability) and 8 (OKF Conformance) are automated and required for *DKP-Conformant* status. Gate 7 (Evaluation) is required for *DKP-Evaluated* status. Gates 1–3, 5, and 6 require human editorial attestation and are required for *DKP-Reviewed* status. *See §16, §7.2.*

---

**Audience Profile**
A named user persona declared in `manifest.json`. Individual concepts and chunks may be scoped to one or more profiles via an `audience` field; content that omits this field is visible to all profiles. Processors performing a filtered export (e.g., `dkp export --audience <id>`) must omit any content not targeting the requested profile. *See §6.3, §6.6.*

---

**Bundle**
See *DKP Bundle*.

---

**Concept File**
A single `.md` file in the *OKF Layer* that represents one item of domain knowledge. Each concept file carries YAML frontmatter with a required `type` field (one of the seven *DKP Types*) and DKP extension fields including `title`, `description`, `tags`, and `timestamp`. *See §2, §10.3.*

---

**Conformance Language**
The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY as used in the specification carry the meanings defined in RFC 2119. MUST denotes an absolute requirement whose violation renders a bundle or *processor* non-conformant. SHOULD denotes a strong recommendation that may be departed from with deliberate justification. MAY denotes a permitted but non-required behavior. *See §2.1.*

---

**Decision Procedure**
A declarative, traversable decision tree stored in `machine/decision_trees.json` and surfaced as a *Concept File* of type `DecisionProcedure` in `okf/procedures/`. A decision procedure encodes branching logic that an agent reads and follows; it is not executable code. Contrast with *Executable Procedure*. *See §4, §9.6.*

---

**DKP Bundle**
The complete, distributable unit of domain knowledge conforming to this specification. A bundle is a directory tree — or a `.zip` archive derived from it — rooted at the *Pack Root*. It contains `manifest.json`, all required layer subdirectories (`machine/`, `okf/`, `evidence/`), and any optional layers (`human/`, `skills/`, `l10n/`). *See §2, §5.*

---

**DKP-Conformant**
A conformance tier. A bundle achieves DKP-Conformant status by passing Gates 4 and 8 of the *8-Gate Quality Standard*. Gate 7 is skipped (not failed) when `eval_set.jsonl` is absent. *See §7.2.*

---

**DKP-Evaluated**
A conformance tier. A bundle achieves DKP-Evaluated status by meeting all DKP-Conformant requirements and additionally including a populated `eval_set.jsonl` with a passing `eval_results/eval_summary.json` (Gate 7). *See §7.2.*

---

**DKP-Reviewed**
A conformance tier. A bundle achieves DKP-Reviewed status by meeting all DKP-Evaluated requirements and additionally satisfying Gates 1–3, 5, and 6 as evidenced by a dated, named editorial sign-off in `evidence/review_notes.md`. *See §7.2, §12.3.*

---

**DKP Type**
The value of the `type` field in a *Concept File*'s YAML frontmatter. The specification defines exactly seven valid types: `DomainTerm`, `DomainRule`, `Constraint`, `DecisionProcedure`, `KnowledgeChunk`, `EntityType`, and `EvalCase`. Each type maps one-to-one to a specific *Machine Layer* asset. *See §4.*

---

**Evidence Layer**
The `evidence/` subdirectory. Contains provenance and rights documentation for the bundle, including `sources.csv` (one row per information source), `rights_log.csv` (rights status and expiry per source), `review_notes.md` (editorial sign-off), and optional evaluation run results. *See §12.*

---

**Executable Procedure**
A runnable module stored in `machine/procedures/` as a WebAssembly (WASM) binary or alternative script. Implements decision logic too complex for a static *Decision Procedure*. Executable procedures are runtime artifacts and are not OKF concept files. Processors must warn users before executing procedures from bundles without a valid `bundle.sig`. *See §9.12.*

---

**GraphRAG**
A retrieval pattern in which a *processor* traverses the *Knowledge Graph* to follow typed relationships between concepts, enabling multi-hop retrieval beyond simple keyword or semantic similarity matching. For example, a query about a term may lead the processor to elaborating chunks, which in turn link to constraining rules. *See §9.9.*

---

**Human Layer**
The `human/` subdirectory. Contains human-readable companion materials including `handbook.md`, optional PDF and EPUB renderings, a quickstart guide, a cheatsheet, an FAQ, and worked examples. This layer is recommended for commercial distribution but is not required for conformance. *See §11.*

---

**Knowledge Graph**
The file `machine/knowledge_graph.json`. Declares typed, directed edges between concepts within the bundle (e.g., `elaborates`, `requires`, `supersedes`, `contradicts`). Enables *GraphRAG*-style multi-hop retrieval. Processors must flag edges whose endpoints do not resolve to declared nodes, and nodes whose IDs do not resolve to a concept in a machine-layer asset. *See §9.9.*

---

**Localization Layer**
The `l10n/` subdirectory. Contains translated or locale-adapted content for non-base locales, organized as `l10n/{BCP-47-locale}/`. Content present in a locale subdirectory takes precedence over base-pack content for that locale; absent content falls back to the base pack. *See §14.*

---

**Machine Layer**
The `machine/` subdirectory. The authoritative source of truth for all content in a DKP bundle. Contains structured JSON and JSONL assets — including `glossary.json`, `rules.json`, `retrieval_chunks.jsonl`, `ontology.json`, `constraints.json`, and `decision_trees.json` — that can be parsed and injected into an LLM without Markdown processing. The *OKF Layer* is generated from the machine layer. *See §9.*

---

**MCP (Model Context Protocol)**
An open protocol for exposing resources and callable tools to LLM-based agents over a standard interface. A DKP bundle may optionally activate an MCP surface, making its assets accessible via `dkp://` URIs and standardized tools such as `search`, `inject`, `chunk`, and `get`. *See §15.*

---

**OKF (Open Knowledge Format)**
A minimal, vendor-neutral open standard for packaging domain knowledge as Markdown files with YAML frontmatter, released by Google Cloud. OKF requires only one frontmatter field (`type`) and imposes no type taxonomy, schema requirements, or quality bar. DKP is a strict superset of OKF: every DKP bundle's *OKF Layer* is a fully conformant OKF bundle. *See §1, §3.*

---

**OKF Layer**
The `okf/` subdirectory. A fully OKF-conformant bundle generated from the *Machine Layer*, intended for distribution to agent frameworks that natively support OKF. Contains *Concept Files* organized by type (terms, rules, constraints, procedures, chunks, ontology). *See §10.*

---

**Pack Root**
The top-level directory of a *DKP Bundle*. Contains `manifest.json` and all layer subdirectories. When a bundle is distributed as a `.zip` archive, the pack root is the single top-level directory inside that archive. *See §2.*

---

**Processor**
Any tool or library that reads, validates, converts, searches, or evaluates a DKP bundle. Examples include the `dkp` CLI, language-specific SDK libraries, and agent framework integrations. A conformant processor satisfies all MUST and MUST NOT requirements stated for processors in §5–§15. *See §2, §7.2.*

---

**Producer**
Any person or system that creates a DKP bundle. A conformant producer satisfies all MUST and MUST NOT requirements stated for producers throughout the specification. *See §2.*

---

**Retrieval Chunk**
A self-contained unit of domain knowledge stored as a single line in `machine/retrieval_chunks.jsonl`. Each chunk is a short, standalone passage — one fact, rule, or concept — written so that it is fully interpretable without surrounding context. Retrieval chunks are the primary unit injected into an LLM context window during retrieval-augmented generation (RAG): a *processor* searches the chunk set and injects the top-ranked matches for a given query. Optional metadata fields include `retrieval_priority` (force inclusion regardless of query relevance), `token_count` (for context budget planning), `confidence` (producer's accuracy confidence, 0.0–1.0), and `summary` (a ≤100-token abstract for two-stage retrieval). Corresponds to DKP type `KnowledgeChunk`. *See §9.7.*

---

**Retrieval Hints**
A `retrieval_hints` object in `manifest.json` that communicates producer recommendations to retrieval-augmented *processors*. Key fields: `recommended_top_k` (number of chunks to retrieve per query), `max_context_tokens` (recommended token budget for pack content in a single context window), `use_reranker` (whether a reranker pass is advised after initial retrieval), and `embedding_model` (the model used to produce any pre-computed embeddings in the bundle). *See §6.3.*

---

**Rights Record**
A row in `evidence/rights_log.csv` documenting the rights status for a single *Source Record*. Fields include `rights_holder`, `license_type`, `granted_date`, and `expiry_date`. When a source's rights expire, the producer is expected to remove all content derived from that source and issue a new bundle version. *See §12.2.*

---

**Skill Layer**
The `skills/` subdirectory. An optional layer that bundles procedural knowledge alongside the declarative *Machine Layer*. Each skill is a directory containing a `SKILL.md` file conforming to the SKILL.md open standard, optional executable scripts, and optional reference files. Skills describe *how* an agent should act in the domain; the machine layer describes *what* the domain contains. *See §13.*

---

**Source Record**
A row in `evidence/sources.csv` identifying a single information source used in pack generation. Fields include a unique `id`, `title`, `url`, `retrieved_date`, `license`, and `notes`. The `id` is referenced by `source_ref` fields throughout the machine and OKF layers. *See §12.1.*

---

**Stability**
A metadata field on individual machine-layer entries and concept files indicating how likely the content is to change. Valid values: `stable` (authoritative, unlikely to change), `volatile` (expected to change in the near term), `experimental` (provisional; use with caution). Processors may surface this value to callers but do not enforce it. *See §9.2–§9.7.*

---

**TTL / `ttl_days`**
"Time to live." An integer field on machine-layer entries and concept files specifying the number of days after which the content should be reviewed for staleness. The companion field `review_date` expresses the same deadline as an absolute ISO 8601 date. Neither field triggers automated expiry; both are advisory signals for the producer's content maintenance workflow. *See §9.2–§9.7.*
