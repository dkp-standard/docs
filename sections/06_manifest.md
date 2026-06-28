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
- **Constraints:** Non-empty. Scoped registry identifier for the pack, in the form `@scope/pack-name` (e.g., `"@example/nutrition-for-men"`). MUST be unique within the registry scope. Use `title` for the human-readable display name.
- **Example:** `"@example/nutrition-for-men"`

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

#### `title`

- **Type:** string
- Human-readable display name of the pack. Shown in search results, registry UI, and documentation. SHOULD be present whenever the pack is published to a registry.
- **Example:** `"Nutrition for Men"`

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
  "name": "@example/nutrition-for-men",
  "title": "Nutrition for Men",
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
