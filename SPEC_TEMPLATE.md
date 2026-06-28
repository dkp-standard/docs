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

{{> sections/01_introduction.md }}
{{> sections/02_terminology.md }}
{{> sections/03_relationship_to_okf.md }}
{{> sections/04_dkp_type_taxonomy.md }}
{{> sections/05_bundle_structure.md }}
{{> sections/06_manifest.md }}
{{> sections/07_conformance.md }}
{{> sections/08_versioning.md }}
{{> sections/09_machine_layer.md }}
{{> sections/10_okf_layer.md }}
{{> sections/11_human_layer.md }}
{{> sections/12_evidence_layer.md }}
{{> sections/13_skill_layer.md }}
{{> sections/14_localization_layer.md }}
{{> sections/15_mcp_surface.md }}
{{> sections/16_8gate_quality_standard.md }}
{{> sections/appendix_a_bundle_example.md }}
{{> sections/appendix_b_json_schemas.md }}
{{> sections/appendix_c_normative_references.md }}
{{> sections/appendix_d_informative_references.md }}
