
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
