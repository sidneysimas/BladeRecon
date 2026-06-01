"""Endpoint discovery from JavaScript assets."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin, urlparse

from .utils import dedupe_preserve_order, info, log_duration, prepare_module_output, print_module_summary, setup_logging, success, target_output_dir, warn, write_json

ENDPOINT_HINTS = (
    "/api/",
    "/api",
    "/v1/",
    "/v2/",
    "/v3/",
    "/graphql",
    "graphql",
    "/rest",
    "/auth",
    "/login",
    "/logout",
    "/register",
    "/users",
    "/admin",
    "/api-docs",
    "/swagger",
    "swagger.json",
    "swagger-ui",
    "/openapi",
    "openapi.json",
    "ws://",
    "wss://",
    "socket.io",
)

ABSOLUTE_URL_RE = re.compile(r"(?:https?|wss?)://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")
RELATIVE_RE = re.compile(r"(?P<quote>['\"`])(?P<path>/(?:api|v[0-9]+|graphql|rest|auth|login|logout|register|users|admin|api-docs|swagger|swagger-ui|openapi|socket\.io)[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%{}-]*)\1", re.IGNORECASE)
DOC_FILE_RE = re.compile(r"(?P<quote>['\"`])(?P<path>/?[A-Za-z0-9._~:/-]*(?:swagger|openapi)(?:-[A-Za-z0-9._~-]+)?\.json)\1", re.IGNORECASE)
CALL_RE = re.compile(
    r"(?:fetch|axios\.(?:get|post|put|delete|patch|request)|[A-Za-z0-9_$]+\.open|new\s+WebSocket|io)\s*\(\s*(?P<arg>[^,\)\n]+)",
    re.IGNORECASE,
)
TEMPLATE_PATH_RE = re.compile(r"(?P<path>/(?:api|v[0-9]+|graphql|rest|auth|login|logout|register|users|admin|api-docs|swagger|swagger-ui|openapi|socket\.io)[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%{}-]*)", re.IGNORECASE)


def _load_js_rows(target_dir: Path) -> List[dict]:
    path = target_dir / "js" / "js_files.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _read_js_content(target_dir: Path, row: dict) -> str:
    local_path = str(row.get("local_path") or "")
    if not local_path:
        return ""
    path = target_dir / local_path
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _normalize_endpoint(raw: str, source_url: str) -> str:
    value = raw.strip().strip("'\"")
    value = value.strip("`")
    value = re.sub(r"\$\{[^}]+\}", "", value)
    value = value.replace("}", "").replace("{", "")
    if not value:
        return ""
    if value.startswith(("http://", "https://", "ws://", "wss://")):
        return value.split("#", 1)[0]
    if value.startswith("/"):
        parsed = urlparse(source_url)
        if parsed.scheme and parsed.netloc:
            return urljoin(f"{parsed.scheme}://{parsed.netloc}", value).split("#", 1)[0]
        return value.split("#", 1)[0]
    return ""


def _category(endpoint: str) -> str:
    value = endpoint.lower()
    if "graphql" in value:
        return "GraphQL"
    if any(marker in value for marker in ("swagger", "openapi", "api-docs")):
        return "Swagger/OpenAPI"
    if value.startswith(("ws://", "wss://")) or "socket.io" in value:
        return "WebSocket"
    return "REST"


def _candidate_from_call_arg(arg: str) -> List[str]:
    value = arg.strip()
    candidates: List[str] = []
    quoted = re.match(r"^[rubfRUBF]*(['\"`])(?P<value>.*)\1$", value)
    if quoted:
        candidates.append(quoted.group("value"))
    elif value.startswith("`"):
        candidates.extend(match.group("path") for match in TEMPLATE_PATH_RE.finditer(value))
    elif value.startswith("{"):
        candidates.extend(match.group("path") for match in RELATIVE_RE.finditer(value))
    return candidates


def _extract_endpoint_items(content: str, source_url: str) -> List[Dict[str, str]]:
    candidates: List[str] = []
    for match in ABSOLUTE_URL_RE.findall(content):
        if any(hint in match.lower() for hint in ENDPOINT_HINTS):
            candidates.append(_normalize_endpoint(match, source_url))
    for match in RELATIVE_RE.finditer(content):
        candidates.append(_normalize_endpoint(match.group("path"), source_url))
    for match in DOC_FILE_RE.finditer(content):
        candidates.append(_normalize_endpoint(match.group("path"), source_url))
    for match in CALL_RE.finditer(content):
        for candidate in _candidate_from_call_arg(match.group("arg")):
            candidates.append(_normalize_endpoint(candidate, source_url))

    endpoints = dedupe_preserve_order(candidate for candidate in candidates if candidate)
    return [{"endpoint": endpoint, "category": _category(endpoint)} for endpoint in endpoints]


def _extract_endpoints(content: str, source_url: str) -> List[str]:
    return [item["endpoint"] for item in _extract_endpoint_items(content, source_url)]


def _source_name(row: dict, source_url: str) -> str:
    local_path = str(row.get("local_path") or "")
    if local_path:
        return Path(local_path).name
    parsed = urlparse(source_url)
    return Path(parsed.path).name or source_url


def run(domain: str, output: Path = Path("results"), resume: bool = False) -> List[Dict[str, str]]:
    """Extract endpoint candidates from downloaded JavaScript files."""
    target_dir = target_output_dir(output, domain)
    out_dir = prepare_module_output(output, domain, "endpoints", resume=resume)
    log = setup_logging(domain, output, "endpoints")
    started = time.perf_counter()

    info(f"Endpoint discovery started for {domain}")
    rows = _load_js_rows(target_dir)
    if not rows:
        warn("No JavaScript inventory found. Run js before endpoints.")

    endpoint_rows: List[Dict[str, str]] = []
    seen = set()
    with log_duration(log, "endpoints"):
        for row in rows:
            source_url = str(row.get("url") or "")
            content = _read_js_content(target_dir, row)
            if not content:
                continue
            source_js_file = _source_name(row, source_url)
            for item in _extract_endpoint_items(content, source_url):
                endpoint = item["endpoint"]
                key = endpoint.lower()
                if key in seen:
                    continue
                seen.add(key)
                endpoint_rows.append({"endpoint": endpoint, "source": source_url, "source_js_file": source_js_file, "category": item["category"]})

    endpoints = [row["endpoint"] for row in endpoint_rows]
    (out_dir / "endpoints.txt").write_text("\n".join(endpoints), encoding="utf-8")
    write_json(out_dir / "endpoints.json", endpoint_rows)

    success(f"Endpoints found: {len(endpoints)}")
    print_module_summary(
        "Endpoint Summary",
        {
            "Target": domain,
            "Duration": f"{time.perf_counter() - started:.2f}s",
            "JavaScript Files": len(rows),
            "Results Found": len(endpoints),
            "Output Location": out_dir,
        },
    )
    log.info("Endpoint discovery found %d endpoints", len(endpoints))
    return endpoint_rows
