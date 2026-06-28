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
