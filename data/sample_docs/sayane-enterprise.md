# Sayane Enterprise Edition

Sayane Enterprise provides two backend families.

PostgreSQL is the standard enterprise backend. It is suitable for conservative enterprise deployment, cloud or on-premise operation, existing SQL operations, pgvector, and full-text search.

TiDB is the scale-out and cloud-oriented backend. It is suitable for distributed SQL, managed cloud RAG, AI memory workloads, and large-scale context retrieval.

The core abstraction remains the Sayane Context Store Interface. TiDB is an adapter, not the theoretical center of Sayane.
