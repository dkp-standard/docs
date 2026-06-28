
## 8. Versioning

### 8.1 Specification Version

This specification uses Semantic Versioning 2.0.0.

- **PATCH** increments (e.g., 1.0.0 → 1.0.1): Clarifications, corrections, and editorial changes. No normative change.
- **MINOR** increments (e.g., 1.0.0 → 1.1.0): Backward-compatible additions. New OPTIONAL or RECOMMENDED fields; new SHOULD requirements. Existing conformant bundles remain conformant.
- **MAJOR** increments (e.g., 1.0.0 → 2.0.0): Breaking changes. New REQUIRED fields; removed fields; changed field semantics.

### 8.2 Bundle Version

`manifest.json` `version` MUST be a Semantic Versioning 2.0.0 string. Bundle version represents the content version of the pack, not the DKP specification version.

- **PATCH**: Minor content corrections, updated `update_date`, no schema changes
- **MINOR**: New concepts added, new evaluation cases added, source list expanded
- **MAJOR**: Domain scope change, structural restructure of the bundle's content organization, audience change, or source rights expiry requiring removal of chunks (see §12.2). **Important:** Bundle versioning MUST NOT be used to bypass schema validation. If a structural restructure violates the normative JSON schemas declared in Appendix B for the bundle's declared `spec` version, the bundle fails Gate 4 and is invalid. Modifying the normative schemas requires adopting a new DKP Specification version, not just incrementing the bundle version.

### 8.3 Processor Version Handling

Processors MUST attempt to parse any bundle whose `manifest.json` is valid JSON and contains all REQUIRED fields. Processors MUST read the `spec` field to determine the specification version the bundle was produced against. Processors SHOULD warn when `spec` identifies a version older than the processor's supported version, and SHOULD warn (but MUST NOT reject) when `spec` identifies a newer version.
