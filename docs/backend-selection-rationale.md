# Backend Selection Rationale

## Purpose

This document explains why the demo intentionally evaluates TiDB Cloud as a Sayane-linked enterprise Context Store backend, rather than using a generic vector SaaS backend.

The goal is not to claim that TiDB is universally better than vector databases or Postgres-based services. The goal is to make the selection criteria explicit for Sayane's use case.

## Sayane-specific selection question

Sayane does not only need semantic search.

A Sayane-linked Context Store must be able to represent and inspect:

- canonical context documents;
- chunks;
- metadata;
- candidate / lineage concepts;
- retrieval logs;
- lightweight audit summaries;
- text search results;
- vector search results;
- hybrid retrieval evidence.

Therefore, the key question is:

> Which backend best demonstrates an enterprise-grade, SQL-addressable, auditable Context Store for Sayane-style AI memory?

## Why TiDB is interesting for this demo

TiDB is interesting because it can be positioned as a SQL-first enterprise backend where structured data and retrieval evidence live together.

For this demo, the important properties are:

1. SQL-addressable storage for documents, chunks, retrieval logs, and audit summaries.
2. A path toward vector search and full-text / hybrid search in the same database family.
3. MySQL-compatible access patterns, which are easy to demonstrate from a small Python CLI.
4. Enterprise-oriented scaling and managed deployment options.
5. A clear contrast with specialized vector SaaS products.

## Comparison with other SaaS backends

| Backend type | Strength | Limitation for this Sayane demo |
| --- | --- | --- |
| Specialized vector DB SaaS such as Pinecone | Strong vector-native and hybrid retrieval features | The main abstraction is usually records/vectors plus metadata, so candidate, lineage, retrieval logs, and audit tables must be modeled around the vector index rather than as first-class SQL tables. |
| Vector-native knowledge SaaS such as Weaviate Cloud | Strong vector + keyword hybrid search and AI-oriented object model | Excellent for retrieval experiments, but less aligned with demonstrating a SQL-addressable audit/log contract for Sayane. |
| Postgres SaaS such as Supabase / Neon + pgvector | Very strong fit for SQL, relational metadata, and enterprise familiarity | This is the conservative enterprise backend candidate, but it does not demonstrate TiDB's distributed SQL / HTAP-oriented differentiation. |
| Search SaaS such as Algolia / Typesense / Elastic Cloud / OpenSearch | Strong lexical search, faceting, and search UX | Usually needs a separate source-of-truth database for lineage and audit semantics. |
| TiDB Cloud | SQL-first, MySQL-compatible, distributed SQL backend with a path toward vector and hybrid retrieval | More work is needed to confirm and implement native vector search in this demo; current implementation is still JSON embedding + Python cosine scoring. |

## The actual claim

The article should make this claim:

> TiDB is worth testing for Sayane because it lets us explore an enterprise Context Store where context records, retrieval logs, and audit summaries are SQL-addressable, while still having a path toward vector / full-text / hybrid retrieval.

The article should not make these claims:

> TiDB is always better than Pinecone, Weaviate, Qdrant, Supabase, or Neon.

> TiDB is the only possible Sayane backend.

> Sayane is TiDB-based.

## Backend positioning in Sayane

Recommended positioning:

```text
Sayane Context Store Interface
  -> LocalContextStore: SQLite + DuckDB
  -> Standard EnterpriseContextStore: PostgreSQL / pgvector
  -> Scale-out EnterpriseContextStore: TiDB Cloud
  -> Retrieval-specialized adapter: optional vector/search SaaS
```

TiDB is therefore not the core. It is a scale-out enterprise backend candidate.

## Demo-specific angle

For this Zenn demo, the useful contrast is:

- A vector SaaS backend demonstrates retrieval quality.
- A SQL SaaS backend demonstrates auditable state.
- TiDB Cloud is being tested because Sayane needs both retrieval and auditable state in one enterprise-friendly Context Store direction.

## RDE / Delta-M

- Preserved: Sayane remains backend-agnostic and centered on Context Store Interface.
- Transformed: TiDB is given a clearer role as a scale-out enterprise backend candidate.
- Added: comparison criteria against vector SaaS, Postgres SaaS, and search SaaS.
- Unresolved: empirical benchmark against these alternatives is not implemented in this repository.
- Drift risk: comparison language may turn into vendor advocacy. Keep the claim bounded to Sayane's Context Store use case.
