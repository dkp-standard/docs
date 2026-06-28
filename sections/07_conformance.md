
## 7. Conformance

### 7.1 Conformance Language

Conformance language (MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL) is defined in §2.1.

### 7.2 Conformance Targets

This specification defines four distinct conformance targets:

**DKP-Conformant Bundle** — A directory (or archive derived from it) that satisfies all MUST and MUST NOT requirements in §5–§6 and §9–§15 and passes Gates 4 and 8 of the quality standard (§16). This is the baseline structural conformance level verifiable by automated tooling (`dkp validate`). Gate 7 is skipped when `eval_set.jsonl` is absent; skipping Gate 7 does not disqualify a bundle from DKP-Conformant status.

**DKP-Evaluated Bundle** — A DKP-Conformant Bundle that additionally includes a populated `eval_set.jsonl` and successfully passes Gate 7 (§16), demonstrating measurable retrieval and generation utility above the `min_eval_delta` threshold.

**DKP-Reviewed Bundle** — A DKP-Evaluated Bundle that additionally satisfies the editorial quality requirements of Gates 1–3 and 5–6 (§16), as attested by a dated, named sign-off in `evidence/review_notes.md` (§12.3). A DKP-Reviewed Bundle is a strict superset of a DKP-Evaluated Bundle.

**Conformant DKP Processor** — A tool (CLI, library, agent integration) that reads, validates, converts, or evaluates DKP bundles and satisfies all MUST and MUST NOT requirements stated for processors in §5–§6 and §9–§15.

A bundle and a processor may independently conform or fail to conform. A processor that accepts non-conformant bundles is not itself non-conformant, provided it signals the non-conformance to the caller.

### 7.3 OKF Conformance

The `okf/` directory of a conformant DKP bundle MUST be a conformant OKF bundle as defined in [OKF SPEC.md](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Where this specification is silent, OKF requirements apply to the `okf/` layer.
