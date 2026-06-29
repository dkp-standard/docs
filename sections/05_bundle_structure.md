
## 5. Bundle Structure

### 5.1 Directory Layout

A conformant DKP bundle MUST have the following directory structure at its pack root. Items marked **[R]** are REQUIRED; items marked **[S]** are SHOULD (RECOMMENDED); items marked **[O]** are OPTIONAL.

```
{pack-root}/
  manifest.json                [R]
  checksums.json               [S]
  bundle.sig                   [O]
  README.md                    [S]
  LICENSE.md                   [S]
  CHANGELOG.md                 [S]
  machine/                     [R]
    system_prompt.md           [R]
    rules.json                 [R]
    ontology.json              [R]
    glossary.json              [R]
    constraints.json           [R]
    decision_trees.json        [R]
    retrieval_chunks.jsonl     [R]
    eval_set.jsonl             [S]
    knowledge_graph.json       [S]
    taxonomy.json              [O]
    assets.json                [O]
    assets/                    [O]
    procedures/                [O]
    cross_refs.json            [O]
    mcp_manifest.json          [O]
  okf/                         [R]
    index.md                   [R]
    log.md                     [S]
    terms/                     [S]
    rules/                     [S]
    constraints/               [S]
    procedures/                [S]
    chunks/                    [S]
    ontology/                  [S]
  human/                       [S]
    handbook.md                [S]
    handbook.pdf               [O]
    handbook.epub              [O]
    quickstart.md              [O]
    cheatsheet.md              [O]
    faq.md                     [O]
    examples/                  [O]
  evidence/                    [R]
    sources.csv                [R]
    rights_log.csv             [R]
    review_notes.md            [S]
    eval_results/              [S]
      eval_summary.json        [S]
      {date}-{model}.jsonl     [S]
  skills/                      [O]
    index.md                   [S]
    {skill-name}/              [O]
      SKILL.md                 [R]
      scripts/                 [O]
      references/              [O]
  l10n/                        [O]
    {locale}/                  [O]
      machine/                 [O]
        glossary.json          [O]
        system_prompt.md       [O]
      okf/                     [O]
        terms/                 [O]
      human/                   [O]
        handbook.md            [O]
```

A bundle distributed as a `.zip` archive MUST contain the pack root as the top-level directory within the archive.

Processors MUST NOT require the presence of OPTIONAL files. Processors MAY warn when RECOMMENDED files are absent.

### 5.2 Archive Format

A DKP bundle MAY be distributed as:

- A directory tree (e.g., as a Git repository or subdirectory)
- A `.zip` archive
- A `.tar.gz` archive
- A `.tar.xz` archive
- A `.dkp` archive — the canonical DKP distribution format; equivalent to `.tar.xz` compressed at maximum XZ compression level (preset 9)

Processors MUST support directory trees. Processors SHOULD support compressed archives. The `.dkp` extension is the RECOMMENDED format for registry publication due to its superior compression ratio.

### 5.3 Pack Naming

The pack root directory name SHOULD match the `name` field in `manifest.json`, with spaces replaced by hyphens and all characters lowercased. This is a convention for tooling, not a conformance requirement.

### 5.4 Supply-Chain Integrity Files

#### `checksums.json`

A JSON object listing the SHA-256 digest of every file in the bundle at the time of signing. Processors SHOULD verify all checksums in `checksums.json` before loading bundle content. Processors MUST warn when a file's actual digest does not match its recorded checksum.

The top-level key is the relative file path from the pack root; the value is the lowercase hex SHA-256 digest:

```json
{
  "manifest.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "machine/glossary.json": "..."
}
```

#### `bundle.sig`

A detached cryptographic signature (Ed25519) over the SHA-256 of the bundle's canonical serialization (deterministic `tar` ordering of all files listed in `checksums.json`). Processors SHOULD verify `bundle.sig` against the publisher's public key declared in `manifest.json` `publisher.pgp_fingerprint` when present. Processors MUST warn when loading bundles from a registry that lack a valid `bundle.sig`.

