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
