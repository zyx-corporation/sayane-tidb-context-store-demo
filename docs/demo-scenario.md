# Demo Scenario

## Title

From captured context to auditable retrieval: a Sayane-linked TiDB Context Store demo

## Purpose

This scenario explains the story that the demo should prove.

The demo is not just "RAG on TiDB". It is a Sayane-linked empirical demonstration that shows how local-first context, candidate review, lineage, retrieval logs, and lightweight audit summaries can be represented in an enterprise Context Store backend.

## Core claim

Sayane needs more than semantic search.

A useful enterprise Context Store for Sayane must store and inspect:

- context documents;
- chunks;
- candidate and lineage concepts;
- text/vector/hybrid retrieval results;
- retrieval logs;
- lightweight audit summaries.

TiDB Cloud is selected for this demo because it lets us test a SQL-addressable, auditable state model while still leaving a path toward vector / full-text / hybrid retrieval.

## Scenario overview

A user is developing Sayane and wants to carry reviewed context across LLM workflows.

The user has several Sayane-related documents:

- local-first context workflow;
- candidate review and lineage;
- enterprise backend positioning;
- lightweight retrieval audit;
- backend selection rationale.

These documents are ingested into a TiDB-backed Context Store. The demo then asks three types of questions.

1. A keyword-heavy question that should be answered well by text search.
2. A concept-heavy question that should be answered better by vector search.
3. A mixed question that should benefit from hybrid search.

Every search is recorded as a retrieval log so that the evidence can be inspected after the query.

## Actor

The actor is a Sayane user or developer evaluating whether Sayane's local-first workflow can be extended into an enterprise Context Store backend.

## Data set

The demo uses `data/sample_docs/` as a small Sayane-linked corpus.

Recommended files:

```text
data/sample_docs/sayane-local.md
data/sample_docs/sayane-enterprise.md
data/sample_docs/sayane-candidate-lineage.md
data/sample_docs/rde-audit.md
data/sample_docs/sayane-backend-selection.md  # optional future addition
```

## Step 1: Initialize Context Store schema

Command:

```bash
make init
```

Meaning:

The demo creates SQL-addressable tables for documents, chunks, and retrieval logs.

This shows the first difference from a pure vector SaaS demo: the Context Store is not just a vector index. It is a structured state store for retrieval and audit evidence.

## Step 2: Ingest Sayane-linked context without embeddings

Command:

```bash
make ingest
```

Meaning:

The demo stores Sayane-related documents and chunks in TiDB.

This proves that Sayane concepts can be represented as structured context records before any semantic search is involved.

## Step 3: Text search for exact concepts

Command:

```bash
sayane-tidb-demo search "candidate lineage" --mode text
```

Expected meaning:

Text search should find chunks that explicitly mention candidate and lineage.

Demo claim:

Exact Sayane terms remain important. Vector search alone is not enough when the user asks about named concepts, feature names, or policy terms.

## Step 4: Ingest embeddings

Command:

```bash
make ingest-embed
```

Meaning:

The same context is enriched with embeddings.

Current boundary:

Embeddings are stored as JSON and scored in Python. This is vector-enabled but not yet TiDB-native vector-indexed.

## Step 5: Vector search for conceptual similarity

Command:

```bash
sayane-tidb-demo search "review changes before merging memory" --mode vector
```

Expected meaning:

Vector search should find content related to candidate evaluation, blind merge prevention, and lineage even when the query does not exactly match the document wording.

Demo claim:

Vector search helps when a user asks conceptually, not lexically.

## Step 6: Hybrid search for mixed questions

Command:

```bash
sayane-tidb-demo search "Sayane candidate lineage audit" --mode hybrid
```

Expected meaning:

Hybrid search should combine exact Sayane terms with semantically related retrieval.

Demo claim:

Hybrid retrieval needs an explicit merge policy. The demo makes the merge policy inspectable rather than hiding it inside an opaque retrieval service.

## Step 7: Inspect retrieval logs

Command:

```bash
make logs
sayane-tidb-demo inspect <retrieval_id>
```

Expected meaning:

The user can inspect:

- query;
- mode;
- retrieved chunk IDs;
- scores;
- selected chunk IDs;
- lightweight audit summary.

Demo claim:

RAG should not only return an answer. It should preserve retrieval evidence so that the result can be audited later.

## What this proves

This scenario proves that:

1. Sayane-linked context can be represented as structured documents and chunks.
2. Text search, vector search, and hybrid search expose different retrieval behavior.
3. Retrieval logs can preserve evidence for later audit.
4. Lightweight audit summaries can be stored beside retrieval state.
5. TiDB can be evaluated as a scale-out enterprise Context Store backend candidate.

## What this does not prove

This scenario does not prove:

- Sayane production backend compatibility;
- full RDE scoring;
- TiDB-native vector-indexed retrieval;
- production auth or multi-user tenancy;
- superiority over every vector SaaS or Postgres backend.

## Article narrative

The article should follow this arc:

1. Sayane already treats context as something that must be reviewed, carried, and audited.
2. Enterprise AI memory needs a backend that can store more than vectors.
3. TiDB Cloud is tested as a SQL-addressable Context Store backend.
4. The demo ingests Sayane-linked context.
5. It compares text, vector, and hybrid retrieval.
6. It records retrieval logs and lightweight audit summaries.
7. The result is not "Sayane is TiDB-based", but "TiDB is a plausible scale-out enterprise backend candidate for Sayane Context Store Interface".

## RDE / Delta-M

- Preserved: Sayane remains local-first and backend-agnostic.
- Transformed: Sayane concepts are represented in a TiDB-backed empirical demo.
- Added: a concrete demonstration scenario for retrieval logs and audit summaries.
- Unresolved: native TiDB vector search and production backend compatibility.
- Drift risk: the scenario may be read as vendor advocacy unless the claim remains bounded to Sayane's enterprise Context Store use case.
