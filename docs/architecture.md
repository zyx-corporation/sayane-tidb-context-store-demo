# Architecture

## Purpose

This repository demonstrates a minimal TiDB Cloud backed Context Store for Sayane.

The prototype is scoped as a Level C article implementation: a small working sample, search comparison, and retrieval logging.

## Core idea

Sayane should not depend on a specific database product. The core abstraction is the Sayane Context Store Interface. This demo validates one concrete backend: TiDB Cloud.

```text
CLI / simple UI
  -> ContextStore interface
      -> TiDBContextStore
          -> documents
          -> chunks
          -> retrieval_logs
          -> audit summaries
```

## Data flow

```text
Markdown files
  -> chunker
  -> embedding provider
  -> TiDB Cloud
  -> text / vector / hybrid search
  -> retrieval logs
  -> lightweight audit summary
```

## Current vector search stance

The current implementation stores embeddings as JSON in TiDB and calculates cosine similarity in Python.

This is a deliberate intermediate step for the Level C article prototype. It allows the demo to compare text, vector, and hybrid retrieval before adopting TiDB native vector index syntax.

A later step should replace the Python-side vector scoring with TiDB Cloud native vector search after confirming the target cluster capabilities and SQL syntax.

This distinction must remain clear in the article: the current implementation is vector-enabled, but not yet TiDB-native vector-indexed.
