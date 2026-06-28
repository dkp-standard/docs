# Domain Knowledge Pack (DKP) Specification

**Version:** 1.0.0
**Status:** Draft 1
**Date:** 2026-06-21
**Author:** Jay Mathis <https://jaymath.is>
**License:** Apache 2.0

---

## Abstract

This document defines the Domain Knowledge Pack (DKP) format — an open standard for packaging curated domain knowledge for use by AI agents, humans, and language model applications. The DKP format extends the Open Knowledge Format (OKF) v0.1 with a mandatory structured machine layer, a rich type taxonomy, provenance requirements, and a defined quality bar. Every conformant DKP bundle contains a valid OKF bundle in its `okf/` layer. This specification describes the bundle structure, asset schemas, frontmatter extensions, and conformance requirements for both producers and processors.

---

## Status of This Document

This is version 1.0.0-draft.1 of the DKP Specification, a Draft. Future versions will be published with a version number increment. See §8 (Versioning) for the change policy.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Terminology](#2-terminology)
3. [Relationship to OKF](#3-relationship-to-okf)
4. [DKP Type Taxonomy](#4-dkp-type-taxonomy)
5. [Bundle Structure](#5-bundle-structure)
6. [Manifest](#6-manifest)
7. [Conformance](#7-conformance)
8. [Versioning](#8-versioning)
9. [Machine Layer](#9-machine-layer)
10. [OKF Layer](#10-okf-layer)
11. [Human Layer](#11-human-layer)
12. [Evidence Layer](#12-evidence-layer)
13. [Skill Layer](#13-skill-layer)
14. [Localization Layer](#14-localization-layer)
15. [MCP Surface](#15-mcp-surface)
16. [The 8-Gate Quality Standard](#16-the-8-gate-quality-standard)
17. [Appendix A — Complete Bundle Example](#appendix-a--complete-bundle-example)
18. [Appendix B — JSON Schemas (Normative)](#appendix-b--json-schemas-normative)
19. [Appendix C — Normative References](#appendix-c--normative-references)
20. [Appendix D — Informative References](#appendix-d--informative-references)

---

## 1. Introduction

The Open Knowledge Format (OKF), released by Google Cloud on 2026-06-12, established a vendor-neutral, Markdown-based format for packaging curated domain knowledge for AI agents. OKF is deliberately minimal: a directory of `.md` files with YAML frontmatter, one required field (`type`), Apache 2.0 licensed.

OKF defines a *format*. It does not prescribe a type taxonomy, a machine-readable structured layer, quality requirements, provenance tracking, or evaluation methodology.

The **Domain Knowledge Pack (DKP) Specification** fills that gap. It defines:

- A six-layer bundle structure (`machine/`, `okf/`, `human/`, `evidence/`, `skills/`, `l10n/`) with the `machine/` layer as source of truth
- A strict OKF type taxonomy for all DKP concept types
- Required YAML frontmatter extensions applied to all OKF concept files
- Schema definitions for all machine-layer assets
- A typed knowledge graph for GraphRAG-style multi-hop retrieval
- Multi-modal asset support (images, structured tables)
- Audience-scoped conditional content
- Freshness and staleness signals per concept
- Vocabulary alignment to SKOS and Schema.org
- A skill layer for bundling procedural knowledge alongside declarative knowledge
- A localization layer for multilingual bundles
- Access control declarations and supply-chain integrity mechanisms
- Retrieval hints for context-budget-aware processors
- Federated dependency declarations for multi-pack composition
- Provenance and rights-tracking requirements
- An 8-gate quality standard that distinguishes a DKP from an arbitrary OKF bundle

The design goals of the DKP format are:

- **OKF conformance** — strict OKF encapsulation: the `okf/` layer of a DKP bundle is a fully conformant OKF bundle, generated from the `machine/` layer and traversable by any OKF-native tool
- **Machine usability** — structured JSON/JSONL assets in `machine/` are directly injectable into LLM context, parseable without markdown processing, and evaluable against a shipped eval set
- **Human usability** — the `human/` layer provides a readable companion guide for non-technical users
- **Provenance** — the `evidence/` layer documents sources, rights, and editorial review for every pack
- **Universality** — the format is viable for global enterprise deployments across domains, audiences, locales, and agent frameworks

### Non-Goals

The DKP Specification does not:

- Define the generation pipeline by which packs are produced
- Prescribe which LLM frameworks or agent stacks a consumer must use
- Constrain the body of OKF concept files beyond what OKF itself requires
- Replace or compete with OKF; DKP is a strict superset

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

---

## 3. Relationship to OKF

DKP is a strict extension of OKF. All DKP-specific frontmatter fields are valid OKF (OKF permits producer-defined fields beyond `type`). Any OKF-compatible agent framework can load and traverse the DKP `okf/` layer without modification.

The relationship is summarized as:

```
OKF — vendor-neutral format (files + frontmatter)
 └── DKP — type taxonomy + machine layer + quality bar + provenance
            + knowledge graph + multi-modal + skills + localization
            + access control + supply-chain integrity
```

The DKP type taxonomy (§4) is a named subset of OKF's open-ended `type` field. Producers MUST use only the defined DKP types in the `okf/` layer of a conformant DKP bundle. Processors MUST NOT reject unknown `type` values when performing general OKF operations, but DKP-specific validation MUST flag unknown types as errors.

## 4. DKP Type Taxonomy

The DKP Type Taxonomy defines the seven canonical type values used throughout a DKP bundle. It governs both the machine layer (§9) and the OKF layer (§10): machine-layer assets map one-to-one to taxonomy entries, and every concept file in the `okf/` directory MUST declare one of these types in its frontmatter.

All concept files in the DKP OKF layer MUST use one of the following seven `type` values. These are valid OKF type values (OKF permits any producer-defined type string).

| DKP Type | Corresponding Machine Asset | Description |
|---|---|---|
| `DomainTerm` | `glossary.json` terms | A glossary entry: canonical term, definition, aliases, related terms |
| `DomainRule` | `rules.json` entries | An operational must-do or must-avoid for agents acting in this domain |
| `Constraint` | `constraints.json` entries | An edge case, anti-pattern, or hard limit |
| `DecisionProcedure` | `decision_trees.json` trees | A traversable decision tree or procedure |
| `KnowledgeChunk` | `retrieval_chunks.jsonl` entries | A self-contained distilled fact for RAG or direct injection |
| `EntityType` | `ontology.json` entity types | A domain entity with attributes and relationships |
| `EvalCase` | `eval_set.jsonl` entries | An evaluation Q/A case (transparency asset) |

Concept files using `EvalCase` type are OPTIONAL and SHOULD be omitted from packs where evaluation transparency is not desired.

Processors performing DKP-specific validation MUST flag any `type` value not in this table as an error.

## 5. Bundle Structure

### 5.1 Directory Layout

A conformant DKP bundle MUST have the following directory structure at its pack root. Items marked **[R]** are REQUIRED; items marked **[S]** are SHOULD (RECOMMENDED); items marked **[O]** are OPTIONAL.

```
{pack-root}/
  manifest.json                [R]
  checksums.json               [S]
  bundle.sig                   [O]
  README.md                    [S]
  LICENSE.md                   [S]
  CHANGELOG.md                 [S]
  machine/                     [R]
    system_prompt.md           [R]
    rules.json                 [R]
    ontology.json              [R]
    glossary.json              [R]
    constraints.json           [R]
    decision_trees.json        [R]
    retrieval_chunks.jsonl     [R]
    eval_set.jsonl             [S]
    knowledge_graph.json       [S]
    taxonomy.json              [O]
    assets.json                [O]
    assets/                    [O]
    procedures/                [O]
    cross_refs.json            [O]
    mcp_manifest.json          [O]
  okf/                         [R]
    index.md                   [R]
    log.md                     [S]
    terms/                     [S]
    rules/                     [S]
    constraints/               [S]
    procedures/                [S]
    chunks/                    [S]
    ontology/                  [S]
  human/                       [S]
    handbook.md                [S]
    handbook.pdf               [O]
    handbook.epub              [O]
    quickstart.md              [O]
    cheatsheet.md              [O]
    faq.md                     [O]
    examples/                  [O]
  evidence/                    [R]
    sources.csv                [R]
    rights_log.csv             [R]
    review_notes.md            [S]
    eval_results/              [S]
      eval_summary.json        [S]
      {date}-{model}.jsonl     [S]
  skills/                      [O]
    index.md                   [S]
    {skill-name}/              [O]
      SKILL.md                 [R]
      scripts/                 [O]
      references/              [O]
  l10n/                        [O]
    {locale}/                  [O]
      machine/                 [O]
        glossary.json          [O]
        system_prompt.md       [O]
      okf/                     [O]
        terms/                 [O]
      human/                   [O]
        handbook.md            [O]
```

A bundle distributed as a `.zip` archive MUST contain the pack root as the top-level directory within the archive.

Processors MUST NOT require the presence of OPTIONAL files. Processors MAY warn when RECOMMENDED files are absent.

### 5.2 Archive Format

A DKP bundle MAY be distributed as:

- A directory tree (e.g., as a Git repository or subdirectory)
- A `.zip` archive with a SHA-256 checksum file (`{name}-v{version}.zip.sha256`)

Processors MUST support directory trees. Processors SHOULD support `.zip` archives.

### 5.3 Pack Naming

The pack root directory name SHOULD match the `name` field in `manifest.json`, with spaces replaced by hyphens and all characters lowercased. This is a convention for tooling, not a conformance requirement.

### 5.4 Supply-Chain Integrity Files

#### `checksums.json`

A JSON object listing the SHA-256 digest of every file in the bundle at the time of signing. Processors SHOULD verify all checksums in `checksums.json` before loading bundle content. Processors MUST warn when a file's actual digest does not match its recorded checksum.

The top-level key is the relative file path from the pack root; the value is the lowercase hex SHA-256 digest:

```json
{
  "manifest.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "machine/glossary.json": "..."
}
```

#### `bundle.sig`

A detached cryptographic signature (Ed25519) over the SHA-256 of the bundle's canonical serialization (deterministic `tar` ordering of all files listed in `checksums.json`). Processors SHOULD verify `bundle.sig` against the publisher's public key declared in `manifest.json` `publisher.pgp_fingerprint` when present. Processors MUST warn when loading bundles from a registry that lack a valid `bundle.sig`.

---

## 6. Manifest

### 6.1 Overview

`manifest.json` is a JSON object at the pack root. It declares the pack's identity, scope, compatibility metadata, access control policy, retrieval hints, and dependency graph. Processors MUST parse `manifest.json` before accessing any other asset.

Normative JSON Schema: see Appendix B §B.22.

### 6.2 Required Fields

All fields in this section are REQUIRED. Processors MUST reject (exit non-zero / return error) any bundle where `manifest.json` is absent, is not valid JSON, or is missing any REQUIRED field.

#### `spec`

- **Type:** string
- **Constraints:** MUST be a Semantic Versioning 2.0.0 string identifying the DKP Specification version this bundle was produced against (e.g., `"1.0.0"`). Processors SHOULD use this field to determine compatibility and SHOULD warn when the value differs from the processor's supported specification version.
- **Example:** `"1.0.0"`

#### `name`

- **Type:** string
- **Constraints:** Non-empty. Human-readable display name of the pack.
- **Example:** `"Nutrition for Men"`

#### `version`

- **Type:** string
- **Constraints:** MUST conform to Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`). See §8.
- **Example:** `"0.1.0"`

#### `domain`

- **Type:** string
- **Constraints:** Non-empty. Top-level domain category (e.g., `"Health"`, `"Programming"`, `"Internet Marketing"`). Producers SHOULD use a consistent taxonomy across packs.
- **Example:** `"Health"`

#### `audience`

- **Type:** string
- **Constraints:** Non-empty. Prose description of the intended user type (human or agent).
- **Example:** `"Adult men aged 18–65 seeking evidence-based nutrition guidance"`

#### `intended_use`

- **Type:** string
- **Constraints:** Non-empty. Authorized use cases for this pack.
- **Example:** `"LLM context injection, RAG retrieval, agent grounding for nutrition Q&A"`

#### `known_limitations`

- **Type:** string
- **Constraints:** Non-empty. What the pack does not cover or where it may be inaccurate.
- **Example:** `"Does not cover clinical conditions, eating disorders, or pediatric nutrition"`

#### `update_date`

- **Type:** string
- **Constraints:** ISO 8601 date (`YYYY-MM-DD`). Date of the most recent content update.
- **Example:** `"2026-06-21"`

#### `compatibility`

- **Type:** array of strings
- **Constraints:** Non-empty array. Each string names an agent framework or model that this pack has been tested with.
- **Example:** `["OpenAI GPT-4o", "Anthropic Claude Sonnet 4.6", "LangChain v0.3", "LlamaIndex v0.11"]`

### 6.3 Recommended Fields

Fields in this section are RECOMMENDED. Processors SHOULD recognize and surface these fields.

#### `source_policy`

- **Type:** string
- Summary of the source selection policy used during pack generation. Producers SHOULD include this field when content is derived from external sources. Packs built entirely from internal or self-authored content (e.g., internal architecture docs, mathematical axioms) MAY omit it or use a value such as `"internal-only"` or `"not-applicable"`.
- **Example:** `"Sources limited to peer-reviewed studies, government dietary guidelines, and established nutrition authorities published after 2020"`

#### `description`

- **Type:** string
- A short (1–3 sentence) prose description of what the pack covers and for whom.

#### `tags`

- **Type:** array of strings
- Keywords for discovery and search.

#### `license`

- **Type:** string
- SPDX license identifier or prose license name for the pack content.
- **Example:** `"Proprietary"`, `"CC-BY-4.0"`

#### `audience_profiles`

- **Type:** array of AudienceProfile objects
- Declares named audience profiles for conditional content filtering (see §6.6). If absent, all content in the bundle is treated as universally visible.

**AudienceProfile object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | REQUIRED | Unique identifier for this profile (e.g., `"consumer"`) |
| `label` | string | REQUIRED | Human-readable name |
| `requires_role` | string | OPTIONAL | Role string an agent or user must hold to receive content scoped to this profile |

#### `retrieval_hints`

- **Type:** object
- Pack-level hints for retrieval-augmented processors. Processors SHOULD use these values as defaults when assembling context from this bundle.

| Field | Type | Description |
|---|---|---|
| `recommended_top_k` | integer | Recommended number of chunks to retrieve per query |
| `max_context_tokens` | integer | Maximum token budget the producer recommends for this pack's content in a single context window |
| `use_reranker` | boolean | Whether a reranker pass is recommended after initial retrieval |
| `embedding_model` | string | Model name used to produce pre-computed embeddings in this bundle, if any |
| `index_version` | string | ISO 8601 date or version string identifying the embedding index version |

#### `min_eval_delta`

- **Type:** number (`[0.0, 1.0]`)
- The minimum required improvement in aggregate eval score (with-pack vs. baseline) for Gate 7 to pass. Producers SHOULD set this to at least `0.10`. Processors running `dkp eval` MUST flag a Gate 7 failure if the measured delta is below this value. When this field is absent, processors running `dkp eval` MUST treat the threshold as `0.0` (any non-negative delta passes Gate 7).

> **Note:** When `eval_set.jsonl` is absent, Gate 7 is skipped regardless of whether `min_eval_delta` is present. The presence of `min_eval_delta` does not obligate a processor to locate or require `eval_set.jsonl`.

#### `locales`

- **Type:** array of strings
- BCP 47 locale tags for which translated content exists in `l10n/`. The base locale is always `"en-US"` unless overridden by `base_locale`.
- **Example:** `["en-US", "es-MX", "fr-FR"]`

#### `base_locale`

- **Type:** string
- BCP 47 locale tag for the base locale of this pack. Defaults to `"en-US"` when absent. Override this field when the primary authoring language is not US English.
- **Example:** `"fr-FR"`

### 6.4 Optional Fields

#### `publisher`

- **Type:** object
- Identifies the pack's publisher for supply-chain integrity verification.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | REQUIRED | Publisher display name |
| `url` | string | OPTIONAL | Publisher's canonical URL |
| `pgp_fingerprint` | string | OPTIONAL | Ed25519 or PGP public key fingerprint used to verify `bundle.sig` |
| `signed` | boolean | OPTIONAL | Whether this bundle is signed. MUST be `true` if `bundle.sig` is present. |

#### `access_control`

- **Type:** object
- Declares the access control policy the producer expects processors to enforce.

| Field | Type | Description |
|---|---|---|
| `classification` | string | One of `"public"`, `"internal"`, `"confidential"`, `"restricted"` |
| `required_roles` | array of strings | Roles an agent or user must hold to load this bundle |
| `export_restrictions` | array of strings | Redistribution constraints (e.g., `"no-redistribution"`, `"internal-only"`) |
| `encryption_required` | boolean | Whether the bundle MUST be stored encrypted at rest |
| `pii_present` | boolean | Whether any content contains personally identifiable information |
| `gdpr_scope` | boolean | Whether GDPR data handling requirements apply to this bundle's content |
| `mcp_scopes_required` | array of strings | OPTIONAL. OAuth 2.1 scopes an MCP client must present to access this bundle's resources. Ignored when `mcp.tool_provider.auth.scheme` is `"none"`. |
| `mcp_audience` | string | OPTIONAL. OAuth 2.1 `aud` claim expected in JWT tokens when `mcp.tool_provider.auth.scheme` is `"bearer"` or `"oauth2"`. |

The `mcp_scopes_required` and `mcp_audience` fields bridge the `access_control` policy declaration to the `mcp.tool_provider.auth` enforcement mechanism (§15.3). Readers unfamiliar with MCP integration should refer to §15 (MCP Surface) for full context on how these fields are enforced. For bundles with `classification: "public"`, both fields SHOULD be omitted.

Processors SHOULD surface `access_control` fields to calling applications. Processors MUST NOT silently discard `access_control` declarations.

#### `dependencies`

- **Type:** array of Dependency objects
- Declares other DKP bundles that this pack depends on for cross-referenced concepts (see §9.13).

**Dependency object fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | REQUIRED | `name` field of the dependency bundle |
| `version` | string | REQUIRED | SemVer range (e.g., `">=1.2.0"`) or exact version |
| `domain` | string | OPTIONAL | `domain` field of the dependency bundle |
| `registry` | string | OPTIONAL | URL of the registry from which the dependency can be resolved |
| `optional` | boolean | OPTIONAL | If `true`, processors MAY load the bundle without resolving this dependency |

#### `procedure_capabilities`

- **Type:** object
- Declares the sandbox constraints the producer requires for any runnable scripts in `machine/procedures/`. This field is an advisory declaration by the producer, not a runtime mandate on the processor.

| Field | Type | Description |
|---|---|---|
| `sandbox` | string | Execution environment (e.g., `"wasm"`, `"none"`) |
| `max_runtime_ms` | integer | Maximum allowed wall-clock time per procedure invocation |
| `network_access` | boolean | Whether procedures are permitted to make network calls |
| `filesystem_access` | string | One of `"none"`, `"read-only"`, `"read-write"` |

Processors that execute procedures SHOULD honor these constraints or SHOULD delegate enforcement to their host environment's native execution sandbox. Processors that cannot satisfy the declared constraints MAY decline to execute procedures and MUST inform the caller with a descriptive error. Processors MUST warn users before executing any procedure from a bundle lacking a valid `bundle.sig`.

> **Note (informative):** Processors running in edge, serverless, or mobile environments may have native platform constraints that supersede or differ from the declared values. In such cases, the host platform's constraints take precedence and the processor need not treat the mismatch as an error.

### 6.5 Example `manifest.json`

The `mcp` block is an advisory manifest. Its presence does not require processors to serve MCP, and its absence does not prevent them. Processors hold final authority over whether and how to instantiate an MCP server for a bundle. See §15 for full field definitions.

```json
{
  "name": "Nutrition for Men",
  "version": "0.1.0",
  "spec": "1.0.0",
  "domain": "Health",
  "audience": "Adult men aged 18–65 seeking evidence-based nutrition guidance",
  "intended_use": "LLM context injection, RAG retrieval, agent grounding for nutrition Q&A",
  "known_limitations": "Does not cover clinical conditions, eating disorders, or pediatric nutrition",
  "update_date": "2026-06-21",
  "source_policy": "Peer-reviewed studies and government dietary guidelines published after 2020",
  "compatibility": ["OpenAI GPT-4o", "Anthropic Claude Sonnet 4.6"],
  "description": "Evidence-based nutrition guidance for adult men, covering macronutrients, micronutrients, meal planning, and common deficiencies.",
  "tags": ["nutrition", "health", "men", "diet", "macros"],
  "license": "Proprietary",
  "audience_profiles": [
    { "id": "consumer", "label": "General public" },
    { "id": "clinician", "label": "Licensed dietitian", "requires_role": "clinician" }
  ],
  "retrieval_hints": {
    "recommended_top_k": 8,
    "max_context_tokens": 12000,
    "use_reranker": true,
    "embedding_model": "text-embedding-3-large",
    "index_version": "2026-06-21"
  },
  "min_eval_delta": 0.15,
  "locales": ["en-US", "es-MX"],
  "publisher": {
    "name": "Example, Inc",
    "url": "https://dkp-standard.com",
    "pgp_fingerprint": "<fingerprint>",
    "signed": true
  },
  "access_control": {
    "classification": "public",
    "required_roles": [],
    "export_restrictions": [],
    "encryption_required": false,
    "pii_present": false,
    "gdpr_scope": false
  },
  "mcp": {
    "resource_server": {
      "uri_scheme": "dkp",
      "expose_eval_cases": false
    },
    "tool_provider": {
      "tools": ["inject", "search", "chunk", "get"],
      "auth": {
        "scheme": "none"
      }
    },
    "transport": "stdio"
  }
}
```

### 6.6 Audience-Scoped Conditional Content

When `audience_profiles` is declared in `manifest.json`, individual entries in machine-layer assets and OKF concept files MAY carry an `audience` field — an array of profile `id` values. Content without an `audience` field is visible to all profiles.

Processors performing audience-filtered export (`dkp export --audience <profile-id>`) MUST omit any entry that possesses an `audience` array if that array does not include the requested profile ID. Processors MUST NOT silently include restricted-audience content when an audience filter is active.

## 7. Conformance

### 7.1 Conformance Language

Conformance language (MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL) is defined in §2.1.

### 7.2 Conformance Targets

This specification defines four distinct conformance targets:

**DKP-Conformant Bundle** — A directory (or archive derived from it) that satisfies all MUST and MUST NOT requirements in §5–§6 and §9–§15 and passes Gates 4 and 8 of the quality standard (§16). This is the baseline structural conformance level verifiable by automated tooling (`dkp validate`). Gate 7 is skipped when `eval_set.jsonl` is absent; skipping Gate 7 does not disqualify a bundle from DKP-Conformant status.

**DKP-Evaluated Bundle** — A DKP-Conformant Bundle that additionally includes a populated `eval_set.jsonl` and successfully passes Gate 7 (§16), demonstrating measurable retrieval and generation utility above the `min_eval_delta` threshold.

**DKP-Reviewed Bundle** — A DKP-Evaluated Bundle that additionally satisfies the editorial quality requirements of Gates 1–3 and 5–6 (§16), as attested by a dated, named sign-off in `evidence/review_notes.md` (§12.3). A DKP-Reviewed Bundle is a strict superset of a DKP-Evaluated Bundle.

**Conformant DKP Processor** — A tool (CLI, library, agent integration) that reads, validates, converts, or evaluates DKP bundles and satisfies all MUST and MUST NOT requirements stated for processors in §5–§6 and §9–§15.

A bundle and a processor may independently conform or fail to conform. A processor that accepts non-conformant bundles is not itself non-conformant, provided it signals the non-conformance to the caller.

### 7.3 OKF Conformance

The `okf/` directory of a conformant DKP bundle MUST be a conformant OKF bundle as defined in [OKF SPEC.md](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Where this specification is silent, OKF requirements apply to the `okf/` layer.

## 8. Versioning

### 8.1 Specification Version

This specification uses Semantic Versioning 2.0.0.

- **PATCH** increments (e.g., 1.0.0 → 1.0.1): Clarifications, corrections, and editorial changes. No normative change.
- **MINOR** increments (e.g., 1.0.0 → 1.1.0): Backward-compatible additions. New OPTIONAL or RECOMMENDED fields; new SHOULD requirements. Existing conformant bundles remain conformant.
- **MAJOR** increments (e.g., 1.0.0 → 2.0.0): Breaking changes. New REQUIRED fields; removed fields; changed field semantics.

### 8.2 Bundle Version

`manifest.json` `version` MUST be a Semantic Versioning 2.0.0 string. Bundle version represents the content version of the pack, not the DKP specification version.

- **PATCH**: Minor content corrections, updated `update_date`, no schema changes
- **MINOR**: New concepts added, new evaluation cases added, source list expanded
- **MAJOR**: Domain scope change, structural restructure of the bundle's content organization, audience change, or source rights expiry requiring removal of chunks (see §12.2). **Important:** Bundle versioning MUST NOT be used to bypass schema validation. If a structural restructure violates the normative JSON schemas declared in Appendix B for the bundle's declared `spec` version, the bundle fails Gate 4 and is invalid. Modifying the normative schemas requires adopting a new DKP Specification version, not just incrementing the bundle version.

### 8.3 Processor Version Handling

Processors MUST attempt to parse any bundle whose `manifest.json` is valid JSON and contains all REQUIRED fields. Processors MUST read the `spec` field to determine the specification version the bundle was produced against. Processors SHOULD warn when `spec` identifies a version older than the processor's supported version, and SHOULD warn (but MUST NOT reject) when `spec` identifies a newer version.

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

## 10. OKF Layer

The `okf/` directory is a fully OKF-conformant bundle, generated from the machine layer. It is the distribution format for agent frameworks that natively support OKF.

### 10.1 DKP Type Taxonomy

The DKP Type Taxonomy is defined in §4. All concept files in the `okf/` layer MUST use one of the seven types defined there.

### 10.2 Required OKF Files

| File | Required | Description |
|---|---|---|
| `okf/index.md` | REQUIRED | Bundle description per OKF §7. MUST include YAML frontmatter. |
| `okf/log.md` | RECOMMENDED | Export history per OKF §8. SHOULD contain one `[EXPORT]` entry per export operation. |

### 10.3 DKP Frontmatter Extensions

All DKP concept files MUST include the following YAML frontmatter fields, in addition to OKF's required `type` field. The bundle version is declared once in `manifest.json` and is not repeated in individual concept files.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | REQUIRED (OKF) | One of the seven DKP types defined in §4 |
| `title` | string | REQUIRED | Human-readable title of this concept |
| `description` | string | REQUIRED | One-sentence description |
| `tags` | array of strings | REQUIRED | Non-empty list of tags |
| `timestamp` | string | REQUIRED | ISO 8601 datetime of last modification (e.g., `2026-06-21T00:00:00Z`) |
| `dkp_domain` | string | RECOMMENDED | Matches `manifest.json` `domain` field |
| `dkp_pack` | string | RECOMMENDED | Matches `manifest.json` `name` field |
| `source_ref` | string | RECOMMENDED | `id` of a record in `evidence/sources.csv` |
| `confidence` | number | OPTIONAL | `[0.0, 1.0]`. Used only on `KnowledgeChunk` type files. |
| `ttl_days` | integer | OPTIONAL | Days until this concept file should be reviewed for staleness |
| `review_date` | string | OPTIONAL | ISO 8601 date for next review |
| `stability` | string | OPTIONAL | One of `"stable"`, `"volatile"`, `"experimental"` |
| `audience` | array of strings | OPTIONAL | Audience profile IDs from `manifest.json`. If absent, visible to all profiles. |
| `asset_refs` | array of strings | OPTIONAL | Asset `id` values from `machine/assets.json` associated with this concept |

Processors validating the OKF layer MUST treat missing REQUIRED frontmatter fields as errors. Processors MUST NOT reject concept files with additional unknown fields (per OKF conformance). When `dkp_domain` or `dkp_pack` is absent from a concept file, processors MUST infer the missing value(s) from `manifest.json` (`domain` and `name` respectively) rather than treating the absence as an error.

Producers MUST quote ISO 8601 datetime values in YAML frontmatter (e.g., `timestamp: "2026-06-21T00:00:00Z"`) to prevent YAML 1.2 parsers from resolving them into native Date objects. Unquoted datetime values that cause parser-level type coercion are a common source of schema validation failures in standard tooling. Processors MUST normalize any native Date object produced by YAML parsing into an ISO 8601 string before validating the frontmatter against the Appendix B.8 schema.

### 10.4 Cross-Links

Concept files SHOULD cross-link related concepts using OKF-conformant relative links. All relative links within the `okf/` directory MUST resolve to existing files within the same bundle. Processors performing OKF validation MUST flag broken relative links as errors.

### 10.5 OKF Subdirectory Conventions

Concept files SHOULD be organized by type in subdirectories. The following layout is RECOMMENDED:

| Directory | Contains |
|---|---|
| `okf/terms/` | `DomainTerm` concept files |
| `okf/rules/` | `DomainRule` concept files |
| `okf/constraints/` | `Constraint` concept files |
| `okf/procedures/` | `DecisionProcedure` concept files |
| `okf/chunks/` | `KnowledgeChunk` concept files |
| `okf/ontology/` | `EntityType` concept files |

Processors MUST NOT require this layout. Processors MAY use it as a hint for type inference.

### 10.6 Example Concept File

```markdown
---
type: DomainTerm
title: Protein Synthesis
description: The cellular process by which amino acids are assembled into proteins using mRNA as a template.
tags: [protein, metabolism, biochemistry, muscle]
timestamp: "2026-06-21T00:00:00Z"
dkp_domain: Health
dkp_pack: Nutrition for Men
source_ref: src-007
stability: stable
ttl_days: 730
---

# Protein Synthesis

The process by which cells build proteins from amino acids, directed by messenger RNA (mRNA) transcribed from DNA.

## Relevance

For nutrition purposes, dietary protein provides the amino acid substrates required for protein synthesis. Adequate intake is required for muscle repair, enzyme production, and immune function.

## See Also

- [Essential Amino Acids](../terms/essential-amino-acids.md)
- [Muscle Protein Turnover](../terms/muscle-protein-turnover.md)
```

## 11. Human Layer

The `human/` directory contains human-readable companion materials. This layer is RECOMMENDED for packs intended for commercial distribution but is not required for conformance.

The `human/` layer is loosely specified by design. Producers MAY include any materials that serve human readers of the domain, provided each file is valid Markdown (or a rendering of a Markdown source). All files in `human/` MUST NOT contradict the domain rules and constraints in the machine layer.

### 11.1 `human/handbook.md` (Recommended)

A comprehensive prose reference covering the pack's full domain scope, suitable for a practitioner to read and use independently of any AI tooling.

If present:

- MUST be valid Markdown
- SHOULD cover the same knowledge scope as the machine layer
- SHOULD include practical examples and checklists

### 11.2 `human/handbook.pdf` and `human/handbook.epub` (Optional)

PDF and EPUB renderings of `human/handbook.md`. If present, they MUST be derived from the same content as `handbook.md` and SHOULD be regenerated whenever `handbook.md` changes.

### 11.3 `human/quickstart.md` (Optional)

A short (one to three page) getting-started guide aimed at a reader who needs to be productive within minutes. SHOULD cover the most common use cases and point to the handbook for depth.

### 11.4 `human/cheatsheet.md` (Optional)

A single-page scannable reference — key terms, rules, thresholds, or decision shortcuts — suitable for printing or keeping open alongside a workflow. SHOULD be structured as tables or short lists, not prose paragraphs.

### 11.5 `human/faq.md` (Optional)

A question-and-answer document addressing common misunderstandings, edge cases, or frequently asked questions in the domain. SHOULD mirror the kinds of queries in `machine/eval_set.jsonl` where applicable.

### 11.6 `human/examples/` (Optional)

A directory of worked examples showing the domain knowledge applied to realistic scenarios. Each file SHOULD be a self-contained Markdown document with a clear scenario, the reasoning applied, and the outcome. Files MAY reference machine-layer concepts by name.

---

## 12. Evidence Layer

The `evidence/` directory documents the provenance, rights, and review history of pack content. All required evidence files MUST be present and non-empty.

### 12.1 `evidence/sources.csv`

A CSV file with a header row and one data row per information source used in pack generation.

**Required columns (header row MUST contain at least these columns; column order is not significant; additional producer-defined columns are permitted):**

| Column | Type | Description |
|---|---|---|
| `id` | string | Unique source identifier (e.g., `src-001`). Referenced by `source_ref` fields throughout the pack. |
| `title` | string | Title of the source document or resource |
| `url` | string | URL or DOI. Use `N/A` for offline-only sources. |
| `retrieved_date` | string | ISO 8601 date the source was accessed |
| `license` | string | License of the source (e.g., `CC-BY-4.0`, `Public Domain`, `All Rights Reserved`) |
| `notes` | string | Any relevant notes about the source. MAY be empty. |

Processors MUST validate that the header row contains at least these six columns. Processors MUST validate that every `source_ref` value in the machine layer and OKF layer resolves to an `id` in `sources.csv`. Normative Frictionless Table Schema for `sources.csv`: see Appendix B §B.24. Processors MUST validate the header row and column types against this schema during Gate 4.

### 12.2 `evidence/rights_log.csv`

A CSV file tracking the rights status for each source used in the pack.

**Required columns (header row MUST contain at least these columns; column order is not significant; additional producer-defined columns are permitted):**

| Column | Type | Description |
|---|---|---|
| `id` | string | Unique rights record identifier |
| `source_id` | string | `id` from `sources.csv` this record applies to |
| `rights_holder` | string | Name of the rights holder |
| `license_type` | string | License type or grant (e.g., `Public Domain`, `CC-BY-4.0`, `Commercial License`) |
| `granted_date` | string | ISO 8601 date rights were confirmed or license granted |
| `expiry_date` | string | ISO 8601 date rights expire, or `perpetual` |
| `notes` | string | Any relevant notes. MAY be empty. |

Normative Frictionless Table Schema for `rights_log.csv`: see Appendix B §B.25. Processors MUST validate the header row and column types against this schema during Gate 4.

#### Source Expiry Lifecycle

When a source's `expiry_date` has passed, the producer SHOULD issue a major bundle version increment (§8.2) and SHOULD remove all `retrieval_chunks.jsonl` entries and `knowledge_graph.json` nodes whose `source_ref` resolves to that source. More generally, producers SHOULD remove all machine-layer asset entries — including entries in `glossary.json`, `rules.json`, `constraints.json`, and `assets.json` — whose `source_ref` field resolves to the expired source. The producer SHOULD also remove the corresponding `.md` concept files in `okf/` whose `source_ref` frontmatter field resolves to the expired source. Failure to prune the OKF layer alongside the machine layer will cause Gate 6 (Consistency) to fail, since the `okf/` layer would contain content derived from a source no longer covered by the evidence layer. The producer SHOULD revalidate `knowledge_graph.json` to ensure no dangling edges remain after removal (edges whose `from` or `to` no longer reference a node in the `nodes` array). The producer SHOULD also validate or prune the `skills/` layer — specifically, any `metadata.dkp_uses_chunks` arrays in `SKILL.md` frontmatter — to remove references to chunk IDs that were deleted, preventing dangling procedural references. If pruning `metadata.dkp_uses_chunks` removes chunks that are critical to a skill's execution, or leaves the array empty, the producer SHOULD remove or deprecate the entire `skills/{skill-name}/` directory to prevent agents from attempting to execute an orphaned procedure. The producer SHOULD also prune `cross_refs.json` — any entry whose `local_id` references a deleted chunk ID must be removed to prevent dangling cross-pack references in downstream packs that depend on this bundle. Performing expiry management at build time — rather than at retrieval time — preserves the structural integrity of the knowledge graph and produces a bundle that consumers can trust to be both legally current and graph-consistent.

Processors MUST NOT perform runtime license expiry enforcement against `rights_log.csv`. Expiry is a producer-side build-time concern; a processor has no obligation to check system time against `expiry_date` during retrieval. Processors SHOULD, however, emit a non-fatal warning to the caller when ingesting a bundle in which one or more sources have an `expiry_date` that has passed relative to the current date. This warning MUST NOT cause the processor to fail, alter graph topology, or refuse to load the bundle.

### 12.3 `evidence/review_notes.md`

A Markdown document recording editorial review observations, decisions, and quality notes for this pack version.

If present, `evidence/review_notes.md` SHOULD include:

- The date of review
- The reviewer identifier or role
- Any content decisions made (sources accepted or rejected, constraints added, etc.)
- Known gaps or areas for future improvement

**DKP-Reviewed sign-off.** To claim DKP-Reviewed status (§7.2, §16), `evidence/review_notes.md` MUST include a sign-off block with the following fields: the ISO 8601 date of the editorial review, the name or role of the reviewer, and an explicit attestation that Gates 1–3, 5, and 6 were evaluated and passed. Example:

```markdown
## Editorial Sign-Off

- **Review date:** 2026-06-21
- **Reviewer:** Jane Smith, Lead Knowledge Engineer
- **Gates attested:** 1 (Relevance), 2 (Originality), 3 (Utility), 5 (Human Usability), 6 (Consistency)
- **Status:** DKP-Reviewed
```

Processors checking for DKP-Reviewed status SHOULD parse `review_notes.md` for the presence of a sign-off block and report its presence or absence as informational output.

### 12.4 `evidence/eval_results/` (Recommended)

A directory of evaluation run result files, enabling regression tracking across pack versions and model updates.

#### `eval_results/{date}-{model}.jsonl`

One result file per `dkp eval` run. Each line MUST be a valid JSON object:

| Field | Type | Required | Description |
|---|---|---|---|
| `query_hash` | string | REQUIRED | SHA-256 of the evaluated query string |
| `model` | string | REQUIRED | Model identifier used for this eval run |
| `pack_version` | string | REQUIRED | `version` from `manifest.json` at time of eval |
| `run_date` | string | REQUIRED | ISO 8601 datetime of the eval run |
| `with_pack_score` | number | REQUIRED | Float `[0.0, 1.0]`. Score achieved with this pack injected |
| `baseline_score` | number | REQUIRED | Float `[0.0, 1.0]`. Score achieved without pack (baseline prompt only) |
| `delta` | number | REQUIRED | `with_pack_score` minus `baseline_score` |
| `dimensions_met` | array of strings | REQUIRED | `expected_dimensions` from the eval case that were satisfied |
| `dimensions_missed` | array of strings | REQUIRED | `expected_dimensions` that were not satisfied |

#### `eval_results/eval_summary.json`

An aggregated summary object updated after each eval run. Normative JSON Schema: see Appendix B §B.13.

| Field | Type | Description |
|---|---|---|
| `last_run_date` | string | ISO 8601 datetime of most recent run |
| `pack_version` | string | Pack version at last run |
| `model` | string | Model at last run |
| `mean_delta` | number | Mean `delta` across all eval cases |
| `pass_rate` | number | Fraction of cases where `delta >= manifest.min_eval_delta` |
| `gate7_pass` | boolean | Whether this run passed Gate 7 |

Processors running `dkp eval` MUST support writing result files and the updated `eval_summary.json` to `stdout` (as newline-delimited JSON) or to a user-specified directory via `--output <dir>`. Processors SHOULD also write results to `evidence/eval_results/` when the bundle directory is writable, but MUST NOT hard-fail when the bundle is read-only (e.g., loaded from a `.zip` archive, a read-only container volume, or remote blob storage).

**DKP-Evaluated status.** A bundle achieves DKP-Evaluated status (§7.2, §16) when `eval_results/eval_summary.json` is present and its `gate7_pass` field is `true` with a `mean_delta` at or above `manifest.min_eval_delta` (default `0.0` when absent). Processors running `dkp eval` MUST set `gate7_pass: true` only when this threshold is met. Processors checking for DKP-Evaluated status SHOULD read `eval_results/eval_summary.json` and report `gate7_pass` as the Gate 7 determination.

## 13. Skill Layer

The `skills/` directory is an OPTIONAL layer that bundles procedural knowledge alongside the declarative machine layer. Each skill is a directory of Markdown files describing how to perform a domain-specific task using the knowledge in this pack.

### 13.1 Purpose

DKP's machine layer is declarative — it describes what domain concepts are, what rules apply, and what constraints exist. The skill layer is procedural — it describes how an agent should act within the domain. The two are complementary: a "Nutrition for Men" DKP might bundle both the knowledge about protein synthesis (machine layer) and a skill for calculating a user's TDEE from their inputs (skill layer).

Skills in the `skills/` layer conform to the Agent Skills open standard (<https://agentskills.io>), which is supported by 32+ agent platforms as of mid-2026. Skills are Markdown-only: they consist of a `SKILL.md` instruction file and optional supporting Markdown, text, or static asset files. Executable code belongs exclusively in `machine/procedures/` (§9.12) and MUST NOT be placed in the `skills/` layer.

### 13.2 Structure

```
skills/
  {skill-name}/                [O]    One directory per bundled skill
    SKILL.md                   [R]    Agent Skills frontmatter + Markdown instructions
    references/                [O]    Additional Markdown context files loaded on demand
    assets/                    [O]    Static resources (templates, data files)
```

The directory name `{skill-name}` MUST match the `name` field in the skill's `SKILL.md` exactly (see §13.3).

### 13.3 `SKILL.md` Frontmatter

Each `SKILL.md` MUST conform to the Agent Skills specification (<https://agentskills.io/specification>). The standard defines the following fields:

| Field | Source | Required | Constraints | Description |
|---|---|---|---|---|
| `name` | Agent Skills | REQUIRED | Lowercase letters (`a-z`), digits (`0-9`), and hyphens (`-`) only. 1–64 characters. No leading, trailing, or consecutive hyphens. MUST match the parent directory name exactly. | Skill identifier |
| `description` | Agent Skills | REQUIRED | 1–1024 characters | What the skill does and when to use it. Should include keywords that help agents identify relevant tasks. |
| `license` | Agent Skills | OPTIONAL | — | License name or reference to a bundled license file |
| `compatibility` | Agent Skills | OPTIONAL | 1–500 characters | Environment requirements (intended product, system packages, network access) |
| `metadata` | Agent Skills | OPTIONAL | Arbitrary key-value map | Additional properties. DKP uses this map for pack-specific fields (see below). |
| `allowed-tools` | Agent Skills | OPTIONAL | Space-separated string | Pre-approved tools the skill may use. Support varies by agent implementation. |

DKP producers MUST place the following pack-specific fields inside the `metadata` map so that the `SKILL.md` remains a conformant Agent Skills file:

| Metadata key | Type | Required | Description |
|---|---|---|---|
| `dkp_pack` | string | REQUIRED | `name` from `manifest.json`. Links this skill to its parent bundle. |
| `dkp_uses_chunks` | array of strings | OPTIONAL | `id` values of `retrieval_chunks.jsonl` entries this skill relies on. Processors SHOULD warn when a referenced chunk ID does not exist in `retrieval_chunks.jsonl`. |
| `dkp_capability_requires` | array of strings | OPTIONAL | MCP tool names or agent capabilities required to execute this skill |
| `dkp_capability_mcp_servers` | array of strings | OPTIONAL | Fully-qualified MCP server URIs or server names that satisfy `dkp_capability_requires`. When absent, processors SHOULD attempt to resolve `dkp_capability_requires` values against any registered DKP MCP server for the parent bundle. |

**Example:**

```yaml
---
name: calculate-tdee
description: Calculates total daily energy expenditure from user-provided metrics. Use when the user asks about TDEE, calorie targets, or daily energy needs.
metadata:
  dkp_pack: nutrition-for-men
  dkp_uses_chunks:
    - chunk-tdee-001
    - chunk-macro-002
  dkp_capability_requires:
    - search
    - inject
  dkp_capability_mcp_servers:
    - "dkp://nutrition-for-men"
---

## Calculate TDEE

Step-by-step instructions for calculating TDEE...
```

When `dkp_capability_mcp_servers` references a `dkp://` URI matching the parent bundle, processors MAY start the bundle's own MCP server (`dkp serve`) to satisfy the declared requirements without requiring an external server.

### 13.4 Conformance

Processors that support the Agent Skills format MUST load skills from the `skills/` layer without modification. Processors that do not support Agent Skills MUST silently ignore the `skills/` directory.

Processors performing DKP validation MUST check each skill for:

- `name` is valid per Agent Skills naming rules (lowercase alphanumeric and hyphens only, 1–64 characters, no leading/trailing/consecutive hyphens)
- `name` matches the parent directory name exactly
- `description` is present and non-empty
- `metadata.dkp_pack` is present and matches `manifest.json` `name`
- All IDs listed in `metadata.dkp_uses_chunks` exist in `retrieval_chunks.jsonl` (when that file is present)
## 14. Localization Layer

The `l10n/` directory is an OPTIONAL layer providing translated or locale-adapted content for non-base locales. The base locale is `"en-US"` unless overridden by a `base_locale` field in `manifest.json`.

### 14.1 Structure

```
l10n/
  {locale}/              BCP 47 locale tag (e.g., es-MX, fr-FR, ja-JP)
    machine/
      glossary.json      Translated terms (same schema as machine/glossary.json)
      system_prompt.md   Locale-adapted system prompt
    okf/
      terms/             Translated OKF concept files with dkp_locale frontmatter
    human/
      handbook.md        Translated handbook
```

Within each `l10n/{locale}/` subdirectory, only `machine/glossary.json` and `machine/system_prompt.md` are RECOMMENDED. All other assets are OPTIONAL and inherit from the base pack when absent.

### 14.2 Locale Frontmatter

OKF concept files in `l10n/{locale}/okf/` MUST include all required DKP frontmatter (§10.3) plus:

| Field | Type | Required | Description |
|---|---|---|---|
| `dkp_locale` | string | REQUIRED | BCP 47 locale tag matching the parent `l10n/{locale}/` directory |

### 14.3 Conformance

`manifest.json` MUST list all supported locales in the `locales` array. Processors loading a locale-specific bundle SHOULD prefer content from `l10n/{locale}/` over base-pack content for matching locale tags, falling back to base-pack content when locale-specific content is absent. When a locale file in `l10n/{locale}/` contains relative Markdown links to targets that are not translated, producers MUST rewrite those links so they resolve relatively to components outside the localization directory (e.g., `../../okf/terms/concept.md`) rather than relative to the locale directory. Processors SHOULD treat the locale overlay as virtually merged onto the base bundle root when resolving such links, so that any remaining relative paths that were not rewritten still resolve correctly.

## 15. MCP Surface

This section defines how a DKP bundle declares its MCP surface configuration. Whether to serve a bundle over MCP is a **processor decision**. The `mcp` field in `manifest.json` is an advisory manifest — it declares how the bundle author recommends the pack be served, but it does not gate processor behavior. Processors that do not implement MCP MUST silently ignore the `mcp` field and `machine/mcp_manifest.json`.

### 15.1 DKP as an MCP Resource Server

A DKP bundle's machine-layer assets are mapped to MCP resources using the following URI scheme:

```
dkp://{pack-name}/{resource-type}/{resource-id}
```

`{pack-name}` is the `name` field from `manifest.json` with spaces replaced by hyphens and all characters lowercased.

**Note:** `dkp://` is a logical resource identifier, not a resolvable URL. When the MCP server uses HTTP transport, resources resolve at `http://localhost:{port}/resources/{pack-name}/...`. The `dkp://` URI is used as the canonical `uri` field in the MCP resource descriptor.

**Resource type mappings:**

| MCP Resource Type | DKP Asset | URI Pattern |
|---|---|---|
| `dkp/system-prompt` | `machine/system_prompt.md` | `dkp://{pack}/system-prompt` |
| `dkp/chunks` | `retrieval_chunks.jsonl` — listing or single entry | `dkp://{pack}/chunks{?cursor,limit}` (listing, returns IDs and titles only) or `dkp://{pack}/chunks/{id}` (single entry, returns full content) |
| `dkp/terms` | `glossary.json` entry | `dkp://{pack}/terms/{id}` |
| `dkp/rules` | `rules.json` entry | `dkp://{pack}/rules/{id}` |
| `dkp/constraints` | `constraints.json` entry | `dkp://{pack}/constraints/{id}` |
| `dkp/eval-cases` | `eval_set.jsonl` entry | `dkp://{pack}/eval-cases/{hash}` |
| `dkp/graph` | `knowledge_graph.json` | `dkp://{pack}/graph` |
| `dkp/entity-types` | `ontology.json` entry | `dkp://{pack}/entity-types/{id}` |
| `dkp/decision-trees` | `decision_trees.json` entry | `dkp://{pack}/decision-trees/{id}` |

Retrieval chunks use a **two-level pattern**: the listing URI (`dkp://{pack}/chunks{?cursor,limit}`) returns an array of `{id, title, token_count}` objects only; full chunk content is fetched per-ID. This prevents serving large JSONL payloads in a single resource response.

For packs with large chunk counts, the listing endpoint SHOULD support optional `cursor` (string) and `limit` (integer) query parameters. The `cursor` value MUST be treated as an opaque string token (e.g., a base64-encoded page token or stringified ID); processors MUST NOT assume it is an integer or attempt numeric comparison. When pagination is supported, the response SHOULD include a `next_cursor` field (string or `null`). When `next_cursor` is `null`, all chunks have been listed. When `cursor` and `limit` are absent, processors MUST return all IDs and titles in a single response. Servers MUST NOT crash or return an unhandled error when an invalid or expired `cursor` value is provided; they MUST instead return an empty results array with `next_cursor: null`, or return a standardized MCP error response indicating the cursor is invalid.

`dkp/eval-cases` resources are served only when `manifest.json` `mcp.resource_server.expose_eval_cases` is `true`.

All resources are **read-only**. Processors MUST NOT expose write operations over MCP for DKP bundle content.

Every resource response MUST be wrapped in the standard DKP resource response envelope (Appendix B §B.21):

```json
{
  "pack": "Nutrition for Men",
  "pack_version": "0.1.0",
  "resource_type": "chunks",
  "resource_id": "chunk-001",
  "content": { },
  "retrieval_metadata": {
    "score": null,
    "retrieved_at": "2026-06-21T12:00:00Z"
  }
}
```

### 15.2 DKP as an MCP Tool Provider

A conformant processor MAY expose the following MCP tools when operating as an MCP server.

| MCP Tool Name | Equivalent CLI | Description |
|---|---|---|
| `inject` | `dkp inject` | Return a formatted context block from the pack for injection into an LLM prompt |
| `search` | `dkp search` | BM25 full-text search over all machine-layer assets; returns ranked results |
| `chunk` | `dkp chunk` | Retrieve a specific retrieval chunk by ID |
| `get` | `dkp get` | Fetch assets from the pack by type, optionally filtered by ID or title |
| `list_procedures` | `dkp procedures list` | List available WASM procedures (only exposed when the pack has procedures) |
| `run_procedure` | `dkp run` | Execute a WASM procedure by ID (only exposed when the pack has procedures) |

`inject` accepts three optional parameters: `scope` (string, default `"system-prompt"`, enum: `system-prompt|full|minimal|chunks`) controls what content is included; `format` (string, default `"markdown"`, enum: `markdown|xml|json`) controls the wrapping format; `max_tokens` (integer) caps the token budget. See Appendix B §B.15 for the full input schema.

`list_procedures` and `run_procedure` are only exposed by processors when the pack contains at least one procedure definition (`machine/procedures/`).

Tool input and output schemas MUST conform to JSON Schema Draft 2020-12. Normative schemas for each tool are defined in Appendix B §B.15–B.20.

Processors MUST NOT expose a tool that is not listed in `manifest.json` `mcp.tool_provider.tools` (when that field is present). When `mcp.tool_provider.tools` is absent, processors MAY expose all tools listed above.

### 15.3 `mcp` field in `manifest.json`

The `mcp` field is an OPTIONAL top-level field in `manifest.json`. All fields are OPTIONAL. When absent, processors MAY still serve the bundle over MCP using default behavior.

**Schema:**

```json
{
  "mcp": {
    "resource_server": {
      "uri_scheme": "dkp",
      "expose_eval_cases": false
    },
    "tool_provider": {
      "tools": ["inject", "search", "chunk", "get"],
      "auth": {
        "scheme": "none"
      }
    },
    "transport": "stdio"
  }
}
```

**Field definitions:**

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `resource_server.uri_scheme` | string | OPTIONAL | `"dkp"` | URI scheme for resource identifiers |
| `resource_server.expose_eval_cases` | boolean | OPTIONAL | `false` | Whether `dkp/eval-cases` resources are served |
| `tool_provider.tools` | array of strings | OPTIONAL | all tools | MCP tool names to expose. If absent, all tools in §15.2 are exposed. |
| `tool_provider.auth.scheme` | string | OPTIONAL | `"none"` | `"none"`, `"bearer"`, or `"oauth2"` |
| `tool_provider.auth.oauth2` | object | CONDITIONAL | — | REQUIRED when `scheme` is `"oauth2"`. Contains `authorization_url`, `token_url`, `scopes`. |
| `transport` | string | OPTIONAL | `"stdio"` | `"stdio"` or `"http"` |

When `tool_provider.auth.scheme` is `"oauth2"`, the `auth.oauth2.scopes` array SHOULD include all values present in `access_control.mcp_scopes_required` (§6.4). This creates a binding between the bundle's policy declaration and the MCP enforcement mechanism.

**Conformance:** Processors SHOULD respect the `mcp` field as advisory configuration. Processors MUST NOT expose a tool not listed in `mcp.tool_provider.tools` when that field is present (§15.2). Processors SHOULD NOT serve `dkp/eval-cases` resources unless `mcp.resource_server.expose_eval_cases` is `true`. Processors SHOULD use the declared `transport` and `auth` scheme when present.

### 15.4 `machine/mcp_manifest.json`

`machine/mcp_manifest.json` is an OPTIONAL machine-layer asset that pre-computes the full MCP server descriptor for the bundle. Processors MAY read this file at startup to avoid re-parsing all machine assets.

`machine/mcp_manifest.json` SHOULD be present when the bundle is intended for MCP serving. It MUST be regenerated whenever the bundle's machine-layer content changes.

**Schema (normative: see Appendix B §B.14):**

```json
{
  "schema_version": "1.0",
  "name": "Nutrition for Men",
  "pack_version": "0.1.0",
  "resources": [
    {
      "uri": "dkp://nutrition-for-men/system-prompt",
      "name": "System Prompt",
      "description": "Complete system prompt for Nutrition for Men DKP",
      "mime_type": "text/markdown"
    },
    {
      "uri": "dkp://nutrition-for-men/chunks",
      "name": "Retrieval Chunks — Listing",
      "description": "18 retrieval chunks. Returns IDs and titles only.",
      "mime_type": "application/json",
      "total_count": 18,
      "supports_pagination": true
    }
  ],
  "tools": [
    {
      "name": "search",
      "description": "Full-text BM25 search across all machine-layer assets",
      "inputSchema": { "$ref": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_search.json" }
    }
  ],
  "generated_at": "2026-06-21T00:00:00Z"
}
```

Producers SHOULD generate this file using `dkp mcp-manifest`. Processors SHOULD validate this file against the schema in Appendix B §B.14 as part of Gate 4 (Machine Usability) when the bundle's `mcp` block is present.

### 15.5 MCP Protocol Version

Processors implementing MCP serving MUST implement MCP protocol version `2024-11-05` as the minimum baseline. Processors SHOULD implement later stable versions when available.

For `transport: "http"`, processors SHOULD support the HTTP+SSE transport defined in the MCP specification. For `transport: "stdio"`, processors MUST use the stdio transport.

## 16. The 8-Gate Quality Standard

The DKP quality standard defines three conformance tiers built from 8 quality gates. The authoritative definitions of these tiers are in §7.2. The summaries below restate the gate-based criteria for reference alongside the gate table.

**DKP-Conformant** — Passes Gates 4 and 8. Gate 7 is skipped (not failed) when `eval_set.jsonl` is absent; skipping Gate 7 does not disqualify a bundle from this tier. A processor running `dkp validate` MUST check Gates 4 and 8 fully and MUST report Gate 7 as skipped (not failed) when `eval_set.jsonl` is absent.

**DKP-Evaluated** — A DKP-Conformant bundle that additionally passes Gate 7 (includes a populated `eval_set.jsonl` and a passing `eval_results/eval_summary.json`). Full Gate 7 evaluation (running a live LLM comparison via `dkp eval`) is OPTIONAL for DKP-Conformant status.

**DKP-Reviewed** — A DKP-Evaluated bundle that additionally satisfies Gates 1–3, 5, and 6, as evidenced by a dated, named sign-off in `evidence/review_notes.md` (§7.3). Processors SHOULD report Reviewed/Not-Reviewed as an informational signal; this does not affect the DKP-Conformant or DKP-Evaluated determination.

| Gate | Name | What Is Checked | Tier | Automated |
|---|---|---|---|---|
| 1 | Relevance | Pack solves a specific operational problem for a defined user type (audience field is non-generic) | Reviewed | No |
| 2 | Originality | Content is not a thin rewrite of generic public web content; adds distillation value | Reviewed | No |
| 3 | Utility | Machine layer contains executable decision logic, realistic constraints, and representative retrieval chunks | Reviewed | No |
| 4 | Machine Usability | All machine-layer files are valid, parseable, and pass schema validation (§9); `knowledge_graph.json` (defined in §9.9) edges resolve (if `knowledge_graph.json` is present); `knowledge_graph.json` `nodes` array entries resolve to valid concept IDs in machine-layer assets (ghost node check); `cross_refs.json` (defined in §9.13) references declared dependencies; `cross_refs.json` `local_id` values resolve to existing concepts in this bundle; if `assets.json` (defined in §9.11) is present, all `path` values MUST resolve to existing files in `machine/assets/`; `evidence/sources.csv` and `evidence/rights_log.csv` header rows and column types conform to Frictionless Table Schemas (Appendix B §B.24–B.25) | Conformant | **Yes** |
| 5 | Human Usability | `human/handbook.md` (if present) is readable and practically actionable by a non-technical reader | Reviewed | No |
| 6 | Consistency | Terminology and constraints in the machine layer are consistent with the OKF layer; no contradictions; `l10n/` content does not contradict the base pack; `okf/` layer does not contain concept files derived from expired sources | Reviewed | No |
| 7 | Evaluation | `eval_set.jsonl` (defined in §9.8) is present and non-empty; `eval_results/eval_summary.json` (defined in §9.8) shows `gate7_pass: true`; measured `mean_delta >= manifest.min_eval_delta` (default `0.0` when field is absent). If `eval_set.jsonl` is absent, this gate is **skipped** (not failed). Bundles that skip this gate achieve DKP-Conformant status but cannot achieve DKP-Evaluated status. | Evaluated | **Yes (partial)** |
| 8 | OKF Conformance | All `okf/` concept files have valid DKP frontmatter; all normatively REQUIRED fields present (RECOMMENDED fields such as `dkp_pack` and `dkp_domain` that are absent are inferred per §10.3 and do not fail this gate); all relative links resolve; `bundle.sig` (if present) verifies against declared publisher fingerprint | Conformant | **Yes** |

## Appendix A — Complete Bundle Example

The following is an illustrative minimal conformant DKP bundle. Content is abbreviated for clarity.

**`manifest.json`**

```json
{
  "name": "Nutrition for Men",
  "version": "0.1.0",
  "spec": "1.0.0",
  "domain": "Health",
  "audience": "Adult men aged 18–65",
  "intended_use": "LLM context injection and RAG for nutrition Q&A",
  "known_limitations": "Does not cover clinical conditions or pediatric nutrition",
  "update_date": "2026-06-21",
  "source_policy": "Peer-reviewed studies published after 2020",
  "compatibility": ["Anthropic Claude Sonnet 4.6"],
  "license": "Proprietary",
  "audience_profiles": [
    { "id": "consumer", "label": "General public" },
    { "id": "clinician", "label": "Licensed dietitian", "requires_role": "clinician" }
  ],
  "retrieval_hints": {
    "recommended_top_k": 8,
    "max_context_tokens": 12000,
    "use_reranker": true
  },
  "min_eval_delta": 0.15,
  "publisher": {
    "name": "Example, Inc",
    "signed": true
  },
  "access_control": {
    "classification": "public",
    "pii_present": false
  }
}
```

> **Note on `signed: true`:** This field asserts the producer's intent to sign the bundle. A verifiable signed bundle additionally requires `pgp_fingerprint` in the `publisher` object and a `bundle.sig` file at the bundle root (§6.4). This minimal example omits both because it demonstrates bundle structure, not a production-signed release.

**`machine/retrieval_chunks.jsonl`** (one line)

```json
{"id": "chunk-001", "title": "Daily Protein Requirement for Adult Men", "chunk_text": "Adult men require approximately 0.8–1.6 g of protein per kg of body weight per day, depending on activity level. Sedentary men should target the lower bound; resistance-training men should target 1.2–1.6 g/kg.", "tags": ["protein", "macronutrients", "daily-intake"], "source_ref": "src-001", "confidence": 0.92, "retrieval_priority": "high", "stability": "stable", "ttl_days": 730}
```

**`machine/knowledge_graph.json`** (abbreviated)

```json
{
  "nodes": [
    { "id": "chunk-001", "type": "KnowledgeChunk" },
    { "id": "term-protein-synthesis", "type": "DomainTerm" }
  ],
  "edges": [
    { "from": "chunk-001", "to": "term-protein-synthesis", "relation": "elaborates", "weight": 0.85 }
  ]
}
```

**`okf/terms/protein-requirement.md`**

```markdown
---
type: DomainTerm
title: Daily Protein Requirement
description: The amount of dietary protein an adult man requires per day, expressed per kg of body weight.
tags: [protein, macronutrients, daily-intake]
timestamp: "2026-06-21T00:00:00Z"
dkp_domain: Health
dkp_pack: Nutrition for Men
source_ref: src-001
stability: stable
ttl_days: 730
---

# Daily Protein Requirement

Adult men: 0.8–1.6 g/kg body weight per day. See [Muscle Protein Turnover](../terms/muscle-protein-turnover.md).
```

**`evidence/sources.csv`**

```csv
id,title,url,retrieved_date,license,notes
src-001,WHO Protein Requirements Report,https://www.who.int/nutrition/publications/nutrientrequirements/9241209130/en/,2026-06-01,Public Domain,""
```

**`evidence/rights_log.csv`**

```csv
id,source_id,rights_holder,license_type,granted_date,expiry_date,notes
rr-001,src-001,World Health Organization,Public Domain,2026-06-01,perpetual,""
```

## Appendix B — JSON Schemas (Normative)

The schemas in this appendix are normative. Conformant DKP bundles MUST produce assets that validate against these schemas. Conformant processors MUST reject assets that fail validation.

Schemas use [JSON Schema Draft 2020-12](https://json-schema.org/specification).

### B.1 `ontology.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/ontology.json",
  "title": "DKP Ontology",
  "type": "object",
  "required": [
    "entity_types"
  ],
  "properties": {
    "entity_types": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "name",
          "description",
          "attributes"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "name": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "attributes": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "relationships": {
            "type": "array",
            "items": {
              "type": "object",
              "required": [
                "name",
                "target_type"
              ],
              "properties": {
                "name": {
                  "type": "string"
                },
                "target_type": {
                  "type": "string"
                },
                "cardinality": {
                  "type": "string",
                  "enum": [
                    "one-to-one",
                    "one-to-many",
                    "many-to-many"
                  ]
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### B.2 `glossary.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/glossary.json",
  "title": "DKP Glossary",
  "type": "object",
  "required": [
    "terms"
  ],
  "properties": {
    "terms": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "term",
          "definition"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "term": {
            "type": "string",
            "minLength": 1
          },
          "definition": {
            "type": "string",
            "minLength": 1
          },
          "aliases": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "related_terms": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "source_ref": {
            "type": "string"
          },
          "ttl_days": {
            "type": "integer",
            "minimum": 1
          },
          "review_date": {
            "type": "string",
            "format": "date"
          },
          "stability": {
            "type": "string",
            "enum": [
              "stable",
              "volatile",
              "experimental"
            ]
          },
          "audience": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    }
  }
}
```

### B.3 `constraints.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/constraints.json",
  "title": "DKP Constraints",
  "type": "object",
  "required": [
    "edge_cases",
    "anti_patterns",
    "hard_limits"
  ],
  "properties": {
    "edge_cases": {
      "$ref": "#/$defs/constraintArray"
    },
    "anti_patterns": {
      "$ref": "#/$defs/constraintArray"
    },
    "hard_limits": {
      "$ref": "#/$defs/constraintArray"
    }
  },
  "$defs": {
    "constraintArray": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "title",
          "description"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "title": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "source_ref": {
            "type": "string"
          },
          "ttl_days": {
            "type": "integer",
            "minimum": 1
          },
          "review_date": {
            "type": "string",
            "format": "date"
          },
          "stability": {
            "type": "string",
            "enum": [
              "stable",
              "volatile",
              "experimental"
            ]
          },
          "audience": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    }
  }
}
```

### B.4 `rules.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/rules.json",
  "title": "DKP Rules",
  "type": "object",
  "required": [
    "rules"
  ],
  "properties": {
    "rules": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "id",
          "title",
          "description",
          "polarity"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "title": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "polarity": {
            "type": "string",
            "enum": [
              "affirmative",
              "prohibitive"
            ]
          },
          "source_ref": {
            "type": "string"
          },
          "ttl_days": {
            "type": "integer",
            "minimum": 1
          },
          "review_date": {
            "type": "string",
            "format": "date"
          },
          "stability": {
            "type": "string",
            "enum": [
              "stable",
              "volatile",
              "experimental"
            ]
          },
          "audience": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    }
  },
  "allOf": [
    {
      "properties": {
        "rules": {
          "contains": {
            "properties": {
              "polarity": {
                "const": "affirmative"
              }
            }
          }
        }
      }
    },
    {
      "properties": {
        "rules": {
          "contains": {
            "properties": {
              "polarity": {
                "const": "prohibitive"
              }
            }
          }
        }
      }
    }
  ]
}
```

### B.5 `decision_trees.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/decision_trees.json",
  "title": "DKP Decision Trees",
  "type": "object",
  "required": [
    "trees"
  ],
  "properties": {
    "trees": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "title",
          "description",
          "root"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "title": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "minLength": 1
          },
          "root": {
            "$ref": "#/$defs/node"
          }
        }
      }
    }
  },
  "$defs": {
    "node": {
      "type": "object",
      "required": [
        "question"
      ],
      "properties": {
        "question": {
          "type": "string",
          "minLength": 1
        }
      },
      "oneOf": [
        {
          "required": [
            "answer"
          ],
          "properties": {
            "answer": {
              "type": "string",
              "minLength": 1
            }
          },
          "not": {
            "required": [
              "branches"
            ]
          }
        },
        {
          "required": [
            "branches"
          ],
          "properties": {
            "branches": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "object",
                "required": [
                  "condition",
                  "next"
                ],
                "properties": {
                  "condition": {
                    "type": "string"
                  },
                  "next": {
                    "$ref": "#/$defs/node"
                  }
                }
              }
            }
          },
          "not": {
            "required": [
              "answer"
            ]
          }
        }
      ]
    }
  }
}
```

### B.6 `retrieval_chunks.jsonl` Line Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/retrieval_chunk.json",
  "title": "DKP Retrieval Chunk",
  "type": "object",
  "required": [
    "id",
    "title",
    "chunk_text",
    "tags",
    "source_ref"
  ],
  "properties": {
    "id": {
      "type": "string",
      "minLength": 1
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "chunk_text": {
      "type": "string",
      "minLength": 1
    },
    "tags": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "source_ref": {
      "type": "string",
      "minLength": 1
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "summary": {
      "type": "string",
      "minLength": 1
    },
    "embedding_model": {
      "type": "string",
      "minLength": 1
    },
    "token_count": {
      "type": "integer",
      "minimum": 1
    },
    "retrieval_priority": {
      "type": "string",
      "enum": [
        "critical",
        "high",
        "normal",
        "low"
      ]
    },
    "asset_refs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "ttl_days": {
      "type": "integer",
      "minimum": 1
    },
    "review_date": {
      "type": "string",
      "format": "date"
    },
    "stability": {
      "type": "string",
      "enum": [
        "stable",
        "volatile",
        "experimental"
      ]
    },
    "audience": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

### B.7 `eval_set.jsonl` Line Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/eval_entry.json",
  "title": "DKP Eval Entry",
  "type": "object",
  "required": [
    "query",
    "expected_dimensions",
    "critical_must_include",
    "scoring_rubric",
    "version_meta"
  ],
  "properties": {
    "query": {
      "type": "string",
      "minLength": 1
    },
    "expected_dimensions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "critical_must_include": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "scoring_rubric": {
      "type": "string",
      "minLength": 1
    },
    "version_meta": {
      "type": "object",
      "required": [
        "prompt_hash",
        "model_version",
        "dataset_version"
      ],
      "properties": {
        "prompt_hash": {
          "type": "string",
          "minLength": 1
        },
        "model_version": {
          "type": "string",
          "minLength": 1
        },
        "dataset_version": {
          "type": "string",
          "minLength": 1
        }
      }
    }
  }
}
```

### B.8 OKF Concept File Frontmatter Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/concept_frontmatter.json",
  "title": "DKP OKF Concept Frontmatter",
  "type": "object",
  "required": [
    "type",
    "title",
    "description",
    "tags",
    "timestamp"
  ],
  "properties": {
    "type": {
      "type": "string",
      "enum": [
        "DomainTerm",
        "DomainRule",
        "Constraint",
        "DecisionProcedure",
        "KnowledgeChunk",
        "EntityType",
        "EvalCase"
      ]
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "description": {
      "type": "string",
      "minLength": 1
    },
    "tags": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "dkp_domain": {
      "type": "string",
      "minLength": 1
    },
    "dkp_pack": {
      "type": "string",
      "minLength": 1
    },
    "source_ref": {
      "type": "string"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "ttl_days": {
      "type": "integer",
      "minimum": 1
    },
    "review_date": {
      "type": "string",
      "format": "date"
    },
    "stability": {
      "type": "string",
      "enum": [
        "stable",
        "volatile",
        "experimental"
      ]
    },
    "audience": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "asset_refs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "dkp_locale": {
      "type": "string"
    }
  },
  "if": {
    "properties": {
      "type": {
        "const": "KnowledgeChunk"
      }
    }
  },
  "then": {},
  "else": {
    "properties": {
      "confidence": false
    }
  }
}
```

### B.9 `knowledge_graph.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/knowledge_graph.json",
  "title": "DKP Knowledge Graph",
  "type": "object",
  "required": [
    "nodes",
    "edges"
  ],
  "properties": {
    "nodes": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "type"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "type": {
            "type": "string",
            "enum": [
              "DomainTerm",
              "DomainRule",
              "Constraint",
              "DecisionProcedure",
              "KnowledgeChunk",
              "EntityType",
              "EvalCase"
            ]
          }
        }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "from",
          "to",
          "relation"
        ],
        "properties": {
          "from": {
            "type": "string",
            "minLength": 1
          },
          "to": {
            "type": "string",
            "minLength": 1
          },
          "relation": {
            "type": "string",
            "enum": [
              "requires",
              "contradicts",
              "elaborates",
              "supersedes",
              "part-of",
              "depends-on",
              "see-also",
              "measured-by",
              "defined-by",
              "specializes"
            ]
          },
          "weight": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
          }
        }
      }
    }
  }
}
```

### B.10 `taxonomy.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/taxonomy.json",
  "title": "DKP Taxonomy Alignment",
  "type": "object",
  "required": [
    "mappings"
  ],
  "properties": {
    "concept_scheme": {
      "type": "object",
      "properties": {
        "uri": {
          "type": "string"
        },
        "skos_type": {
          "type": "string"
        },
        "dc_title": {
          "type": "string"
        },
        "dc_creator": {
          "type": "string"
        }
      }
    },
    "mappings": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "dkp_id"
        ],
        "properties": {
          "dkp_id": {
            "type": "string",
            "minLength": 1
          },
          "skos_exactMatch": {
            "type": "string"
          },
          "skos_closeMatch": {
            "type": "string"
          },
          "schema_org_type": {
            "type": "string"
          },
          "wikidata": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### B.11 `assets.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/assets.json",
  "title": "DKP Assets",
  "type": "object",
  "required": [
    "assets"
  ],
  "properties": {
    "assets": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "type",
          "path",
          "source_ref"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "type": {
            "type": "string",
            "enum": [
              "image",
              "table",
              "audio",
              "video"
            ]
          },
          "path": {
            "type": "string",
            "minLength": 1
          },
          "source_ref": {
            "type": "string",
            "minLength": 1
          },
          "alt_text": {
            "type": "string",
            "minLength": 1
          },
          "caption": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "columns": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "transcript": {
            "type": "string"
          }
        },
        "allOf": [
          {
            "if": {
              "properties": {
                "type": {
                  "const": "image"
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "required": [
                "alt_text"
              ]
            }
          },
          {
            "if": {
              "properties": {
                "type": {
                  "const": "table"
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "required": [
                "columns"
              ]
            }
          },
          {
            "if": {
              "properties": {
                "type": {
                  "not": {
                    "const": "table"
                  }
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "properties": {
                "columns": false
              }
            }
          },
          {
            "if": {
              "properties": {
                "type": {
                  "not": {
                    "enum": [
                      "audio",
                      "video"
                    ]
                  }
                }
              },
              "required": [
                "type"
              ]
            },
            "then": {
              "properties": {
                "transcript": false
              }
            }
          }
        ]
      }
    }
  }
}
```

### B.12 `cross_refs.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/cross_refs.json",
  "title": "DKP Cross-Pack References",
  "type": "object",
  "required": [
    "cross_refs"
  ],
  "properties": {
    "cross_refs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "local_id",
          "remote_pack",
          "remote_id",
          "relation"
        ],
        "properties": {
          "local_id": {
            "type": "string",
            "minLength": 1
          },
          "remote_pack": {
            "type": "string",
            "minLength": 1
          },
          "remote_id": {
            "type": "string",
            "minLength": 1
          },
          "relation": {
            "type": "string",
            "enum": [
              "requires",
              "contradicts",
              "elaborates",
              "supersedes",
              "part-of",
              "depends-on",
              "see-also",
              "measured-by",
              "defined-by",
              "specializes"
            ]
          }
        }
      }
    }
  }
}
```

### B.13 `eval_results/eval_summary.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/eval_summary.json",
  "title": "DKP Eval Summary",
  "type": "object",
  "required": [
    "last_run_date",
    "pack_version",
    "model",
    "mean_delta",
    "pass_rate",
    "gate7_pass"
  ],
  "properties": {
    "last_run_date": {
      "type": "string",
      "format": "date-time"
    },
    "pack_version": {
      "type": "string"
    },
    "model": {
      "type": "string"
    },
    "mean_delta": {
      "type": "number",
      "minimum": -1.0,
      "maximum": 1.0
    },
    "pass_rate": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "gate7_pass": {
      "type": "boolean"
    }
  }
}
```

### B.14 `machine/mcp_manifest.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_manifest.json",
  "title": "DKP MCP Manifest",
  "type": "object",
  "required": [
    "schema_version",
    "name",
    "pack_version",
    "resources",
    "tools",
    "generated_at"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0"
    },
    "name": {
      "type": "string",
      "minLength": 1
    },
    "pack_version": {
      "type": "string",
      "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    },
    "resources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "uri",
          "name",
          "description",
          "mime_type"
        ],
        "properties": {
          "uri": {
            "type": "string",
            "minLength": 1
          },
          "name": {
            "type": "string",
            "minLength": 1
          },
          "description": {
            "type": "string"
          },
          "mime_type": {
            "type": "string"
          },
          "total_count": {
            "type": "integer",
            "minimum": 0
          },
          "supports_pagination": {
            "type": "boolean",
            "description": "Whether this listing resource supports cursor + limit query parameters."
          }
        }
      }
    },
    "tools": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "description",
          "inputSchema"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "inputSchema": {
            "type": "object"
          }
        }
      }
    },
    "generated_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

### B.15 `inject` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_inject.json",
  "title": "inject Tool Input",
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "enum": [
        "system-prompt",
        "full",
        "minimal",
        "chunks"
      ],
      "default": "system-prompt",
      "description": "Content scope to include in the context block."
    },
    "format": {
      "type": "string",
      "enum": [
        "markdown",
        "xml",
        "json"
      ],
      "default": "markdown",
      "description": "Wrapping format for the returned context block."
    },
    "max_tokens": {
      "type": "integer",
      "minimum": 1,
      "description": "Token budget cap for the returned content."
    }
  }
}
```

### B.16 `search` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_search.json",
  "title": "search Tool Input",
  "type": "object",
  "required": [
    "query"
  ],
  "properties": {
    "query": {
      "type": "string",
      "minLength": 1,
      "description": "Full-text search query (BM25)"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 10,
      "description": "Maximum number of results to return"
    },
    "asset_types": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "chunks",
          "terms",
          "rules",
          "constraints",
          "eval-cases",
          "assets",
          "entity-types",
          "decision-trees"
        ]
      },
      "description": "Asset types to include in search. If absent, searches all types."
    }
  }
}
```

### B.17 `chunk` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_chunk.json",
  "title": "chunk Tool Input",
  "type": "object",
  "required": [
    "id"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Chunk ID to retrieve"
    }
  }
}
```

### B.18 `get` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_get.json",
  "title": "get Tool Input",
  "type": "object",
  "required": [
    "asset_type"
  ],
  "properties": {
    "asset_type": {
      "type": "string",
      "enum": [
        "term",
        "rule",
        "chunk",
        "constraint",
        "entity",
        "eval",
        "graph",
        "cross-ref",
        "system-prompt"
      ],
      "description": "Asset type to retrieve"
    },
    "id": {
      "type": "string",
      "description": "Asset ID or title substring to filter by. Omit to get all assets of this type."
    },
    "by_id": {
      "type": "boolean",
      "default": false,
      "description": "When true, match id exactly instead of substring-matching on title."
    }
  }
}
```

### B.19 `list_procedures` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_list_procedures.json",
  "title": "list_procedures Tool Input",
  "type": "object",
  "properties": {}
}
```

### B.20 `run_procedure` Tool Input Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_tool_run_procedure.json",
  "title": "run_procedure Tool Input",
  "type": "object",
  "required": [
    "procedure_id"
  ],
  "properties": {
    "procedure_id": {
      "type": "string",
      "description": "Procedure ID (stem name, e.g. \"calculate-tdee\")"
    },
    "input": {
      "type": "object",
      "description": "JSON input passed to the procedure (default: {})"
    },
    "timeout_ms": {
      "type": "integer",
      "description": "Wall-clock timeout override in milliseconds"
    }
  }
}
```

### B.21 MCP Resource Response Envelope Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/mcp_response.json",
  "title": "DKP MCP Resource Response Envelope",
  "type": "object",
  "required": [
    "pack",
    "pack_version",
    "resource_type",
    "content",
    "retrieval_metadata"
  ],
  "properties": {
    "pack": {
      "type": "string",
      "description": "Pack name from manifest.json"
    },
    "pack_version": {
      "type": "string",
      "description": "Pack version from manifest.json"
    },
    "resource_type": {
      "type": "string",
      "description": "DKP resource type (\u00a716.1)"
    },
    "resource_id": {
      "type": "string",
      "description": "Resource ID. OPTIONAL for singleton resources."
    },
    "content": {
      "description": "The DKP asset payload. Schema varies by resource_type."
    },
    "next_cursor": {
      "type": [
        "string",
        "null"
      ],
      "description": "Pagination cursor for the next page of results. Present only on listing responses when pagination is supported. null when all results have been returned."
    },
    "retrieval_metadata": {
      "type": "object",
      "required": [
        "retrieved_at"
      ],
      "properties": {
        "score": {
          "type": [
            "number",
            "null"
          ],
          "description": "BM25 relevance score for search-driven retrievals. null for direct fetches."
        },
        "retrieved_at": {
          "type": "string",
          "format": "date-time",
          "description": "ISO-8601 timestamp of retrieval"
        }
      }
    }
  }
}
```

### B.22 `manifest.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/manifest.json",
  "title": "DKP Manifest",
  "type": "object",
  "required": [
    "spec",
    "name",
    "version",
    "domain",
    "audience",
    "intended_use",
    "known_limitations",
    "update_date",
    "compatibility"
  ],
  "properties": {
    "spec": {
      "type": "string",
      "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    },
    "name": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    },
    "domain": {
      "type": "string",
      "minLength": 1
    },
    "audience": {
      "type": "string",
      "minLength": 1
    },
    "intended_use": {
      "type": "string",
      "minLength": 1
    },
    "known_limitations": {
      "type": "string",
      "minLength": 1
    },
    "update_date": {
      "type": "string",
      "format": "date"
    },
    "source_policy": {
      "type": "string",
      "minLength": 1
    },
    "compatibility": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "description": {
      "type": "string"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "license": {
      "type": "string"
    },
    "audience_profiles": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id",
          "label"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "label": {
            "type": "string",
            "minLength": 1
          },
          "requires_role": {
            "type": "string"
          }
        }
      }
    },
    "retrieval_hints": {
      "type": "object",
      "properties": {
        "recommended_top_k": {
          "type": "integer",
          "minimum": 1
        },
        "max_context_tokens": {
          "type": "integer",
          "minimum": 1
        },
        "use_reranker": {
          "type": "boolean"
        },
        "embedding_model": {
          "type": "string"
        },
        "index_version": {
          "type": "string"
        }
      }
    },
    "min_eval_delta": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "locales": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "base_locale": {
      "type": "string"
    },
    "publisher": {
      "type": "object",
      "required": [
        "name"
      ],
      "properties": {
        "name": {
          "type": "string",
          "minLength": 1
        },
        "url": {
          "type": "string",
          "format": "uri"
        },
        "pgp_fingerprint": {
          "type": "string"
        },
        "signed": {
          "type": "boolean"
        }
      }
    },
    "access_control": {
      "type": "object",
      "properties": {
        "classification": {
          "type": "string",
          "enum": [
            "public",
            "internal",
            "confidential",
            "restricted"
          ]
        },
        "required_roles": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "export_restrictions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "encryption_required": {
          "type": "boolean"
        },
        "pii_present": {
          "type": "boolean"
        },
        "gdpr_scope": {
          "type": "boolean"
        },
        "mcp_scopes_required": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "mcp_audience": {
          "type": "string"
        }
      }
    },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "version"
        ],
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1
          },
          "version": {
            "type": "string",
            "minLength": 1
          },
          "domain": {
            "type": "string"
          },
          "registry": {
            "type": "string",
            "format": "uri"
          },
          "optional": {
            "type": "boolean"
          }
        }
      }
    },
    "procedure_capabilities": {
      "type": "object",
      "properties": {
        "sandbox": {
          "type": "string",
          "enum": [
            "wasm",
            "none"
          ]
        },
        "max_runtime_ms": {
          "type": "integer",
          "minimum": 1
        },
        "network_access": {
          "type": "boolean"
        },
        "filesystem_access": {
          "type": "string",
          "enum": [
            "none",
            "read-only",
            "read-write"
          ]
        }
      }
    },
    "mcp": {
      "type": "object",
      "required": [
        "enabled"
      ],
      "properties": {
        "enabled": {
          "type": "boolean"
        },
        "resource_server": {
          "type": "object",
          "properties": {
            "uri_scheme": {
              "type": "string",
              "default": "dkp"
            },
            "expose_eval_cases": {
              "type": "boolean",
              "default": false
            }
          }
        },
        "tool_provider": {
          "type": "object",
          "properties": {
            "tools": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "auth": {
              "type": "object",
              "required": [
                "scheme"
              ],
              "properties": {
                "scheme": {
                  "type": "string",
                  "enum": [
                    "none",
                    "bearer",
                    "oauth2"
                  ]
                },
                "oauth2": {
                  "type": "object",
                  "required": [
                    "authorization_url",
                    "token_url",
                    "scopes"
                  ],
                  "properties": {
                    "authorization_url": {
                      "type": "string",
                      "format": "uri"
                    },
                    "token_url": {
                      "type": "string",
                      "format": "uri"
                    },
                    "scopes": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    }
                  }
                }
              },
              "if": {
                "properties": {
                  "scheme": {
                    "const": "oauth2"
                  }
                },
                "required": [
                  "scheme"
                ]
              },
              "then": {
                "required": [
                  "oauth2"
                ]
              }
            }
          }
        },
        "transport": {
          "type": "string",
          "enum": [
            "stdio",
            "http"
          ],
          "default": "stdio"
        }
      }
    }
  }
}
```

### B.23 `{procedure-id}.schema.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dkp-standard.com/dkp/schemas/v1/procedure_schema.json",
  "title": "Procedure Schema File",
  "type": "object",
  "required": [
    "input_schema",
    "output_schema"
  ],
  "properties": {
    "input_schema": {
      "type": "object",
      "description": "JSON Schema defining the procedure's input object."
    },
    "output_schema": {
      "type": "object",
      "description": "JSON Schema defining the procedure's output object."
    },
    "entry_point": {
      "type": "object",
      "required": [
        "filename",
        "command"
      ],
      "description": "Required when {procedure-id}.wasm is absent. Declares how to invoke the alternative executable.",
      "properties": {
        "filename": {
          "type": "string",
          "description": "Exact filename of the alternative executable, including extension (e.g., \"macro_calculator.py\")."
        },
        "command": {
          "type": "string",
          "description": "Full execution command string (e.g., \"python3 macro_calculator.py\")."
        }
      }
    }
  }
}
```

### B.24 `evidence/sources.csv` Frictionless Table Schema

```json
{
  "$schema": "https://specs.frictionlessdata.io/schemas/table-schema.json",
  "fields": [
    {
      "name": "id",
      "type": "string",
      "description": "Unique source identifier (e.g., src-001). Referenced by source_ref fields throughout the pack.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "title",
      "type": "string",
      "description": "Title of the source document or resource.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "url",
      "type": "string",
      "description": "URL or DOI. Use N/A for offline-only sources.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "retrieved_date",
      "type": "date",
      "format": "%Y-%m-%d",
      "description": "ISO 8601 date the source was accessed.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "license",
      "type": "string",
      "description": "License of the source (e.g., CC-BY-4.0, Public Domain, All Rights Reserved).",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "notes",
      "type": "string",
      "description": "Any relevant notes about the source. MAY be empty."
    }
  ]
}
```

### B.25 `evidence/rights_log.csv` Frictionless Table Schema

```json
{
  "$schema": "https://specs.frictionlessdata.io/schemas/table-schema.json",
  "fields": [
    {
      "name": "id",
      "type": "string",
      "description": "Unique rights record identifier.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "source_id",
      "type": "string",
      "description": "id from sources.csv this record applies to.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "rights_holder",
      "type": "string",
      "description": "Name of the rights holder.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "license_type",
      "type": "string",
      "description": "License type or grant (e.g., Public Domain, CC-BY-4.0, Commercial License).",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "granted_date",
      "type": "date",
      "format": "%Y-%m-%d",
      "description": "ISO 8601 date rights were confirmed or license granted.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "expiry_date",
      "type": "string",
      "description": "ISO 8601 date rights expire, or the literal string 'perpetual'.",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "notes",
      "type": "string",
      "description": "Any relevant notes. MAY be empty."
    }
  ]
}
```

## Appendix C — Normative References

- **[BCP14]** Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997. Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, May 2017. <https://www.rfc-editor.org/info/bcp14>

- **[OKF]** Google Cloud, "Open Knowledge Format Specification v0.1", June 2026. <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>

- **[SEMVER]** Preston-Werner, T., "Semantic Versioning 2.0.0". <https://semver.org/spec/v2.0.0.html>

- **[JSON-SCHEMA]** Wright, A., Andrews, H., Hutton, B., "JSON Schema: A Media Type for Describing JSON Documents", draft-bhutton-json-schema-01, December 2020. <https://json-schema.org/specification>

- **[RFC4180]** Shafranovich, Y., "Common Format and MIME Type for Comma-Separated Values (CSV) Files", RFC 4180, October 2005. <https://www.rfc-editor.org/rfc/rfc4180>

- **[BCP47]** Phillips, A., Davis, M., "Tags for Identifying Languages", BCP 47, RFC 5646, September 2009. <https://www.rfc-editor.org/rfc/rfc5646>

- **[SKOS]** Miles, A., Bechhofer, S., "SKOS Simple Knowledge Organization System Reference", W3C Recommendation, August 2009. <https://www.w3.org/TR/skos-reference/>

- **[MCP]** Anthropic, "Model Context Protocol Specification", protocol version 2024-11-05. <https://modelcontextprotocol.io/specification>

## Appendix D — Informative References

- **[OKF-BLOG]** Google Cloud Blog, "How the Open Knowledge Format can improve data sharing", June 2026. <https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing>
- **[SKILL-MD]** Agent Skills Open Standard, "SKILL.md Specification". <https://github.com/agentskills/agentskills>
- **[MCP-ROADMAP]** Anthropic, "Model Context Protocol 2026 Roadmap". <https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/>
- **[GRAPHRAG]** Microsoft Research, "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", 2024. <https://arxiv.org/abs/2404.16130>
- **[SCHEMA-ORG]** Schema.org Community Group. <https://schema.org>
- **[OPENAPI]** OpenAPI Initiative, "OpenAPI Specification v3.1.2". <https://spec.openapis.org/oas/v3.1.2.html>
