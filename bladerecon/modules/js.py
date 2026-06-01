"""JavaScript reconnaissance module.

Discovers external JavaScript assets from alive hosts and stores a lightweight
local copy for endpoint and secret analysis.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from .utils import (
    AsyncRateLimiter,
    async_retry,
    config_get,
    dedupe_preserve_order,
    get_profiled_ceiling,
    get_profiled_concurrency,
    get_profiled_per_host_concurrency,
    get_profiled_rate_limit,
    host_key,
    httpx_client_kwargs,
    info,
    limit_items_with_notice,
    load_config,
    log_duration,
    normalize_scan_profile,
    ProgressReporter,
    prepare_module_output,
    print_module_summary,
    setup_logging,
    success,
    target_output_dir,
    warn,
    write_json,
)


def _load_alive_hosts(target_dir: Path) -> List[str]:
    path = target_dir / "probe" / "alive.txt"
    if not path.exists():
        return []
    return dedupe_preserve_order(path.read_text(encoding="utf-8").splitlines())


def _load_probe_rows(target_dir: Path) -> List[Dict[str, object]]:
    path = target_dir / "probe" / "probe.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _host(url: str) -> str:
    parsed = urlparse(url)
    return (parsed.hostname or url).lower().rstrip(".")


def _prioritize_alive_hosts(alive_hosts: List[str], probe_rows: List[Dict[str, object]], domain: str, max_pages: int) -> List[str]:
    if max_pages <= 0 or len(alive_hosts) <= max_pages:
        return alive_hosts

    row_by_url: Dict[str, Dict[str, object]] = {}
    for row in probe_rows:
        if not isinstance(row, dict):
            continue
        for key in ("url", "final_url"):
            value = str(row.get(key) or "").strip()
            if value:
                row_by_url[value] = row
                row_by_url[value.rstrip("/")] = row
    primary_hosts = {domain.lower(), f"www.{domain.lower()}"}
    selected: List[str] = []
    seen_titles = set()
    seen_lengths = set()
    seen_tech = set()

    def remember(url: str) -> None:
        row = row_by_url.get(url, {})
        if isinstance(row, dict):
            title = str(row.get("title") or "").strip().lower()
            length = int(row.get("content_length") or 0)
            technologies = row.get("technologies", [])
            if title:
                seen_titles.add(title)
            if length:
                seen_lengths.add(length)
            if technologies:
                seen_tech.add(",".join(sorted(str(item) for item in technologies)))

    def score(url: str) -> int:
        row = row_by_url.get(url, {})
        host = _host(url)
        status = int(row.get("status_code") or 0) if isinstance(row, dict) else 0
        title = str(row.get("title") or "").strip().lower() if isinstance(row, dict) else ""
        length = int(row.get("content_length") or 0) if isinstance(row, dict) else 0
        technologies = row.get("technologies", []) if isinstance(row, dict) else []
        value = 0
        if host in primary_hosts or host.endswith(f".{domain.lower()}") and host.split(".", 1)[0] in {"www", "app", "admin", "api"}:
            value += 100
        if status == 200:
            value += 35
        elif status in {401, 403}:
            value += 15
        elif status == 404:
            value -= 90
        elif status in {301, 302, 303, 307, 308}:
            value -= 30
        if title and title not in seen_titles:
            value += 20
        if length and length not in seen_lengths:
            value += 15
        if technologies:
            tech_key = ",".join(sorted(str(item) for item in technologies))
            if tech_key not in seen_tech:
                value += 15
        if "404" in title or "not found" in title:
            value -= 20
        return value

    # Keep a small ordered seed from probe output. On large SaaS targets, useful
    # storefronts can be redirect-only and otherwise look less valuable than
    # generic 403/404 infrastructure in a pure score sort.
    seed_count = 0 if max_pages < 10 else min(len(alive_hosts), max(5, max_pages // 4))
    for url in alive_hosts[:seed_count]:
        row = row_by_url.get(url, {})
        selected.append(url)
        remember(url)
        if len(selected) >= max_pages:
            break
    for url in sorted((url for url in alive_hosts if url not in selected), key=score, reverse=True):
        selected.append(url)
        remember(url)
        if len(selected) >= max_pages:
            break
    return selected


def _extract_script_urls(html: str, base_url: str) -> List[str]:
    """Extract and normalize external script URLs from HTML."""
    urls: List[str] = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script", src=True)
    except Exception:
        return []
    for script in scripts:
        src = str(script.get("src") or "").strip()
        if not src or src.startswith(("data:", "javascript:")):
            continue
        absolute = urljoin(base_url, src)
        parsed = urlparse(absolute)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            urls.append(absolute.split("#", 1)[0])
    return dedupe_preserve_order(urls)


def _safe_js_name(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name or "script.js"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    if not name.endswith(".js"):
        name = f"{name}.js"
    return f"{digest}-{name}"


async def _fetch_text(client: httpx.AsyncClient, url: str, timeout: float) -> str:
    resp = await async_retry(client.get, url, timeout=timeout, follow_redirects=True, max_retries=1, delay=0.5, backoff=2.0)
    resp.raise_for_status()
    return resp.text


async def _collect_js(
    alive_hosts: List[str],
    out_dir: Path,
    config: dict,
    concurrency: int,
    timeout: float,
    proxy: Optional[str],
    user_agent: Optional[str],
    random_user_agent: bool,
    profile: Optional[str],
) -> List[Dict[str, object]]:
    active_profile = normalize_scan_profile(profile, config)
    html_ceiling = get_profiled_ceiling("js_html", 40, active_profile, config)
    alive_hosts, _html_skipped = limit_items_with_notice(alive_hosts, html_ceiling, "JavaScript HTML requests")
    js_download_ceiling = get_profiled_ceiling("js_downloads", 150, active_profile, config)
    per_host_limit = get_profiled_per_host_concurrency("js", 2, active_profile, config)
    limiter = AsyncRateLimiter(get_profiled_rate_limit("js", 6, active_profile, config))
    sem = asyncio.Semaphore(max(1, concurrency))
    host_sems: Dict[str, asyncio.Semaphore] = {}
    js_by_url: Dict[str, Dict[str, object]] = {}
    files_dir = out_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    html_reporter = ProgressReporter("JavaScript HTML", total=len(alive_hosts), interval=10)
    js_reporter: Optional[ProgressReporter] = None
    html_completed = 0
    js_completed = 0

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        verify=False,
        **httpx_client_kwargs(config, proxy, user_agent, random_user_agent),
    ) as client:
        async def handle_page(page_url: str) -> None:
            nonlocal html_completed
            try:
                async with sem:
                    host_sem = host_sems.setdefault(host_key(page_url), asyncio.Semaphore(per_host_limit))
                    async with host_sem:
                        await limiter.wait()
                        html = await _fetch_text(client, page_url, timeout)
            except Exception as exc:
                warn(f"Unable to fetch HTML: {page_url} ({exc})")
                html_completed += 1
                html_reporter.update(html_completed)
                return

            for js_url in _extract_script_urls(html, page_url):
                js_by_url.setdefault(js_url, {"url": js_url, "source_page": page_url})
            html_completed += 1
            html_reporter.update(html_completed)

        await asyncio.gather(*(handle_page(host) for host in alive_hosts), return_exceptions=True)
        html_reporter.update(html_completed, force=True)
        discovered_js_count = len(js_by_url)
        if js_download_ceiling > 0 and discovered_js_count > js_download_ceiling:
            warn(f"JavaScript downloads capped at {js_download_ceiling} of {discovered_js_count} asset(s) by active safety profile")
            js_by_url = dict(list(js_by_url.items())[:js_download_ceiling])
        js_reporter = ProgressReporter("JavaScript Downloads", total=len(js_by_url), interval=10)

        async def handle_js(item: Dict[str, object]) -> None:
            nonlocal js_completed
            url = str(item["url"])
            try:
                async with sem:
                    host_sem = host_sems.setdefault(host_key(url), asyncio.Semaphore(per_host_limit))
                    async with host_sem:
                        await limiter.wait()
                        resp = await async_retry(client.get, url, timeout=timeout, follow_redirects=True, max_retries=1, delay=0.5, backoff=2.0)
                        resp.raise_for_status()
                        content_type = resp.headers.get("content-type", "")
                        if "javascript" not in content_type.lower() and not urlparse(url).path.lower().endswith(".js"):
                            return
                        local_path = files_dir / _safe_js_name(url)
                        local_path.write_text(resp.text, encoding="utf-8", errors="ignore")
                        item.update(
                            {
                                "status_code": resp.status_code,
                                "content_length": len(resp.content),
                                "local_path": str(local_path.relative_to(out_dir.parent)),
                            }
                        )
            except Exception as exc:
                warn(f"Skipping broken JS link: {url} ({exc})")
            finally:
                js_completed += 1
                if js_reporter:
                    js_reporter.update(js_completed)

        await asyncio.gather(*(handle_js(item) for item in js_by_url.values()), return_exceptions=True)
        if js_reporter:
            js_reporter.update(js_completed, force=True)

    return [item for item in js_by_url.values() if item.get("local_path")]


def run(
    domain: str,
    output: Path = Path("results"),
    concurrency: Optional[int] = None,
    timeout: Optional[int] = None,
    proxy: Optional[str] = None,
    user_agent: Optional[str] = None,
    random_user_agent: bool = False,
    resume: bool = False,
    profile: Optional[str] = None,
) -> List[Dict[str, object]]:
    """Discover JavaScript files from alive hosts."""
    target_dir = target_output_dir(output, domain)
    out_dir = prepare_module_output(output, domain, "js", resume=resume)
    log = setup_logging(domain, output, "js")
    started = time.perf_counter()

    config = load_config()
    alive_hosts = _load_alive_hosts(target_dir)
    if not alive_hosts:
        warn("No alive hosts found. Run probe before js.")
        print_module_summary(
            "JavaScript Summary",
            {"Target": domain, "Duration": "0.00s", "Alive Hosts": 0, "Results Found": 0, "Output Location": out_dir},
        )
        return []

    active_profile = normalize_scan_profile(profile, config)
    resolved_concurrency = max(1, int(concurrency or get_profiled_concurrency("js", int(config_get(config, "concurrency.js", 10)), active_profile, config)))
    resolved_timeout = float(timeout or config_get(config, "timeouts.http", 10))
    max_html_pages = int(config_get(config, "js.max_html_pages", 40) or 40)
    original_alive_count = len(alive_hosts)
    probe_rows = _load_probe_rows(target_dir)
    alive_hosts = _prioritize_alive_hosts(alive_hosts, probe_rows, domain, max_html_pages)
    html_ceiling = get_profiled_ceiling("js_html", max_html_pages, active_profile, config)
    alive_hosts, _profile_html_skipped = limit_items_with_notice(alive_hosts, html_ceiling, "JavaScript HTML requests")

    info(f"JavaScript recon started for {domain} profile={active_profile}")
    if len(alive_hosts) < original_alive_count:
        info(f"JavaScript HTML targets prioritized: {len(alive_hosts)} of {original_alive_count}")
    log.info("Starting JS recon for %s with %d alive hosts (%d original)", domain, len(alive_hosts), original_alive_count)

    try:
        with log_duration(log, "js"):
            rows = asyncio.run(
                _collect_js(
                    alive_hosts,
                    out_dir,
                    config,
                    resolved_concurrency,
                    resolved_timeout,
                    proxy,
                    user_agent,
                    random_user_agent,
                    active_profile,
                )
            )
    except Exception as exc:
        log.exception("JavaScript recon failed")
        warn(f"JavaScript recon failed: {exc}")
        rows = []

    urls = dedupe_preserve_order(str(row["url"]) for row in rows)
    (out_dir / "js_files.txt").write_text("\n".join(urls), encoding="utf-8")
    write_json(out_dir / "js_files.json", rows)
    write_json(
        out_dir / "metadata.json",
        {
            "alive_hosts": original_alive_count,
            "html_requests": len(alive_hosts),
            "html_hosts_skipped": max(0, original_alive_count - len(alive_hosts)),
            "download_requests": len(rows),
            "results_found": len(urls),
            "concurrency": resolved_concurrency,
            "per_host_concurrency": get_profiled_per_host_concurrency("js", 2, active_profile, config),
            "rate_limit_per_second": get_profiled_rate_limit("js", 6, active_profile, config),
            "safety_profile": active_profile,
            "html_request_ceiling": get_profiled_ceiling("js_html", 40, active_profile, config),
            "download_request_ceiling": get_profiled_ceiling("js_downloads", 150, active_profile, config),
            "timeout": resolved_timeout,
        },
    )

    success(f"JavaScript files found: {len(urls)}")
    print_module_summary(
        "JavaScript Summary",
        {
            "Target": domain,
            "Duration": f"{time.perf_counter() - started:.2f}s",
            "Alive Hosts": original_alive_count,
            "HTML Requests": len(alive_hosts),
            "Hosts Skipped": max(0, original_alive_count - len(alive_hosts)),
            "Results Found": len(urls),
            "Output Location": out_dir,
        },
    )
    return rows
