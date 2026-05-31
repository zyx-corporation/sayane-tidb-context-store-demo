# Article Implementation Notes

## Current implementation level

This repository currently implements a Level C prototype:

- small working CLI;
- Markdown ingestion;
- chunking;
- TiDB-backed document and chunk storage;
- optional embedding generation;
- text search;
- JSON-embedding vector search evaluated in Python;
- hybrid search result merging;
- retrieval logs;
- lightweight RDE-style audit summary;
- unit tests and CI.

## Important claim boundary

The current vector search implementation is vector-enabled but not yet TiDB-native vector-indexed.

Embeddings are stored in TiDB as JSON, then loaded by Python for cosine similarity scoring. This is useful for validating the retrieval pipeline and comparing text, vector, and hybrid search behavior before adopting TiDB Cloud native vector search syntax.

The article must not claim that this version uses TiDB native vector indexes.

## Why this intermediate design is useful

This stage keeps the prototype reproducible and easy to inspect:

- text search works without embeddings;
- vector search works after `--embed` ingestion;
- hybrid search can be evaluated as a deterministic merge of text and vector results;
- retrieval logs show what was retrieved and how the lightweight audit evaluated it.

## Demo flow

```bash
sayane-tidb-demo init
sayane-tidb-demo ingest data/sample_docs
sayane-tidb-demo search "TiDB" --mode text

sayane-tidb-demo ingest data/sample_docs --embed
sayane-tidb-demo search "Context Store Interface" --mode vector
sayane-tidb-demo search "enterprise backend" --mode hybrid
sayane-tidb-demo logs
```

## Article thesis

RAG is not only retrieval. A useful AI memory foundation should record retrieval decisions and keep them inspectable.

This demo shows that a Context Store can unify:

- source documents;
- chunks;
- embeddings;
- search results;
- retrieval logs;
- lightweight audit summaries.

## Engineering lessons to highlight

1. Text search and vector search solve different failure modes.
2. Hybrid search needs an explicit merge policy.
3. Retrieval logs are part of the product, not debug output.
4. Lightweight audit must not be described as full RDE scoring.
5. TiDB should be presented as a backend adapter, not the theoretical center of Sayane.

## Next implementation step

Replace JSON embedding storage and Python cosine scoring with TiDB Cloud native vector search after confirming the target cluster capabilities and SQL syntax.

That step should be implemented as a separate Delta-M change because it changes retrieval semantics and the article claim boundary.
