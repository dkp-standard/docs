
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
