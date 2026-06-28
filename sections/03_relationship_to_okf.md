---

## 3. Relationship to OKF

DKP is a strict extension of OKF. All DKP-specific frontmatter fields are valid OKF (OKF permits producer-defined fields beyond `type`). Any OKF-compatible agent framework can load and traverse the DKP `okf/` layer without modification.

The relationship is summarized as:

```
OKF — vendor-neutral format (files + frontmatter)
 └── DKP — type taxonomy + machine layer + quality bar + provenance
            + knowledge graph + multi-modal + skills + localization
            + access control + supply-chain integrity
```

The DKP type taxonomy (§4) is a named subset of OKF's open-ended `type` field. Producers MUST use only the defined DKP types in the `okf/` layer of a conformant DKP bundle. Processors MUST NOT reject unknown `type` values when performing general OKF operations, but DKP-specific validation MUST flag unknown types as errors.
