import pytest

from sayane_tidb_demo.config import DatabaseConfigError, Settings, validate_tidb_settings


def test_validate_tidb_settings_raises_when_host_missing() -> None:
    settings = Settings(tidb_host="", tidb_user="user", tidb_password="secret")
    with pytest.raises(DatabaseConfigError) as exc_info:
        validate_tidb_settings(settings)

    message = str(exc_info.value)
    assert "TIDB_HOST" in message
    assert ".env.example" in message


def test_validate_tidb_settings_lists_all_missing_fields() -> None:
    settings = Settings()
    with pytest.raises(DatabaseConfigError) as exc_info:
        validate_tidb_settings(settings)

    message = str(exc_info.value)
    assert "TIDB_HOST" in message
    assert "TIDB_USER" in message
    assert "TIDB_PASSWORD" in message
