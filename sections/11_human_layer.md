
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

