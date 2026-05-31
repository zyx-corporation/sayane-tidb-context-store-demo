# Context Store Connection Layer Specification

## Status

General draft for Sayane Context Store backends.

This document defines the backend-agnostic connection layer contract between Sayane-style context workflows and concrete Context Store implementations.

It is intentionally general. SQLite, DuckDB, PostgreSQL, TiDB, vector databases, search services, and other stores are implementation targets, not the conceptual center.

## Purpose

The connection layer provides a stable boundary between:

```text
Sayane workflow concepts
  -> Context Store Connection Layer
      -> backend adapter
          -> concrete database / service
```

The purpose is to prevent Sayane from becoming coupled to one backend while still allowing backend-specific capabilities to be used when available.

The connection layer should make storage, retrieval, and audit evidence portable across backend families.

## Design principles

1. Backend independence: Sayane core must not depend on TiDB, PostgreSQL, SQLite, or any vector service.
2. Capability discovery: backend-specific features must be declared, not assumed.
3. Inspectability: retrieval behavior must produce logs that can be reviewed later.
4. Progressive specialization: specialized backends may optimize storage or retrieval, but the general contract remains stable.
5. RDE compatibility: meaning-changing operations must remain traceable and auditable.

## Non-goals

This layer does not define:

- the full Sayane production storage model;
- the full RDE scoring model;
- any single backend's SQL dialect or vector syntax;
- multi-user enterprise authentication;
- cloud deployment topology;
- UI or editor integration;
- migration compatibility between every backend pair.

## Backend families

The connection layer should be able to support multiple backend families.

```text
LocalContextStore
  -> SQLite / file-backed metadata
  -> DuckDB / local analytics

StandardEnterpriseContextStore
  -> PostgreSQL / pgvector
  -> managed PostgreSQL SaaS

ScaleOutEnterpriseContextStore
  -> TiDB Cloud
  -> distributed SQL backends

RetrievalSpecializedContextStore
  -> vector DB SaaS
  -> search SaaS
  -> hybrid retrieval services
```

No backend family is the conceptual center. Each exists to satisfy a different deployment and retrieval profile.

## Core responsibilities

The connection layer must provide a contract for:

1. storing source records;
2. storing derived searchable units;
3. storing metadata;
4. storing optional embeddings or embedding references;
5. running lexical search when supported;
6. running semantic/vector search when supported;
7. running hybrid retrieval when supported;
8. recording retrieval events;
9. inspecting retrieval events;
10. attaching audit summaries or audit hooks;
11. reporting backend capabilities;
12. exporting portable evidence when possible.

## Conceptual objects

### SourceRecord

A source record represents an original unit of context.

Examples:

- Markdown document;
- Sayane profile fragment;
- candidate context item;
- approved lineage record;
- prompt artifact;
- imported external note.

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

A search unit represents a retrievable piece of context derived from a source record.

Examples:

- chunk;
- paragraph;
- section;
- candidate item;
- lineage item;
- prompt block.

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
```

### RetrievalEvent

A retrieval event records one search execution.

Minimum fields:

```text
id
query
mode
retrieved_unit_ids
scores
selected_unit_ids
audit_summary
created_at
metadata
```

### AuditSummary

An audit summary records retrieval-adjacent interpretation.

Minimum fields:

```text
preserved
inferred
drift_risk
unresolved
```

This is not full RDE scoring. Full RDE integration should remain a higher-level evaluator unless explicitly promoted.

### BackendCapability

A backend capability describes what a backend adapter can safely provide.

Recommended fields:

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
```

## Interface operations

The connection layer should expose the following logical operations.

```text
get_capabilities()
initialize()
put_source_record(record)
put_search_units(source_id, units)
ingest_source(source, options)
search(query, mode, options)
record_retrieval_event(event)
list_retrieval_events(options)
get_retrieval_event(id)
export_evidence(options)
```

Backend adapters may expose additional operations, but those operations must not become required by Sayane core unless promoted into this general contract.

## Search modes

### lexical

Lexical search retrieves units based on exact or near-exact textual matching.

Expected role:

- named concepts;
- feature names;
- policy terms;
- candidate / lineage wording;
- audit terminology;
- source identifiers.

### vector

Vector search retrieves units based on semantic similarity.

Expected role:

- conceptual questions;
- paraphrases;
- queries that do not match exact document wording;
- cross-document conceptual discovery.

### hybrid

Hybrid search combines lexical and vector retrieval.

Expected role:

- exact-term and conceptual mixed queries;
- domain-specific vocabulary plus broader intent;
- retrieval where both precision and recall matter.

The merge policy must be inspectable and testable.

### backend_native

Some backends may expose their own retrieval mode.

Examples:

- native full-text ranking;
- native vector index search;
- native hybrid search;
- external reranker pipeline.

Backend-native modes must disclose how they map to the general contract and what evidence is logged.

## Logging requirements

Every retrieval execution should be recordable as a RetrievalEvent.

A retrieval event should preserve:

- original query;
- search mode;
- backend adapter name;
- backend capability snapshot when relevant;
- retrieved unit IDs;
- scores or rank metadata;
- selected unit IDs;
- audit summary;
- timestamp;
- optional trace metadata.

The log is part of the system's inspectability, not debug output.

## Error handling

The connection layer should fail explicitly when required backend capabilities, credentials, indexes, or data are missing.

Examples:

- missing database connection settings should fail before initialization;
- missing embedding provider credentials should fail before embedding generation;
- vector search should fail or return a clear no-capability result if embeddings are absent;
- unsupported search modes should raise explicit errors;
- backend-native features should not silently fall back unless the fallback is logged.

## Capability negotiation

Before using optional backend features, callers should check capabilities.

Example:

```text
if backend.supports_native_vector_index:
    use native vector search
else if backend.supports_vector_search:
    use adapter-level vector search
else:
    report unsupported vector mode
```

Fallback behavior must be visible in retrieval events or operation output.

## Promotion rule

A backend-specific capability should be promoted to the general connection layer only when:

1. it is needed by more than one backend family;
2. it can be described without vendor-specific syntax;
3. it has testable behavior;
4. it does not weaken Sayane's backend independence;
5. its Delta-M can be explained.

## Backend-specific mapping examples

### SQLite + DuckDB

Expected role:

- local-first storage;
- portable development and personal use;
- local analytics over logs.

### PostgreSQL / pgvector

Expected role:

- standard enterprise SQL backend;
- relational metadata;
- pgvector-based retrieval;
- conservative cloud or on-premise deployment.

### TiDB Cloud

Expected role:

- scale-out enterprise SQL backend candidate;
- SQL-addressable retrieval logs and audit summaries;
- path toward native vector / full-text / hybrid retrieval.

### Vector/search SaaS

Expected role:

- retrieval-specialized backend;
- high-quality vector, lexical, or hybrid retrieval;
- usually paired with another source-of-truth store for audit and lineage.

## RDE / Delta-M

- Preserved: Sayane remains backend-agnostic and centered on inspectable context workflows.
- Transformed: connection behavior is generalized beyond the TiDB demo.
- Added: capability negotiation, backend family mapping, and promotion rules.
- Unresolved: exact migration path into the main Sayane repository.
- Drift risk: the general layer may become too abstract unless kept tied to concrete retrieval and audit requirements.
