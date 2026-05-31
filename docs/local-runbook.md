# Local Runbook

## Purpose

This runbook describes how to run the Sayane TiDB Context Store Demo locally.

The current implementation supports:

- schema initialization;
- Markdown ingestion;
- optional embedding generation;
- text search;
- JSON-embedding vector search evaluated in Python;
- hybrid search;
- retrieval log inspection.

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Or use:

```bash
make install
```

## 2. Configure environment

Copy the example file and fill in local values.

```bash
cp .env.example .env
```

Required for TiDB access:

```env
TIDB_HOST=
TIDB_PORT=4000
TIDB_USER=
TIDB_PASSWORD=
TIDB_DATABASE=sayane_context_demo
TIDB_SSL_CA=
```

Required only when using `--embed`, `--mode vector`, or `--mode hybrid`:

```env
OPENAI_API_KEY=
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIM=1536
```

## 3. Initialize schema

```bash
sayane-tidb-demo init
# or
make init
```

This command executes SQL files under `sql/`.

## 4. Ingest without embeddings

```bash
sayane-tidb-demo ingest data/sample_docs
# or
make ingest
```

This is enough for text search.

```bash
sayane-tidb-demo search "TiDB" --mode text
# or
make search-text
```

## 5. Ingest with embeddings

```bash
sayane-tidb-demo ingest data/sample_docs --embed
# or
make ingest-embed
```

This requires `OPENAI_API_KEY`.

After this, vector and hybrid modes can run.

```bash
sayane-tidb-demo search "Context Store Interface" --mode vector
sayane-tidb-demo search "enterprise backend" --mode hybrid
# or
make search-vector
make search-hybrid
```

## 6. Inspect retrieval logs

```bash
sayane-tidb-demo logs
sayane-tidb-demo inspect <retrieval_id>
# or
make logs
```

## Current implementation boundary

Vector mode is currently implemented as JSON embedding storage in TiDB plus Python-side cosine similarity.

It is not yet TiDB-native vector-indexed search. See `docs/article-implementation-notes.md` and Issue #1 before changing article claims.

## Expected article demo path

For the Zenn article, the simplest reproducible flow is:

```bash
make init
make ingest
make search-text
make ingest-embed
make search-vector
make search-hybrid
make logs
```
