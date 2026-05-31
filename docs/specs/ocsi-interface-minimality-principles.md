# OCSI Interface Minimality Principles

## Status

Conceptual draft.

This document defines principles for keeping OCSI — Open Context Store Interface — open, extensible, and T-RDE-compatible without turning the interface layer into an overly fat abstraction.

## Purpose

OCSI should be powerful enough to preserve context evidence and support T-RDE-style review.

However, it must not become a dumping ground for every convenient backend feature, retrieval method, summarization operation, agent behavior, or workflow action.

The purpose of this document is to define how OCSI stays minimal.

## Core thesis

OCSI core should be evidence-centered, not feature-centered.

The core interface should define the minimum structures needed to trace meaning transformation:

```text
SourceRecord
  -> SearchUnit
      -> RetrievalEvent
          -> AuditSummary
              -> EvidenceExport
```

If a proposed interface addition does not improve this traceability, it should not be added to OCSI core.

## Layer distinction

OCSI should be divided into three layers.

```text
OCSI Core
  -> OCSI Extension Profile
      -> Backend Adapter
```

### OCSI Core

Defines the minimum portable evidence model.

Core concepts:

- SourceRecord;
- SearchUnit;
- RetrievalEvent;
- AuditSummary;
- EvidenceExport;
- BackendCapability.

Core operations:

- get_capabilities;
- put source records;
- put search units;
- search;
- record retrieval events;
- inspect retrieval events;
- export evidence.

### OCSI Extension Profile

Defines optional behavior for a particular family of systems.

Examples:

- Sayane profile/context profile;
- enterprise SQL profile;
- vector-native profile;
- local-first profile;
- compliance/audit profile.

Extension profiles may add conventions, but they should not silently redefine OCSI core.

### Backend Adapter

Maps OCSI concepts to concrete implementation details.

Examples:

- TiDB SQL schema;
- PostgreSQL / pgvector schema;
- SQLite tables;
- DuckDB analytics views;
- Qdrant collection schema;
- OpenSearch index mapping.

Backend-specific behavior belongs here unless it is promoted through the promotion rule.

## What belongs in OCSI core

A feature may belong in OCSI core if it satisfies all of the following:

1. It is necessary for traceability.
2. It is useful across multiple backend families.
3. It can be described without vendor-specific syntax.
4. It can be tested as observable behavior.
5. It preserves separation between retrieval evidence and generated conclusions.
6. It supports T-RDE evidence requirements.

## What does not belong in OCSI core

The following should not be added to OCSI core by default:

- summarization;
- generation;
- planning;
- autonomous decision execution;
- approval workflows;
- human resource scoring;
- model-specific prompting;
- vendor-specific query syntax;
- UI behavior;
- scheduling;
- notification delivery;
- business-specific policy logic.

These may be implemented in systems that use OCSI, but they should not become part of OCSI core.

## Capability over method proliferation

OCSI should prefer capability declarations over many specialized methods.

Prefer:

```text
get_capabilities()
search(query, mode, options)
record_retrieval_event(event)
```

Avoid turning the core into:

```text
search_by_bm25()
search_by_vector_cosine()
search_by_hnsw()
search_by_tidb_vector()
search_by_pgvector_l2()
search_by_qdrant_filter()
search_by_opensearch_query_string()
```

Backend-specific methods should live in adapters or extension profiles.

## Evidence over convenience

Convenience APIs can be useful, but they should not replace the evidence model.

For example, a convenience API such as:

```text
retrieve_context_for_prompt(query)
```

may exist in a higher-level profile.

But OCSI core must still preserve:

```text
query
mode
retrieved_unit_ids
scores
selected_unit_ids
audit_summary
backend_capability_snapshot
```

## T-RDE as minimality constraint

T-RDE compatibility constrains interface growth.

A proposed addition should be rejected from OCSI core if it only adds capability but does not improve the ability to evaluate meaning transformation.

Questions to ask:

- Does this preserve source-to-search-unit traceability?
- Does this preserve retrieval evidence?
- Does this distinguish selected evidence from generated conclusions?
- Does this help detect drift, overstatement, or unresolved claims?
- Can this be represented as metadata, capability, or adapter behavior instead?

## Promotion rule

A feature should move from adapter or extension profile into OCSI core only when:

1. at least two backend families need it;
2. it has a backend-neutral definition;
3. it strengthens T-RDE evidence preservation;
4. it has positive and negative tests;
5. it does not force one retrieval architecture on all backends;
6. its Delta-M is documented.

## Anti-fat-interface examples

### Bad: adding backend-specific query methods to core

```text
search_tidb_vector()
search_pgvector_l2()
search_qdrant_payload_filter()
```

Why bad:

- leaks backend details;
- makes the core harder to implement;
- confuses interface with adapter.

Better:

```text
search(query, mode="backend_native", options={...})
record_retrieval_event(...)
```

### Bad: adding generation to core

```text
generate_answer(query)
summarize_retrieved_context()
```

Why bad:

- turns OCSI into an agent runtime;
- collapses evidence and conclusion;
- weakens T-RDE review.

Better:

```text
export_evidence(...)
```

Then let a downstream generator consume the evidence.

### Bad: adding approval workflow to core

```text
approve_candidate()
reject_candidate()
merge_candidate()
```

Why bad:

- these are Sayane workflow concepts, not universal OCSI core requirements;
- other systems may handle approval differently.

Better:

Represent candidate and lineage as SourceRecord/SearchUnit metadata, then let a Sayane extension profile define approval operations.

## RDE / Delta-M

- Preserved: OCSI remains open, backend-agnostic, and evidence-centered.
- Transformed: interface growth is constrained by T-RDE evidence requirements.
- Added: core/extension/adapter layering and promotion rules.
- Unresolved: exact compliance test format for minimality.
- Drift risk: convenience APIs may re-enter core unless extension boundaries are enforced.

## Next steps

1. Reference this document from `open-context-store-interface.md`.
2. Add a compliance checklist for OCSI-Basic / T-RDE-Ready / T-RDE-Strict.
3. Keep Sayane-specific workflows in a Sayane extension profile.
4. Keep TiDB-specific behavior in the Sayane-TiDB adapter profile.
