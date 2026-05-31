# Connection Layer Specification

## Status

Draft for the Sayane-linked TiDB Context Store demo.

This document defines the connection layer contract between Sayane-style context workflows and backend-specific Context Store implementations.

It is intentionally backend-agnostic. TiDB, PostgreSQL, SQLite, DuckDB, and other services are implementation targets, not the conceptual center.

## Purpose

The connection layer provides a stable boundary between:

```text
Sayane workflow concepts
  -> Context Store Interface
      -> backend adapter
          -> concrete database / service
```

The purpose is to prevent Sayane from becoming coupled to one backend while still allowing backend-specific capabilities to be demonstrated and tested.

## Non-goals

This layer does not define:

- the full Sayane production storage model;
- the full RDE scoring model;
- TiDB-native vector search syntax;
- multi-user enterprise authentication;
- migration compatibility with the main Sayane repository.

## Core responsibilities

The connection layer must provide a contract for:

1. storing source documents;
2. storing chunks derived from documents;
3. storing optional embeddings;
4. running text search;
5. running vector search;
6. running hybrid search;
7. recording retrieval logs;
8. inspecting retrieval logs;
9. attaching lightweight audit summaries;
10. exporting enough evidence for article/demo verification.

## Conceptual objects

### Document

A document represents a source unit of Sayane-linked context.

Required fields:

```text
id
title
source_path
source_type
created_at
updated_at
```

### Chunk

A chunk represents a searchable piece of a document.

Required fields:

```text
id
document_id
chunk_index
content
content_hash
metadata
created_at
```

Optional fields:

```text
embedding
```

### RetrievalLog

A retrieval log records one search execution.

Required fields:

```text
id
query
mode
retrieved_chunk_ids
scores
selected_chunk_ids
audit_summary
created_at
```

### AuditSummary

A lightweight audit summary records inspectable retrieval interpretation.

Minimum fields:

```text
preserved
inferred
drift_risk
unresolved
```

This is not full RDE scoring.

## Interface operations

The connection layer should expose the following logical operations.

```text
initialize_schema()
put_document(document)
put_chunks(document_id, chunks)
ingest_path(path, embed=false)
search_text(query, limit)
search_vector(query, limit)
search_hybrid(query, limit)
record_retrieval_log(record)
list_retrieval_logs(limit)
get_retrieval_log(id)
```

Backend adapters may expose additional capabilities, but those capabilities must not become required by Sayane core unless promoted into this contract.

## Search modes

### text

Text search retrieves chunks based on lexical matching.

Expected role:

- named Sayane concepts;
- exact feature names;
- policy terms;
- candidate / lineage wording;
- audit terminology.

### vector

Vector search retrieves chunks based on semantic similarity.

Expected role:

- conceptual questions;
- paraphrases;
- queries that do not match exact document wording.

### hybrid

Hybrid search combines text and vector search results.

Expected role:

- mixed exact-term and conceptual questions;
- Sayane-specific terms plus broader semantic intent.

The merge policy must be inspectable and testable.

## Logging requirements

Every search execution should be logged.

A retrieval log must preserve:

- original query;
- search mode;
- retrieved chunk IDs;
- scores;
- selected chunk IDs;
- lightweight audit summary.

The log is part of the demo's evidence, not debug output.

## Backend adapter expectations

A backend adapter must declare which capabilities it supports.

Recommended capability flags:

```text
supports_text_search
supports_vector_search
supports_hybrid_search
supports_native_vector_index
supports_sql_audit_tables
supports_transactional_ingest
supports_portable_export
```

The current TiDB demo supports text search, JSON-based vector search, hybrid merge, SQL retrieval logs, and transactional ingest. It does not yet support TiDB-native vector-indexed search.

## Error handling

The connection layer should fail explicitly when required backend capabilities or credentials are missing.

Examples:

- missing TiDB host should fail before schema initialization;
- missing OpenAI API key should fail before embedding generation;
- vector search should fail or return a clear message if embeddings are absent;
- unsupported modes should raise explicit errors.

## RDE / Delta-M

- Preserved: Sayane remains backend-agnostic and centered on Context Store Interface.
- Transformed: backend access is formalized as a connection-layer contract.
- Added: explicit retrieval log and audit summary requirements.
- Unresolved: exact promotion path into Sayane main repository.
- Drift risk: backend-specific capabilities may leak into Sayane core unless guarded by capability flags.
