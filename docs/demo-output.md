# Demo Output Capture

## Purpose

This file captures concrete command outputs for the Zenn article.

Do not invent outputs. Replace the placeholders below only after running the commands against a real TiDB Cloud environment.

## Environment

```text
Date:
Python version:
TiDB Cloud plan:
TiDB region:
Embedding model:
```

## 1. Schema initialization

Command:

```bash
make init
```

Output:

```text
TODO: paste real output here
```

## 2. Markdown ingestion without embeddings

Command:

```bash
make ingest
```

Output:

```text
TODO: paste real output here
```

## 3. Text search

Command:

```bash
make search-text
```

Output:

```text
TODO: paste real output here
```

## 4. Markdown ingestion with embeddings

Command:

```bash
make ingest-embed
```

Output:

```text
TODO: paste real output here
```

## 5. Vector search

Command:

```bash
make search-vector
```

Output:

```text
TODO: paste real output here
```

## 6. Hybrid search

Command:

```bash
make search-hybrid
```

Output:

```text
TODO: paste real output here
```

## 7. Retrieval logs

Command:

```bash
make logs
```

Output:

```text
TODO: paste real output here
```

## Notes for article use

- Confirm that retrieval IDs are visible.
- Confirm that audit summaries are visible.
- Confirm that text, vector, and hybrid modes produce distinguishable behavior.
- Do not claim TiDB-native vector index usage unless Issue #1 is completed.
