# Sayane-TiDB Basic Specification

## Status

Draft for the Sayane-linked TiDB Context Store demo.

This specification defines the basic role, responsibilities, and boundaries of a TiDB-backed Context Store adapter for Sayane-style workflows.

## Purpose

Sayane-TiDB demonstrates how Sayane Context Store concepts can be represented in a TiDB Cloud backend.

The purpose is to evaluate TiDB as a scale-out enterprise backend candidate for Sayane, especially where retrieval evidence, audit summaries, and structured context records should remain SQL-addressable.

## Positioning

Sayane-TiDB is:

- a backend adapter candidate;
- an enterprise Context Store experiment;
- a Zenn article implementation target;
- a retrieval log and lightweight audit demonstration.

Sayane-TiDB is not:

- the Sayane core;
- the only Sayane backend;
- the production Sayane backend;
- a full RDE scoring implementation;
- currently a TiDB-native vector-indexed implementation.

## Architectural placement

```text
Sayane Core
  -> Sayane Context Store Interface
      -> LocalContextStore: SQLite + DuckDB
      -> StandardEnterpriseContextStore: PostgreSQL / pgvector
      -> ScaleOutEnterpriseContextStore: TiDB Cloud
          -> Sayane-TiDB adapter
```

## Current implementation boundary

The current demo implementation stores embeddings as JSON in TiDB and calculates cosine similarity in Python.

This means the current implementation is vector-enabled but not TiDB-native vector-indexed.

TiDB-native vector search is tracked separately and must be treated as a Delta-M change because it changes schema, retrieval semantics, and article claim boundaries.

## Data model

### documents

Stores source documents.

Current fields:

```text
id VARCHAR(64) PRIMARY KEY
title TEXT
source_path TEXT
source_type VARCHAR(32)
created_at TIMESTAMP
updated_at TIMESTAMP
```

### chunks

Stores searchable chunks.

Current fields:

```text
id VARCHAR(64) PRIMARY KEY
document_id VARCHAR(64)
chunk_index INT
content TEXT
content_hash VARCHAR(128)
embedding JSON
metadata JSON
created_at TIMESTAMP
```

### retrieval_logs

Stores one log per search execution.

Current fields:

```text
id VARCHAR(64) PRIMARY KEY
query TEXT
mode VARCHAR(32)
retrieved_chunk_ids JSON
scores JSON
selected_chunk_ids JSON
audit_summary JSON
created_at TIMESTAMP
```

## Supported operations

### initialize schema

Initializes TiDB tables from SQL files.

```bash
sayane-tidb-demo init
```

### ingest context

Ingests Markdown context documents into `documents` and `chunks`.

```bash
sayane-tidb-demo ingest data/sample_docs
```

### ingest context with embeddings

Generates embeddings and stores them in `chunks.embedding`.

```bash
sayane-tidb-demo ingest data/sample_docs --embed
```

### text search

Performs lexical search over chunk content.

```bash
sayane-tidb-demo search "candidate lineage" --mode text
```

### vector search

Performs semantic search using JSON-stored embeddings and Python-side cosine similarity.

```bash
sayane-tidb-demo search "review changes before merging memory" --mode vector
```

### hybrid search

Combines text and vector results using an explicit merge policy.

```bash
sayane-tidb-demo search "Sayane candidate lineage audit" --mode hybrid
```

### retrieval log inspection

Displays recorded retrieval evidence.

```bash
sayane-tidb-demo logs
sayane-tidb-demo inspect <retrieval_id>
```

## Search semantics

### text mode

Text mode is for exact Sayane concepts and policy terms.

Examples:

```text
candidate lineage
Context Store Interface
retrieval log
```

### vector mode

Vector mode is for semantic paraphrases.

Examples:

```text
review changes before merging memory
avoid blind context updates
carry context across LLM workflows
```

### hybrid mode

Hybrid mode is for mixed exact/conceptual queries.

Examples:

```text
Sayane candidate lineage audit
enterprise backend context memory
```

Current hybrid scoring:

- text matches receive a fixed bonus;
- vector scores are added;
- duplicate text/vector hits are merged;
- results are sorted by merged score.

This merge policy is intentionally simple and testable.

## Why TiDB for this demo

TiDB is evaluated because Sayane needs auditable state, not just semantic retrieval.

The demo tests whether one backend direction can represent:

- documents;
- chunks;
- embeddings;
- retrieval logs;
- audit summaries;
- text/vector/hybrid retrieval evidence.

TiDB is especially useful as a demo target because it is SQL-first, MySQL-compatible, enterprise-oriented, and has a path toward native vector / full-text / hybrid retrieval.

## Capability declaration

Current capabilities:

```text
supports_text_search: true
supports_vector_search: true
supports_hybrid_search: true
supports_native_vector_index: false
supports_sql_audit_tables: true
supports_transactional_ingest: true
supports_portable_export: false
```

## RDE boundary

The lightweight audit summary is not full RDE scoring.

It only records retrieval-adjacent inspection fields such as:

```text
preserved
inferred
drift_risk
unresolved
```

Full RDE integration remains outside this demo.

## Migration path to Sayane core

Do not copy this demo directly into Sayane core.

Recommended migration sequence:

1. Extract `Context Store Interface` contract.
2. Extract `RetrievalLog` contract.
3. Define backend capability flags.
4. Define PostgreSQL and TiDB adapter specifications.
5. Promote only stable operations into Sayane core.
6. Keep demo-specific article code separate.

## Future work

- Replace JSON embedding storage with TiDB-native vector type.
- Replace Python cosine similarity with TiDB-native vector search.
- Add full-text search if supported in the target TiDB Cloud environment.
- Add migration strategy from LocalContextStore to TiDBContextStore.
- Define PostgreSQL parity behavior.
- Add export/import format for portable context bundles.

## RDE / Delta-M

- Preserved: Sayane remains local-first, backend-agnostic, and centered on Context Store Interface.
- Transformed: TiDB is specified as a scale-out enterprise backend adapter candidate.
- Added: concrete schema, operation, and capability boundaries for the demo.
- Unresolved: TiDB-native vector search and production integration path.
- Drift risk: demo implementation may be mistaken for the production Sayane backend unless this boundary is preserved.
