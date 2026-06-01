from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BackendCapabilities:
    backend_id: str
    supports_lexical_search: bool
    supports_vector_search: bool
    supports_hybrid_search: bool
    supports_native_vector_index: bool
    supports_full_text_index: bool
    supports_sql_queries: bool
    supports_transactional_ingest: bool
    supports_audit_log_tables: bool
    supports_portable_export: bool
    supports_multi_user_access: bool
    supports_cloud_managed_operations: bool
    supports_local_first_storage: bool
    supports_event_lineage: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def get_backend_capabilities() -> BackendCapabilities:
    return BackendCapabilities(
        backend_id="sayane-tidb-json-vector-demo",
        supports_lexical_search=True,
        supports_vector_search=True,
        supports_hybrid_search=True,
        supports_native_vector_index=False,
        supports_full_text_index=False,
        supports_sql_queries=True,
        supports_transactional_ingest=True,
        supports_audit_log_tables=True,
        supports_portable_export=False,
        supports_multi_user_access=False,
        supports_cloud_managed_operations=True,
        supports_local_first_storage=False,
        supports_event_lineage=True,
    )
