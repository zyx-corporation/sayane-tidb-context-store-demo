# Open Context Store Interface

## Abbreviation

OCSI: Open Context Store Interface

## Status

Conceptual draft.

This document defines OCSI as an open, backend-agnostic interface concept for storing, retrieving, inspecting, and auditing context across AI workflows.

OCSI is broader than the Sayane-TiDB demo. The Sayane-TiDB demo is one implementation-oriented experiment that validates parts of this interface.

## Companion specifications

- `ocsi-t-rde-requirement.md`: defines T-RDE compatibility requirements for OCSI implementations.
- `ocsi-interface-minimality-principles.md`: defines how OCSI avoids fat-interface growth.
- `connection-layer-spec.md`: defines a Sayane-oriented application profile of OCSI.
- `sayane-tidb-basic-spec.md`: defines a TiDB adapter profile of OCSI.

## Purpose

AI workflows increasingly rely on context that moves across tools, models, editors, agents, and organizations.

However, context is often stored in isolated memory systems, vector databases, prompt files, chat histories, or vendor-specific formats. This causes several problems:

- context becomes locked to one runtime or vendor;
- retrieval evidence disappears after generation;
- candidate changes may be merged blindly;
- audit trails become separate from retrieval state;
- embeddings become the center even when structured state is also needed;
- backend-specific features leak into the conceptual model.

OCSI defines a common interface layer for context stores so that context, retrieval evidence, lineage, and audit summaries can remain portable and inspectable.

## Core thesis

A Context Store should not be defined as only a vector index.

A useful Context Store must represent:

- source records;
- searchable units;
- metadata;
- optional embeddings;
- retrieval events;
- selected evidence;
- audit summaries;
- backend capabilities;
- exportable traces.

OCSI treats retrieval as an inspectable event, not a hidden implementation detail.

## Scope

OCSI applies to systems that need to store and retrieve context for:

- LLM workflows;
- AI agents;
- RAG systems;
- local-first profile/context tools;
- enterprise AI memory;
- knowledge workspaces;
- audit-oriented AI pipelines.

OCSI can be implemented by multiple backend families, including:

- local file stores;
- SQLite;
- DuckDB;
- PostgreSQL / pgvector;
- TiDB Cloud;
- vector databases;
- search services;
- hybrid retrieval systems;
- future context-native stores.

## Non-goals

OCSI does not define:

- a single database schema;
- a single vector search implementation;
- a single embedding model;
- a full RDE scoring system;
- a governance model for all AI systems;
- a UI specification;
- a vendor-specific storage format.

OCSI defines the conceptual interface and required evidence boundaries.

## Design principles

### 1. Backend agnosticism

No backend is the conceptual center.

SQLite, DuckDB, PostgreSQL, TiDB, Qdrant, Weaviate, Pinecone, OpenSearch, and future stores are possible implementations.

### 2. Capability declaration

Backends must declare their capabilities instead of assuming uniform behavior.

A caller should be able to ask whether a backend supports lexical search, vector search, hybrid search, native vector indexes, transactional ingest, audit tables, export, and cloud operations.

### 3. Inspectable retrieval

Search results should produce retrieval events that can be inspected later.

The interface should preserve query, mode, retrieved unit IDs, score metadata, selected evidence, audit summary, and timestamp.

### 4. Separation of evidence and generation

A Context Store stores retrieval evidence. It should not silently turn retrieved evidence into a generated conclusion.

Generation belongs to a downstream model or agent. Evidence and generation must remain distinguishable.

### 5. Progressive specialization

Generic operations should remain stable, while backend-specific optimizations may be layered underneath.

For example, TiDB-native vector search, pgvector, or a vector SaaS reranker can be used without rewriting the general OCSI model.

### 6. T-RDE compatibility

OCSI implementations should be T-RDE-compatible.

This does not mean that every retrieval must run a heavyweight evaluator synchronously. It means that the implementation must preserve enough trace data for T-RDE-style review.

See `ocsi-t-rde-requirement.md`.

### 7. Interface minimality

OCSI core should be evidence-centered, not feature-centered.

Backend-specific methods, generation, planning, approval workflows, UI behavior, and business-specific policy logic should not be added to OCSI core unless they satisfy the promotion rule.

See `ocsi-interface-minimality-principles.md`.

## Conceptual model

```text
SourceRecord
  -> SearchUnit
      -> RetrievalEvent
          -> AuditSummary
              -> EvidenceExport
```

## Core objects

### SourceRecord

A SourceRecord is an original unit of context.

Examples:

- Markdown document;
- profile fragment;
- prompt artifact;
- candidate memory;
- approved lineage record;
- imported note;
- conversation extract;
- policy document;
- project file.

Minimum fields:

```text
id
title
source_uri
source_type
created_at
updated_at
metadata
```

### SearchUnit

A SearchUnit is a retrievable unit derived from a SourceRecord.

Examples:

- chunk;
- paragraph;
- section;
- candidate item;
- lineage item;
- prompt block;
- table row;
- transcript segment.

Minimum fields:

```text
id
source_id
unit_index
content
content_hash
metadata
created_at
```

Optional fields:

```text
embedding
embedding_model
embedding_ref
language
tags
valid_from
valid_until
```

### RetrievalEvent

A RetrievalEvent records one retrieval execution.

Minimum fields:

```text
id
query
mode
backend_id
backend_capabilities
retrieved_unit_ids
scores
selected_unit_ids
audit_summary
created_at
metadata
```

### AuditSummary

An AuditSummary records retrieval-adjacent interpretation.

Minimum fields:

```text
preserved
inferred
drift_risk
unresolved
```

This is not full T-RDE scoring. Full T-RDE evaluation can consume OCSI records as input.

### EvidenceExport

EvidenceExport is a portable bundle or trace that can be used outside the backend.

Examples:

- JSON export;
- Markdown report;
- audit bundle;
- article demo output;
- CI artifact;
- compliance evidence package.

## Interface operations

OCSI-compatible systems should expose these logical operations.

```text
get_capabilities()
initialize(options)
put_source_record(record)
put_search_units(source_id, units)
ingest_source(source, options)
search(query, mode, options)
record_retrieval_event(event)
list_retrieval_events(options)
get_retrieval_event(id)
export_evidence(options)
```

These operations may be implemented synchronously or asynchronously.

## Search modes

### lexical

Lexical search retrieves units based on exact or near-exact text matching.

Use cases:

- named concepts;
- feature names;
- policy terms;
- identifiers;
- candidate / lineage wording;
- audit terminology.

### vector

Vector search retrieves units based on semantic similarity.

Use cases:

- paraphrased questions;
- conceptual discovery;
- weakly specified intent;
- cross-document semantic search.

### hybrid

Hybrid search combines lexical and vector retrieval.

Use cases:

- exact terms plus broad semantic intent;
- domain vocabulary plus user paraphrase;
- precision / recall balancing.

Hybrid merge policy must be inspectable and testable.

### backend_native

Backends may expose native retrieval modes.

Examples:

- TiDB-native vector search;
- pgvector search;
- full-text ranking;
- vector SaaS reranking;
- search engine scoring.

Backend-native modes must declare how they map to OCSI evidence fields.

## Backend capability model

Recommended capability fields:

```text
supports_lexical_search
supports_vector_search
supports_hybrid_search
supports_native_vector_index
supports_full_text_index
supports_sql_queries
supports_transactional_ingest
supports_audit_log_tables
supports_portable_export
supports_multi_user_access
supports_cloud_managed_operations
supports_local_first_storage
supports_event_lineage
```

Capabilities are not marketing claims. They must correspond to observable behavior.

## Backend families

### LocalContextStore

Expected implementations:

- file-backed store;
- SQLite;
- DuckDB;
- local Markdown index;
- Git-backed vault.

Primary use:

- local-first personal or developer workflows;
- portable context;
- offline operation;
- lightweight audit and testability.

### StandardEnterpriseContextStore

Expected implementations:

- PostgreSQL;
- pgvector;
- managed PostgreSQL services.

Primary use:

- conservative enterprise deployment;
- SQL governance;
- relational metadata;
- existing operational practices.

### ScaleOutEnterpriseContextStore

Expected implementations:

- TiDB Cloud;
- distributed SQL backends.

Primary use:

- scale-out SQL-backed context storage;
- SQL-addressable retrieval evidence;
- enterprise managed operations;
- hybrid transactional / analytical directions.

### RetrievalSpecializedContextStore

Expected implementations:

- Pinecone;
- Weaviate;
- Qdrant;
- OpenSearch;
- Elastic;
- Algolia;
- Typesense;
- other vector or search SaaS systems.

Primary use:

- high-quality retrieval;
- vector-native search;
- keyword and semantic hybrid retrieval;
- reranking and search UX.

These systems may need a separate source-of-truth store for lineage and audit semantics.

## Relationship to Sayane

Sayane can be an OCSI user and partial implementer.

Sayane-specific concepts map naturally to OCSI:

```text
Sayane Profile / Context Document -> SourceRecord
Captured Candidate -> SourceRecord or SearchUnit
Approved / Rejected Lineage -> SourceRecord or metadata
Compiled Prompt Block -> SearchUnit
Retrieval Log -> RetrievalEvent
Lightweight T-RDE Summary -> AuditSummary
```

Sayane should not become tied to one OCSI backend.

## Relationship to Sayane-TiDB demo

The Sayane-TiDB demo is an empirical implementation experiment for OCSI.

It currently demonstrates:

- SourceRecord-like documents;
- SearchUnit-like chunks;
- JSON embedding storage;
- lexical search;
- Python-side vector scoring;
- hybrid merge policy;
- RetrievalEvent-like logs;
- lightweight AuditSummary.

It does not yet demonstrate:

- TiDB-native vector-indexed retrieval;
- full OCSI compliance;
- full T-RDE scoring;
- production multi-user backend behavior.

## Promotion rule

A backend-specific feature should be promoted into OCSI only when:

1. it is useful across more than one backend family;
2. it can be described without vendor-specific syntax;
3. it has testable behavior;
4. it preserves backend independence;
5. it strengthens T-RDE evidence preservation;
6. its Delta-M can be clearly explained.

## RDE / Delta-M

- Preserved: context remains portable, inspectable, and not bound to a single backend.
- Transformed: Sayane Context Store thinking is generalized into an open interface concept.
- Added: OCSI names, object model, capability model, backend families, T-RDE requirement, minimality principles, and promotion rule.
- Unresolved: formal versioning, compliance test suite, and governance process.
- Drift risk: OCSI may become too abstract unless anchored by concrete demo implementations such as Sayane-TiDB.

## Next steps

1. Keep this document as the conceptual OCSI draft.
2. Treat `ocsi-t-rde-requirement.md` as the implementation conformance constraint.
3. Treat `ocsi-interface-minimality-principles.md` as the interface growth constraint.
4. Treat `connection-layer-spec.md` as a Sayane-oriented application profile of OCSI.
5. Treat `sayane-tidb-basic-spec.md` as a TiDB adapter profile of OCSI.
6. Add a minimal compliance checklist.
7. Add an OCSI-to-Sayane mapping document if the concept is promoted to the main Sayane repository.
