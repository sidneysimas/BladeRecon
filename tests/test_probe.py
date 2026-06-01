import json
from pathlib import Path

from bladerecon.modules import probe


def test_probe_targets_include_http_and_https_for_host():
    urls = probe._normalize_probe_targets(["testphp.vulnweb.com"])

    assert urls == ["https://testphp.vulnweb.com", "http://testphp.vulnweb.com"]


def test_probe_treats_redirect_and_auth_statuses_as_alive():
    assert 301 in probe.ALIVE_STATUS_CODES
    assert 302 in probe.ALIVE_STATUS_CODES
    assert 307 in probe.ALIVE_STATUS_CODES
    assert 308 in probe.ALIVE_STATUS_CODES
    assert 401 in probe.ALIVE_STATUS_CODES
    assert 403 in probe.ALIVE_STATUS_CODES


def test_technology_outputs_merge_duplicate_hosts(tmp_path: Path):
    target_dir = tmp_path / "example.com"
    probe._write_technology_outputs(
        target_dir,
        [
            {
                "url": "https://WWW.example.com",
                "final_url": "https://www.example.com/",
                "server": "nginx/1.25.0",
                "cdn": "Cloudflare",
                "waf": "",
                "technologies": ["React"],
                "technology_details": [
                    {"name": "React", "confidence": "High", "sources": ["HTML Fingerprint"], "evidence": ["data-reactroot"]}
                ],
            },
            {
                "url": "http://www.example.com",
                "final_url": "http://www.example.com",
                "server": "",
                "cdn": "Fastly",
                "waf": "",
                "technologies": ["Drupal"],
                "technology_details": [
                    {"name": "Drupal", "confidence": "Medium", "sources": ["HTML Fingerprint"], "evidence": ["drupal"]}
                ],
            },
        ],
    )

    rows = json.loads((target_dir / "technologies" / "technologies.json").read_text(encoding="utf-8"))

    assert len(rows) == 1
    assert rows[0]["host"] == "www.example.com"
    assert set(rows[0]["detected"]) >= {"Cloudflare", "Fastly", "React", "Drupal", "nginx"}
    react = next(item for item in rows[0]["technologies"] if item["name"] == "React")
    assert react["confidence"] == "High"
    assert "HTML Fingerprint" in react["sources"]
