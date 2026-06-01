from pathlib import Path
from unittest.mock import patch

from bladerecon.modules import screenshots


def test_screenshot_preserves_chromium_validation_detail(tmp_path: Path) -> None:
    with patch(
        "bladerecon.modules.screenshots.check_playwright_chromium",
        return_value=(False, "Browser launch failed: Access denied"),
    ):
        result = screenshots.run(domain="example.com", output=tmp_path, concurrency=1)

    assert result.status == "skipped"
    assert result.reason == "Browser launch failed: Access denied"


def test_screenshot_failure_classifier_categorizes_common_errors() -> None:
    assert screenshots._classify_navigation_error(Exception("net::ERR_CERT_AUTHORITY_INVALID"), "domcontentloaded") == "SSL error"
    assert screenshots._classify_navigation_error(Exception("net::ERR_NAME_NOT_RESOLVED"), "domcontentloaded") == "DNS failure"
    assert screenshots._classify_navigation_error(Exception("net::ERR_TOO_MANY_REDIRECTS"), "domcontentloaded") == "Redirect loop"
