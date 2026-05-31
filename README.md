# Sayane TiDB Context Store Demo

A minimal TiDB Cloud backed Context Store demo for Sayane.

This repository is a Level C prototype for a Zenn technical article: a small working sample with search comparison and retrieval logging.

## Goal

Build a minimal Context Store that demonstrates Markdown ingestion, chunking, TiDB Cloud schema setup, text search, vector search, hybrid search, retrieval logging, and lightweight RDE-style audit summaries.

This is not the full Sayane implementation. It is a focused prototype for validating the Sayane Context Store Interface with TiDB Cloud.

## Engineering stance

Development follows a lightweight RDE engineering policy for this demo. See [`docs/engineering/rde-development-guidelines.md`](docs/engineering/rde-development-guidelines.md).

## Runbook

See [`docs/local-runbook.md`](docs/local-runbook.md) for local setup and demo execution steps.

## Article notes

See [`docs/article-implementation-notes.md`](docs/article-implementation-notes.md) for the current implementation boundary and article claim scope.

## Demo output

See [`docs/demo-output.md`](docs/demo-output.md) for real command output capture.

## Zenn draft

See [`docs/zenn-article-draft.md`](docs/zenn-article-draft.md) for the initial article draft.

## Planned CLI

```bash
sayane-tidb-demo init
sayane-tidb-demo ingest data/sample_docs
sayane-tidb-demo ingest data/sample_docs --embed
sayane-tidb-demo search "Sayane local backend" --mode text
sayane-tidb-demo search "Context Store Interface" --mode vector
sayane-tidb-demo search "TiDB enterprise backend" --mode hybrid
sayane-tidb-demo logs
sayane-tidb-demo inspect <retrieval_id>
```
