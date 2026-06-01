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

## 1. Backend capabilities

Command:

```bash
sayane-tidb-demo capabilities
```

Output:

```text
{
    'backend_id': 'sayane-tidb-json-vector-demo',
    'supports_lexical_search': True,
    'supports_vector_search': True,
    'supports_hybrid_search': True,
    'supports_native_vector_index': False,
    'supports_full_text_index': False,
    'supports_sql_queries': True,
    'supports_transactional_ingest': True,
    'supports_audit_log_tables': True,
    'supports_portable_export': False,
    'supports_multi_user_access': False,
    'supports_cloud_managed_operations': True,
    'supports_local_first_storage': False,
    'supports_event_lineage': True
}
```

This command does not require TiDB or OpenAI credentials.

## 2. Schema initialization

Command:

```bash
make init
```

Output:

```text
Initialized schema: 6 statements executed
```

## 3. Markdown ingestion without embeddings

Command:

```bash
make ingest
```

Output:

```text
sayane-tidb-demo ingest data/sample_docs

data/sample_docs/rde-audit.md: 1 chunks, 0 embeddings ->
5d10ccc2e291bdafe97f2ec16864da27
data/sample_docs/sayane-candidate-lineage.md: 1 chunks, 0 embeddings ->
e997c41bef28a129261ef3443180a672
data/sample_docs/sayane-enterprise.md: 1 chunks, 0 embeddings ->
ad1f70369396bc9164ed67d77818b7ee
data/sample_docs/sayane-local.md: 1 chunks, 0 embeddings ->
43f1f5683d698418fe2c4de02105948b
```

## 4. Text search

Command:

```bash
make search-text
```

Output:

```text
sayane-tidb-demo search "TiDB" --mode text
Retrieval ID: 4445e8ff-d2c2-45b5-a7d8-a99415810795
Mode: text
Results: 2
1. ad1f70369396bc9164ed67d77818b7ee-0 score=1.0 :: # Sayane Enterprise Edition
Sayane Enterprise provides two backend families.  PostgreSQL is the standard
enterprise backend. It is suitable for conservative en
2. e997c41bef28a129261ef3443180a672-0 score=1.0 :: # Sayane Candidate and
Lineage  Sayane treats captured context as a candidate before it becomes
canonical context.  A captured insight should not be merged blin
{
    'audit_summary': {
        'preserved': ['retrieved source chunks are logged'],
        'inferred': [],
        'drift_risk': 'low',
        'unresolved': ['full RDE scoring is outside this demo']
    }
}
```

## 5. Markdown ingestion with embeddings

Command:

```bash
make ingest-embed
```

Output:

```text
sayane-tidb-demo ingest data/sample_docs --embed
data/sample_docs/rde-audit.md: 1 chunks, 1 embeddings ->
5d10ccc2e291bdafe97f2ec16864da27
data/sample_docs/sayane-candidate-lineage.md: 1 chunks, 1 embeddings ->
e997c41bef28a129261ef3443180a672
data/sample_docs/sayane-enterprise.md: 1 chunks, 1 embeddings ->
ad1f70369396bc9164ed67d77818b7ee
data/sample_docs/sayane-local.md: 1 chunks, 1 embeddings ->
43f1f5683d698418fe2c4de02105948b
```

## 6. Vector search

Command:

```bash
make search-vector
```

Output:

```text
sayane-tidb-demo search "Context Store Interface" --mode vector
Retrieval ID: d9a2052f-7774-478b-9c6a-c35ed92a62e8
Mode: vector
Results: 4
1. e997c41bef28a129261ef3443180a672-0 score=0.3266898897604514 :: # Sayane
Candidate and Lineage  Sayane treats captured context as a candidate before it
becomes canonical context.  A captured insight should not be merged blin
2. ad1f70369396bc9164ed67d77818b7ee-0 score=0.2847524986776959 :: # Sayane
Enterprise Edition  Sayane Enterprise provides two backend families.  PostgreSQL
is the standard enterprise backend. It is suitable for conservative en
3. 43f1f5683d698418fe2c4de02105948b-0 score=0.2559699414987857 :: # Sayane Local
Edition  Sayane Local uses SQLite as the primary local context store and DuckDB
as the local analytics store.  SQLite stores documents, chunks, s
4. 5d10ccc2e291bdafe97f2ec16864da27-0 score=0.17314136607114844 :: # Lightweight
RDE Audit  RDE in this demo means a lightweight audit record for retrieval
results.  The audit summary does not implement the full RDE theory. It
{
    'audit_summary': {
        'preserved': ['retrieved source chunks are logged'],
        'inferred': [],
        'drift_risk': 'low',
        'unresolved': ['full RDE scoring is outside this demo']
    }
}
```

## 7. Hybrid search

Command:

```bash
make search-hybrid
```

Output:

```text
sayane-tidb-demo search "enterprise backend" --mode hybrid
Retrieval ID: 009e9bcb-544e-4b2c-8592-385022210dca
Mode: hybrid
Results: 4
1. ad1f70369396bc9164ed67d77818b7ee-0 score=1.9620616067552754 :: # Sayane
Enterprise Edition  Sayane Enterprise provides two backend families.  PostgreSQL
is the standard enterprise backend. It is suitable for conservative en
2. 43f1f5683d698418fe2c4de02105948b-0 score=0.33496512992382727 :: # Sayane
Local Edition  Sayane Local uses SQLite as the primary local context store and
DuckDB as the local analytics store.  SQLite stores documents, chunks, s
3. e997c41bef28a129261ef3443180a672-0 score=0.24866572848418408 :: # Sayane
Candidate and Lineage  Sayane treats captured context as a candidate before it
becomes canonical context.  A captured insight should not be merged blin
4. 5d10ccc2e291bdafe97f2ec16864da27-0 score=0.22215284394785698 :: # Lightweight
RDE Audit  RDE in this demo means a lightweight audit record for retrieval
results.  The audit summary does not implement the full RDE theory. It
{
    'audit_summary': {
        'preserved': ['retrieved source chunks are logged'],
        'inferred': [],
        'drift_risk': 'low',
        'unresolved': ['full RDE scoring is outside this demo']
    }
}
```

## 8. Retrieval logs

Command:

```bash
make logs
```

Output:

```text
sayane-tidb-demo logs

{
    'id': '22054f3b-caf5-4b23-b319-75eea6148ecd',
    'query': 'enterprise backend',
    'mode': 'hybrid',
    'retrieved_chunk_ids': '["ad1f70369396bc9164ed67d77818b7ee-0",
"43f1f5683d698418fe2c4de02105948b-0", "e997c41bef28a129261ef3443180a672-0",
"5d10ccc2e291bdafe97f2ec16864da27-0"]',
    'audit_summary': '{"drift_risk": "low", "inferred": [], "preserved":
["retrieved source chunks are logged"], "unresolved": ["full RDE scoring is
outside this demo"]}',
    'backend_capabilities': '{"backend_id": "sayane-tidb-json-vector-demo",
"supports_audit_log_tables": true, "supports_cloud_managed_operations": true,
"supports_event_lineage": true, "supports_full_text_index": false,
"supports_hybrid_search": true, "supports_lexical_search": true,
"supports_local_first_storage": false, "supports_multi_user_access": false,
"supports_native_vector_index": false, "supports_portable_export": false,
"supports_sql_queries": true, "supports_transactional_ingest": true,
"supports_vector_search": true}',
    'created_at': datetime.datetime(2026, 6, 1, 7, 42, 9)
}
{
    'id': 'd9a2052f-7774-478b-9c6a-c35ed92a62e8',
    'query': 'Context Store Interface',
    'mode': 'vector',
    'retrieved_chunk_ids': '["e997c41bef28a129261ef3443180a672-0",
"ad1f70369396bc9164ed67d77818b7ee-0", "43f1f5683d698418fe2c4de02105948b-0",
"5d10ccc2e291bdafe97f2ec16864da27-0"]',
    'audit_summary': '{"drift_risk": "low", "inferred": [], "preserved":
["retrieved source chunks are logged"], "unresolved": ["full RDE scoring is
outside this demo"]}',
    'backend_capabilities': '{"backend_id": "sayane-tidb-json-vector-demo",
"supports_audit_log_tables": true, "supports_cloud_managed_operations": true,
"supports_event_lineage": true, "supports_full_text_index": false,
"supports_hybrid_search": true, "supports_lexical_search": true,
"supports_local_first_storage": false, "supports_multi_user_access": false,
"supports_native_vector_index": false, "supports_portable_export": false,
"supports_sql_queries": true, "supports_transactional_ingest": true,
"supports_vector_search": true}',
    'created_at': datetime.datetime(2026, 6, 1, 7, 41, 38)
}
{
    'id': '4445e8ff-d2c2-45b5-a7d8-a99415810795',
    'query': 'TiDB',
    'mode': 'text',
    'retrieved_chunk_ids': '["ad1f70369396bc9164ed67d77818b7ee-0",
"e997c41bef28a129261ef3443180a672-0"]',
    'audit_summary': '{"drift_risk": "low", "inferred": [], "preserved":
["retrieved source chunks are logged"], "unresolved": ["full RDE scoring is
outside this demo"]}',
    'backend_capabilities': '{"backend_id": "sayane-tidb-json-vector-demo",
"supports_audit_log_tables": true, "supports_cloud_managed_operations": true,
"supports_event_lineage": true, "supports_full_text_index": false,
"supports_hybrid_search": true, "supports_lexical_search": true,
"supports_local_first_storage": false, "supports_multi_user_access": false,
"supports_native_vector_index": false, "supports_portable_export": false,
"supports_sql_queries": true, "supports_transactional_ingest": true,
"supports_vector_search": true}',
    'created_at': datetime.datetime(2026, 6, 1, 7, 39, 52)
}
```

## Notes for article use

- Confirm that retrieval IDs are visible.
- Confirm that audit summaries are visible.
- Confirm that backend capability snapshots are visible in retrieval logs.
- Confirm that text, vector, and hybrid modes produce distinguishable behavior.
- Do not claim TiDB-native vector index usage unless Issue #1 is completed.
- Do not claim full T-RDE scoring; lightweight audit only.

