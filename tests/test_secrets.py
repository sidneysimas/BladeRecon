from bladerecon.modules.secrets import _find_secrets


def test_find_secrets_detects_common_javascript_patterns() -> None:
    content = """
    const google = "AIzaSyD-abcdefghijklmnopqrstuvwxyz01234";
    const token = "Bearer abcdefghijklmnopqrstuvwxyz123456";
    """

    findings = _find_secrets(content)
    types = {item["type"] for item in findings}

    assert "Google API Key" in types
    assert "Bearer Token" in types
    by_type = {item["type"]: item for item in findings}
    assert by_type["Google API Key"]["confidence"] == "LOW"
    assert by_type["Bearer Token"]["confidence"] == "MEDIUM"
    assert by_type["Bearer Token"]["risk"] == "Medium"
    assert "value_preview" in by_type["Google API Key"]
