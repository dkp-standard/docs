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
