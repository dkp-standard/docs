
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
