
## 4. DKP Type Taxonomy

The DKP Type Taxonomy defines the seven canonical type values used throughout a DKP bundle. It governs both the machine layer (§9) and the OKF layer (§10): machine-layer assets map one-to-one to taxonomy entries, and every concept file in the `okf/` directory MUST declare one of these types in its frontmatter.

All concept files in the DKP OKF layer MUST use one of the following seven `type` values. These are valid OKF type values (OKF permits any producer-defined type string).

| DKP Type | Corresponding Machine Asset | Description |
|---|---|---|
| `DomainTerm` | `glossary.json` terms | A glossary entry: canonical term, definition, aliases, related terms |
| `DomainRule` | `rules.json` entries | An operational must-do or must-avoid for agents acting in this domain |
| `Constraint` | `constraints.json` entries | An edge case, anti-pattern, or hard limit |
| `DecisionProcedure` | `decision_trees.json` trees | A traversable decision tree or procedure |
| `KnowledgeChunk` | `retrieval_chunks.jsonl` entries | A self-contained distilled fact for RAG or direct injection |
| `EntityType` | `ontology.json` entity types | A domain entity with attributes and relationships |
| `EvalCase` | `eval_set.jsonl` entries | An evaluation Q/A case (transparency asset) |

Concept files using `EvalCase` type are OPTIONAL and SHOULD be omitted from packs where evaluation transparency is not desired.

Processors performing DKP-specific validation MUST flag any `type` value not in this table as an error.
