
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
