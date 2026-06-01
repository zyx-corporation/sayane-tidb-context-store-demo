# OCSI Compliance Checklist

## Status

Conceptual checklist draft.

This document defines a practical compliance checklist for OCSI — Open Context Store Interface — implementations.

It operationalizes:

- `open-context-store-interface.md`;
- `ocsi-t-rde-requirement.md`;
- `ocsi-interface-minimality-principles.md`.

## Purpose

OCSI should not become a vague label.

An implementation should be able to state which conformance level it satisfies, which evidence it preserves, which capabilities it exposes, and which gaps remain.

This checklist is designed for:

- implementation review;
- PR review;
- backend adapter evaluation;
- article/demo claim boundaries;
- future compliance tests.

## Conformance levels

OCSI defines three practical conformance levels.

```text
OCSI-Basic
OCSI-T-RDE-Ready
OCSI-T-RDE-Strict
```

A system may also declare itself as:

```text
OCSI-Experimental
```

when it implements only a subset of OCSI and should not be presented as conforming.

## OCSI-Experimental

Use this label when the implementation is a prototype or demo that does not yet satisfy OCSI-Basic.

Checklist:

- [ ] It clearly states that it is experimental.
- [ ] It does not claim full OCSI compliance.
- [ ] It identifies missing OCSI-Basic requirements.
- [ ] It documents which evidence fields are currently preserved.
- [ ] It documents which claims must not be made.

## OCSI-Basic

OCSI-Basic is the minimum level for claiming that a backend implements OCSI.

### Source and search-unit storage

- [ ] Stores SourceRecord-like objects.
- [ ] Stores SearchUnit-like objects.
- [ ] Preserves a stable source ID.
- [ ] Preserves a stable search unit ID.
- [ ] Preserves content or a recoverable content reference.
- [ ] Preserves metadata.

### Retrieval

- [ ] Exposes at least one search mode.
- [ ] Declares supported search modes.
- [ ] Records retrieval events.
- [ ] Preserves query text.
- [ ] Preserves search mode.
- [ ] Preserves retrieved unit IDs.
- [ ] Preserves selected unit IDs.
- [ ] Preserves score or rank metadata when available.

### Audit summary

- [ ] Stores lightweight AuditSummary or equivalent.
- [ ] Distinguishes lightweight audit from full T-RDE scoring.
- [ ] Preserves unresolved items or states that unresolved tracking is unsupported.

### Capability declaration

- [ ] Exposes backend capability metadata.
- [ ] Does not claim unsupported capabilities.
- [ ] Declares whether vector search is native, adapter-level, or unsupported.
- [ ] Declares whether hybrid search is native, adapter-level, or unsupported.

### Claim boundary

- [ ] Documentation states what the implementation proves.
- [ ] Documentation states what the implementation does not prove.

## OCSI-T-RDE-Ready

OCSI-T-RDE-Ready is the minimum recommended level for enterprise or cross-agent use.

It must satisfy OCSI-Basic plus the following.

### Source provenance

- [ ] Preserves source URI or equivalent source location.
- [ ] Preserves source hash or equivalent integrity marker.
- [ ] Preserves source type.
- [ ] Preserves creation/update timestamps.

### Search-unit transformation evidence

- [ ] Records chunking or search-unit derivation strategy.
- [ ] Preserves content hash for each SearchUnit.
- [ ] Preserves the relation from SearchUnit to SourceRecord.
- [ ] Preserves enough information to explain why a SearchUnit exists.

### Embedding evidence

Required when embeddings are used.

- [ ] Records embedding model name.
- [ ] Records embedding model version or provider metadata when available.
- [ ] Records embedding generation timestamp or equivalent.
- [ ] Records embedding hash or reference.
- [ ] Distinguishes embedding representation from source meaning.

### Retrieval evidence

- [ ] Records backend ID.
- [ ] Records backend capability snapshot at retrieval time.
- [ ] Records fallback behavior.
- [ ] Records merge policy for hybrid retrieval.
- [ ] Separates retrieved evidence from selected evidence.

### Exportability

- [ ] Exports retrieval evidence in a portable format.
- [ ] Exports enough data for later T-RDE-style review.
- [ ] Does not require access to a proprietary UI to inspect basic evidence.

## OCSI-T-RDE-Strict

OCSI-T-RDE-Strict is the level required before describing an implementation as audit-grade.

It must satisfy OCSI-T-RDE-Ready plus the following.

### Tests

- [ ] Positive tests cover source storage.
- [ ] Negative tests cover missing or malformed source evidence.
- [ ] Positive tests cover search-unit derivation.
- [ ] Negative tests cover drift-prone search-unit derivation.
- [ ] Positive tests cover retrieval logging.
- [ ] Negative tests cover missing retrieval logs.
- [ ] Positive tests cover capability declaration.
- [ ] Negative tests cover unsupported capability claims.
- [ ] Positive tests cover evidence export.
- [ ] Negative tests cover incomplete evidence export.

### Reviewability

- [ ] A human reviewer can inspect one retrieval event without backend-specific tooling.
- [ ] Drift-risk classification is reviewable.
- [ ] Backend-native ranking or scoring is explained or preserved as metadata.
- [ ] Generated output can be linked back to selected evidence when downstream generation is used.

### Governance

- [ ] Backend-specific features follow the OCSI promotion rule before entering OCSI core.
- [ ] Changes to evidence schema require Delta-M notes.
- [ ] Changes to retrieval semantics require tests and documentation updates.
- [ ] Changes to audit summary meaning require explicit review.

### Portability

- [ ] Evidence export is versioned.
- [ ] Evidence export has compatibility notes.
- [ ] Evidence export can be validated independently.

## Current Sayane-TiDB demo status

Current expected status:

```text
OCSI-Experimental approaching OCSI-Basic
```

Known satisfied areas:

- [x] Stores document-like records.
- [x] Stores chunk-like records.
- [x] Preserves source hash per document.
- [x] Records chunking strategy per SearchUnit.
- [x] Records embedding model/provider per SearchUnit when embedded.
- [x] Supports text search.
- [x] Supports adapter-level vector search using JSON embeddings and Python cosine scoring.
- [x] Supports adapter-level hybrid merge.
- [x] Records retrieval logs.
- [x] Stores backend capability snapshot per RetrievalEvent.
- [x] Exposes backend capability metadata via CLI.
- [x] Stores lightweight audit summaries.
- [x] Has unit tests and CI for selected retrieval utilities.

Known gaps:

- [ ] Does not yet export evidence as a formal portable bundle.
- [ ] Does not yet implement TiDB-native vector search.
- [ ] Does not yet satisfy OCSI-T-RDE-Ready.
- [ ] Does not yet record embedding generation timestamp or embedding hash.
- [ ] Does not yet record fallback behavior or merge policy metadata in retrieval logs.

## Claim guidance

Allowed:

> This implementation is an OCSI-oriented Sayane-TiDB experiment.

> It demonstrates parts of OCSI-Basic: source storage, search units, retrieval logs, and lightweight audit summaries.

Not allowed yet:

> This implementation is OCSI-compliant.

> This implementation is audit-grade.

> This implementation satisfies OCSI-T-RDE-Ready.

> This implementation uses TiDB-native vector-indexed search.

## RDE / Delta-M

- Preserved: OCSI remains evidence-centered and backend-agnostic.
- Transformed: abstract conformance levels become reviewable checklist items.
- Added: concrete Basic / T-RDE-Ready / T-RDE-Strict criteria.
- Unresolved: automated compliance test suite is not yet implemented.
- Drift risk: checklist compliance may become box-ticking unless linked to real tests and evidence exports.

## Next steps

1. Add a machine-readable checklist format.
2. Add CI checks for OCSI-Basic evidence preservation.
3. Update Sayane-TiDB implementation toward OCSI-Basic.
4. Create issues for each known gap.
