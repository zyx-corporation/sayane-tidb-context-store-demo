# Lightweight RDE Development Guidelines

## Purpose

This document adapts the RDE engineering development guideline style to the Sayane TiDB Context Store Demo.

This repository is a small article prototype, not the full Sayane product. Therefore, this document is intentionally lightweight. It preserves the core engineering intent:

- design changes should be reviewed as meaning changes, not only code changes;
- implementation should leave traceable rationale;
- tests should pin down important invariants;
- retrieval and audit behavior should remain inspectable.

## Scope

This guideline applies to changes in this demo repository that affect:

- Context Store behavior;
- TiDB schema or indexing strategy;
- Markdown ingestion and chunking;
- retrieval logs;
- lightweight RDE audit summaries;
- article-facing claims about Sayane, TiDB, RAG, or AI memory.

It does not define the normative Sayane specification.

## Three RDE layers

### 1. Design layer

Before changing storage, retrieval, or audit behavior, describe the expected meaning change.

Ask:

- What user-visible behavior changes?
- Does this alter the claim made in the Zenn article?
- Does this make TiDB look like the core of Sayane rather than an adapter?
- Does this change the distinction between text search, vector search, and hybrid search?

### 2. Development layer

Implementation changes should leave traceable rationale in commits, issues, or PR descriptions.

For non-trivial changes, include a short Delta-M note:

```text
Delta-M:
- Preserved:
- Transformed:
- Added:
- Unresolved:
- Drift risk:
```

### 3. Verification layer

Tests should cover both positive and negative behavior when the change affects semantics.

Examples:

- chunking should preserve source text boundaries where possible;
- ingestion should not silently duplicate stale chunks;
- retrieval logs should record query, mode, retrieved chunks, and audit summary;
- audit output should not claim full RDE scoring when only lightweight audit is implemented.

## Review triggers

Treat the following changes as RDE review triggers:

| Category | Examples |
| --- | --- |
| Schema and persistence | `sql/*.sql`, document/chunk/retrieval log shape |
| Retrieval semantics | text/vector/hybrid search behavior, score interpretation |
| Audit behavior | `audit.py`, `retrieval_logs.audit_summary`, drift risk wording |
| Public explanation | `README.md`, `docs/zenn-article-outline.md`, article claims |
| Backend positioning | wording that changes TiDB from adapter to Sayane core |

When unsure, treat the change as a trigger.

## Design and implementation guidance

Use abstraction only where it helps this demo remain readable and extensible.

Recommended boundaries:

- `config.py`: environment and settings;
- `db.py`: database connection;
- `schema.py`: schema initialization;
- `ingest.py`: document and chunk ingestion;
- `search.py`: retrieval behavior;
- `audit.py`: lightweight audit summary;
- `cli.py`: command boundary.

Avoid premature architecture. The goal is a reproducible Level C article prototype, not a product-scale framework.

## Suppression patterns

Avoid the following:

- presenting lightweight audit as full RDE implementation;
- making TiDB appear to be the theoretical center of Sayane;
- adding flexible JSON fields that look like normative schema without explanation;
- adding only positive examples while leaving failure modes untested;
- changing schema or retrieval behavior without updating the article outline.

## PR / commit note template

```text
Summary:

Delta-M:
- Preserved:
- Transformed:
- Added:
- Unresolved:
- Drift risk:

Tests:
- Positive:
- Negative:

Article impact:
```

## Current demo stance

This repository should keep the following claims stable:

- Sayane is centered on the Context Store Interface.
- TiDB Cloud is one backend adapter used for this implementation article.
- The demo uses lightweight RDE-style audit, not full RDE scoring.
- Retrieval should be logged and inspectable after generation.
- Local Sayane and enterprise Sayane remain separate design concerns.
