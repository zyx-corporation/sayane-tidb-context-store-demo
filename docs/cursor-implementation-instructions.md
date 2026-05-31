# Cursor Implementation Instructions

## Purpose

This document is an implementation instruction file for Cursor.

The goal is to improve the Sayane-TiDB Context Store demo toward `OCSI-Basic` while preserving the current design boundaries:

- OCSI is backend-agnostic.
- Sayane-TiDB is an adapter/demo, not Sayane core.
- Current vector search is JSON embedding + Python cosine scoring, not TiDB-native vector index.
- T-RDE compatibility is required as evidence preservation, not as mandatory heavy evaluation on every operation.
- OCSI core must remain evidence-centered and must not become a fat interface.

## Read these documents first

Before implementing, read the following files in this repository:

```text
docs/specs/open-context-store-interface.md
docs/specs/ocsi-t-rde-requirement.md
docs/specs/ocsi-interface-minimality-principles.md
docs/specs/ocsi-compliance-checklist.md
docs/specs/connection-layer-spec.md
docs/specs/sayane-tidb-basic-spec.md
docs/engineering/rde-development-guidelines.md
docs/demo-scenario.md
docs/article-implementation-notes.md
```

## Current implementation status

The current implementation already includes:

- CLI command: `sayane-tidb-demo`
- schema initialization
- Markdown ingestion
- optional embedding generation
- text search
- JSON embedding vector search using Python cosine similarity
- hybrid merge policy
- retrieval log storage
- lightweight audit summary
- unit tests and CI

Current status should be described as:

```text
OCSI-Experimental approaching OCSI-Basic
```

Do not describe the implementation as:

```text
OCSI-compliant
OCSI-T-RDE-Ready
audit-grade
TiDB-native vector-indexed
Sayane production backend
```

## Primary implementation goal

Move the implementation closer to `OCSI-Basic` by adding missing evidence fields and capability reporting without over-expanding the interface.

The next implementation target is:

```text
OCSI-Basic evidence preservation for SourceRecord, SearchUnit, RetrievalEvent, AuditSummary, and BackendCapability.
```

## Required tasks

### Task 1: Add backend capability reporting

Add a module:

```text
src/sayane_tidb_demo/capabilities.py
```

Define a dataclass or Pydantic model named `BackendCapabilities`.

Minimum fields:

```text
backend_id
supports_lexical_search
supports_vector_search
supports_hybrid_search
supports_native_vector_index
supports_full_text_index
supports_sql_queries
supports_transactional_ingest
supports_audit_log_tables
supports_portable_export
supports_multi_user_access
supports_cloud_managed_operations
supports_local_first_storage
supports_event_lineage
```

For the current Sayane-TiDB demo, return:

```text
backend_id: sayane-tidb-json-vector-demo
supports_lexical_search: true
supports_vector_search: true
supports_hybrid_search: true
supports_native_vector_index: false
supports_full_text_index: false
supports_sql_queries: true
supports_transactional_ingest: true
supports_audit_log_tables: true
supports_portable_export: false
supports_multi_user_access: false
supports_cloud_managed_operations: true
supports_local_first_storage: false
supports_event_lineage: true
```

Add a function:

```python
def get_backend_capabilities() -> BackendCapabilities:
    ...
```

### Task 2: Add CLI command for capabilities

Update:

```text
src/sayane_tidb_demo/cli.py
```

Add command:

```bash
sayane-tidb-demo capabilities
```

Expected behavior:

- prints backend capabilities as a readable dict or JSON-like object;
- does not require TiDB connection;
- does not require OpenAI API key.

Update README and local runbook to include:

```bash
sayane-tidb-demo capabilities
```

### Task 3: Store backend capability snapshot in retrieval logs

Update schema:

```text
sql/001_create_tables.sql
```

Add a column to `retrieval_logs`:

```sql
backend_capabilities JSON
```

Because this is a demo repository, it is acceptable to update the initial schema directly. If adding a migration file, make it simple and document it.

Update:

```text
src/sayane_tidb_demo/search.py
```

When recording a retrieval log, store current backend capabilities as JSON.

Update `get_retrieval_log()` and `list_retrieval_logs()` if needed so capability evidence remains inspectable.

### Task 4: Record embedding metadata per chunk

Update schema:

```text
sql/001_create_tables.sql
```

Add optional columns to `chunks`:

```sql
embedding_model TEXT
embedding_provider TEXT
```

Update:

```text
src/sayane_tidb_demo/ingest.py
```

When `--embed` is used, store:

```text
embedding_model = settings.embedding_model
embedding_provider = openai
```

When `--embed` is not used, store null values.

This is needed for T-RDE evidence at the embedding checkpoint.

### Task 5: Record chunking strategy per chunk

Update schema:

```text
sql/001_create_tables.sql
```

Add optional column to `chunks`:

```sql
chunking_strategy TEXT
```

Current value:

```text
paragraph-boundary-max-chars-1200
```

Update:

```text
src/sayane_tidb_demo/chunker.py
src/sayane_tidb_demo/ingest.py
```

Do not over-engineer this. A constant is enough for this demo.

Example:

```python
CHUNKING_STRATEGY = "paragraph-boundary-max-chars-1200"
```

### Task 6: Add source hash to documents

Update schema:

```text
sql/001_create_tables.sql
```

Add column to `documents`:

```sql
source_hash VARCHAR(128)
```

Update:

```text
src/sayane_tidb_demo/ingest.py
```

Store SHA-256 hash of the full source file content.

This supports T-RDE source-level evidence.

### Task 7: Add tests

Update or add tests under:

```text
tests/
```

Required tests:

1. `get_backend_capabilities()` returns native vector index as false.
2. `get_backend_capabilities()` reports SQL audit tables as true.
3. `chunk_markdown()` still passes existing tests.
4. `CHUNKING_STRATEGY` is not empty.
5. Source hash function returns stable SHA-256 for identical content.
6. Capability object can be serialized to dict or JSON.

Do not require TiDB or OpenAI in unit tests.

CI must continue to pass with:

```bash
pytest
```

### Task 8: Update documentation

Update the following docs:

```text
docs/article-implementation-notes.md
docs/local-runbook.md
docs/demo-output.md
docs/specs/ocsi-compliance-checklist.md
docs/specs/sayane-tidb-basic-spec.md
```

Required documentation updates:

- mention `sayane-tidb-demo capabilities`;
- mention backend capability snapshot in retrieval logs;
- update current demo status if appropriate;
- keep claim boundary: still not TiDB-native vector-indexed;
- keep claim boundary: still not OCSI-T-RDE-Ready unless all checklist items are actually satisfied.

## Constraints

### Do not fatten OCSI core

Do not add high-level operations such as:

```text
generate_answer
summarize_context
approve_candidate
merge_candidate
plan_task
notify_user
```

These are outside OCSI core.

### Do not make TiDB the conceptual center

The implementation may use TiDB, but documentation must keep the framing:

```text
TiDB is a backend adapter candidate.
OCSI is backend-agnostic.
Sayane remains independent of any single backend.
```

### Do not overclaim vector capability

The current implementation remains:

```text
JSON embedding storage + Python-side cosine similarity
```

Do not describe it as:

```text
TiDB-native vector-indexed search
```

unless Issue #1 is completed.

### Do not treat lightweight audit as full T-RDE

The current implementation stores lightweight audit summaries only.

Do not describe it as:

```text
full T-RDE scoring
```

## Suggested implementation order

1. Add `capabilities.py`.
2. Add tests for capabilities.
3. Add CLI `capabilities` command.
4. Update schema fields.
5. Update ingestion for source hash, chunking strategy, embedding metadata.
6. Update retrieval log recording for capability snapshot.
7. Update tests.
8. Update docs.
9. Run `pytest`.
10. Run a manual smoke test if TiDB credentials are available.

## Manual smoke test

If `.env` is configured:

```bash
make install
sayane-tidb-demo capabilities
make init
make ingest
make search-text
make ingest-embed
make search-vector
make search-hybrid
make logs
```

## Expected Delta-M

Preserved:

- OCSI remains backend-agnostic.
- Sayane-TiDB remains a demo/adapter, not Sayane core.
- Current vector implementation remains clearly non-native.

Transformed:

- Retrieval logs become stronger T-RDE evidence by storing backend capability snapshots.
- Chunks become stronger SearchUnit evidence by storing chunking strategy and embedding metadata.
- Documents become stronger SourceRecord evidence by storing source hash.

Added:

- BackendCapabilities model.
- CLI capability reporting.
- More OCSI-Basic evidence fields.

Unresolved:

- Formal EvidenceExport bundle.
- TiDB-native vector search.
- Full OCSI-T-RDE-Ready compliance.

Drift risk:

- Adding evidence fields may be mistaken for full T-RDE compliance.
- Documentation must keep the claim bounded.

## Acceptance criteria

- [ ] `sayane-tidb-demo capabilities` works without TiDB or OpenAI credentials.
- [ ] `pytest` passes.
- [ ] Retrieval logs include backend capability snapshot.
- [ ] Chunks include chunking strategy.
- [ ] Chunks include embedding model/provider when embedded.
- [ ] Documents include source hash.
- [ ] Docs still state that vector search is not TiDB-native vector-indexed.
- [ ] Docs still state that lightweight audit is not full T-RDE scoring.
- [ ] OCSI compliance checklist is updated to reflect actual status.
