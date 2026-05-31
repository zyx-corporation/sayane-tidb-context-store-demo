# Sayane Integration Demo Plan

## Purpose

This document reframes the TiDB demo as an empirical extension demo for Sayane.

The goal is not to present TiDB as the center of Sayane. The goal is to demonstrate that Sayane's local-first context, candidate review, audit trail, and lineage ideas can be extended into an enterprise-grade Context Store backend.

## Relationship to Sayane core

Sayane core focuses on:

- local canonical persona and context;
- prompt compilation across LLM runtimes;
- captured context as reviewable candidates;
- evaluation before merge;
- accepted/rejected lineage records;
- portable and inspectable workflows.

This demo focuses on one empirical question:

> Can Sayane-style context, retrieval, and audit trails be represented in a TiDB-backed Context Store suitable for enterprise RAG / AI memory use cases?

## Demo framing

The demo should be presented as:

```text
Sayane local-first workflow
  -> exported / sample context documents
  -> TiDB-backed Context Store
  -> text / vector / hybrid retrieval
  -> retrieval logs
  -> lightweight audit summary
  -> article evidence and future backend design
```

## What is being proven

This demo empirically checks the following claims:

1. Sayane context can be chunked and stored in a structured Context Store.
2. Context retrieval can be inspected after the fact through retrieval logs.
3. Text, vector, and hybrid search expose different failure modes.
4. A lightweight audit hook can preserve the boundary between retrieval evidence and generated conclusions.
5. TiDB can be evaluated as an enterprise backend adapter without becoming the theoretical center of Sayane.

## What is not being proven

This demo does not prove:

- full Sayane backend compatibility;
- full RDE scoring;
- TiDB-native vector-indexed search;
- production multi-user auth;
- migration compatibility with the main Sayane repository.

Those remain future integration tasks.

## Minimal Sayane-linked dataset

The sample documents should represent Sayane concepts, not generic filler.

Recommended documents:

- Sayane local-first context workflow;
- candidate evaluation and lineage;
- Context Store Interface and backend adapters;
- retrieval log and lightweight audit;
- enterprise backend positioning.

## Integration path back to Sayane

The demo can feed the main Sayane repository through documents and contracts before code migration.

Recommended extraction targets:

```text
docs/context-store-interface.md
docs/retrieval-log-contract.md
docs/backends/tidb-context-store.md
docs/backends/postgresql-context-store.md
```

## RDE / Delta-M

- Preserved: Sayane remains local-first and centered on context portability, candidate review, and lineage.
- Transformed: Sayane's storage/audit ideas are tested against an enterprise database backend.
- Added: empirical retrieval logs and search mode comparison.
- Unresolved: exact boundary between Sayane local storage and enterprise Context Store backend.
- Drift risk: TiDB may be mistaken as Sayane's core rather than one backend adapter.

## Article positioning

The Zenn article should say:

> This is a Sayane-linked empirical demo. It uses TiDB Cloud to test how a Sayane-style Context Store can store chunks, run retrieval, and preserve retrieval logs for later audit.

The article should not say:

> Sayane is TiDB-based.

or:

> This demo is the Sayane production backend.
