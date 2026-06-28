
## 2. Terminology

**DKP Bundle** — A directory tree (or `.zip` archive derived from it) that conforms to this specification. The root of the tree is the *pack root*.

**Pack Root** — The directory containing `manifest.json` and the layer subdirectories.

**Machine Layer** — The `machine/` subdirectory. Contains structured JSON, JSONL, and Markdown assets that are the source of truth for all DKP content. The OKF layer is generated from the machine layer.

**OKF Layer** — The `okf/` subdirectory. A fully OKF-conformant bundle generated from the machine layer, intended for distribution to OKF-compatible agent frameworks.

**Human Layer** — The `human/` subdirectory. Contains human-readable companion materials (Markdown, PDF, EPUB).

**Evidence Layer** — The `evidence/` subdirectory. Contains provenance, rights, and review documentation.

**Skill Layer** — The `skills/` subdirectory. Contains SKILL.md-compatible procedural knowledge bundled alongside the declarative machine layer.

**Localization Layer** — The `l10n/` subdirectory. Contains translated or locale-adapted content for non-base locales.

**Concept File** — A `.md` file in the OKF layer with YAML frontmatter, representing one DKP concept.

**DKP Type** — The value of the `type` field in a concept file's frontmatter. MUST be one of the seven values defined in §4.

**Processor** — Any tool or library that reads, validates, converts, searches, or evaluates a DKP bundle.

**Producer** — Any person or system that creates a DKP bundle.

**Source Record** — A row in `evidence/sources.csv` identifying a single information source used in pack generation.

**Rights Record** — A row in `evidence/rights_log.csv` recording rights status for a source record.

**Audience Profile** — A named target reader or agent role declared in `manifest.json`, used for conditional content filtering.

**Decision Procedure** — A declarative decision-tree asset (DKP type `DecisionProcedure`) stored in `okf/procedures/` as a JSON file. Represents human-readable branching logic; not directly executable. See §4 and §10.

**Executable Procedure** — A runnable module stored in `machine/procedures/` as a WASM binary or alternative script (see §9.12). Implements decision logic too complex for a static JSON decision tree. Distinct from a Decision Procedure: executable procedures are runtime artifacts, not OKF concept files.

### 2.1 Conformance Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in normative sections of this document are to be interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14) ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when they appear in all capitals.

Normative sections are: §5–§16 and Appendix B. All other sections are informative.

