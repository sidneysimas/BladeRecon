from pathlib import Path

from bladerecon.modules.endpoints import _extract_endpoint_items, _extract_endpoints, run


def test_extract_endpoints_normalizes_relative_routes_and_deduplicates() -> None:
    content = """
    fetch('/api/users')
    const graph = "/graphql";
    const absolute = "https://api.example.com/v1/login";
    fetch('/api/users')
    """

    assert set(_extract_endpoints(content, "https://www.example.com/static/app.js")) == {
        "https://www.example.com/api/users",
        "https://api.example.com/v1/login",
        "https://www.example.com/graphql",
    }


def test_extract_endpoints_detects_modern_javascript_patterns() -> None:
    content = """
    fetch(`${base}/api/v2/accounts`)
    axios.post('/auth/login')
    xhr.open('GET', '/swagger.json')
    const client = new WebSocket('wss://stream.example.com/socket.io/?token=x')
    const apollo = { uri: '/graphql/' }
    const docs = "/api-docs";
    """

    items = _extract_endpoint_items(content, "https://www.example.com/assets/main.js")
    endpoints = {item["endpoint"]: item["category"] for item in items}

    assert "https://www.example.com/api/v2/accounts" in endpoints
    assert endpoints["https://www.example.com/auth/login"] == "REST"
    assert endpoints["https://www.example.com/swagger.json"] == "Swagger/OpenAPI"
    assert endpoints["wss://stream.example.com/socket.io/?token=x"] == "WebSocket"
    assert endpoints["https://www.example.com/graphql/"] == "GraphQL"
    assert endpoints["https://www.example.com/api-docs"] == "Swagger/OpenAPI"


def test_endpoint_run_keeps_source_file_attribution(tmp_path: Path) -> None:
    target = tmp_path / "example.com"
    js_dir = target / "js" / "files"
    js_dir.mkdir(parents=True)
    (js_dir / "app.js").write_text("fetch('/api/users')", encoding="utf-8")
    (target / "js" / "js_files.json").write_text(
        '[{"url":"https://www.example.com/app.js","source_page":"https://www.example.com","local_path":"js/files/app.js"}]',
        encoding="utf-8",
    )

    rows = run("example.com", output=tmp_path)

    assert rows == [
        {
            "endpoint": "https://www.example.com/api/users",
            "source": "https://www.example.com/app.js",
            "source_js_file": "app.js",
            "category": "REST",
        }
    ]
