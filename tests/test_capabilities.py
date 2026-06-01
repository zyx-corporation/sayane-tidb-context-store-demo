import json

from sayane_tidb_demo.capabilities import get_backend_capabilities
from sayane_tidb_demo.chunker import CHUNKING_STRATEGY
from sayane_tidb_demo.ingest import source_hash_for_content


def test_get_backend_capabilities_reports_native_vector_index_as_false() -> None:
    capabilities = get_backend_capabilities()
    assert capabilities.supports_native_vector_index is False


def test_get_backend_capabilities_reports_sql_audit_tables_as_true() -> None:
    capabilities = get_backend_capabilities()
    assert capabilities.supports_audit_log_tables is True


def test_chunking_strategy_is_not_empty() -> None:
    assert CHUNKING_STRATEGY


def test_source_hash_returns_stable_sha256_for_identical_content() -> None:
    content = "Sayane Context Store Interface demo content."
    assert source_hash_for_content(content) == source_hash_for_content(content)
    assert len(source_hash_for_content(content)) == 64


def test_capability_object_can_be_serialized_to_dict() -> None:
    payload = get_backend_capabilities().to_dict()
    assert payload["backend_id"] == "sayane-tidb-json-vector-demo"
    assert payload["supports_vector_search"] is True


def test_capability_object_can_be_serialized_to_json() -> None:
    payload = json.dumps(get_backend_capabilities().to_dict())
    parsed = json.loads(payload)
    assert parsed["supports_hybrid_search"] is True
