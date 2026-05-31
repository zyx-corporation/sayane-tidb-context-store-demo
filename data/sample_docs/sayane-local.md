# Sayane Local Edition

Sayane Local uses SQLite as the primary local context store and DuckDB as the local analytics store.

SQLite stores documents, chunks, sources, semantic events, RDE audit logs, retrieval logs, and context snapshots.

DuckDB analyzes accumulated logs, RDE evaluations, Delta-M trends, retrieval quality, and backend comparison results.

The local edition should remain portable and local-first.
