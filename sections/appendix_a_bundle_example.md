
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

