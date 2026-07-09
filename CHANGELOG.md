# Changelog

## Unreleased

- Added release-readiness community files for support and pull requests.
- Clarified responsible-use guidance, Python version support, and report command
  behavior in user-facing documentation.
- Improved issue templates so maintainers receive sanitized reproduction data,
  environment details, and validation context.

## 0.2.1 - 2026-06-05

- Added a discoverable `bladerecon scan` alias for the standard full workflow and surfaced a Start Here path in root help for first-time users.
- Modernized installation documentation for PyPI/pipx users, corrected stale v0.2.0 artifact references, and added contribution guidance for public testing.
- Tightened Nuclei tag-fallback behavior so failed intelligence tags cannot fall through into an unjustified baseline-only scan without passing the ROI gate.
- Refined opportunity scoring so weakly validated or historical-only leads cannot inflate the Research Opportunity Score into a perfect/high-confidence signal.
- Prevented campaign clustering from inferring Authentication Surface campaigns from generic authorization-testing guidance.
- Capped campaign confidence when validation is weak or absent so campaigns read like investigation plans instead of inflated clusters.
- Kept concrete GraphQL plus administrative attack paths eligible for Critical Investigation when current endpoint evidence supports them.
- Hardened report architecture for release readiness: one canonical start-here queue, campaign cards as testing plans, secondary leads renamed to additional opportunities, priority assets demoted to supporting inventory, and technology evidence split into attack-surface versus infrastructure context.
- Reduced report duplication by keeping the primary recommendation in Where Should I Start and moving additional target detail lower in the report.
- Updated package metadata to v0.2.1 and modernized the MIT license declaration for clean builds with current setuptools.

## 0.2.0 - 2026-05-29

- Added Advanced Recon intelligence with historical URL collection, historical endpoint/parameter extraction, historical attack-surface correlation, historical JavaScript analysis, low-noise content discovery, security-header asset discovery, and asset prioritization.
- Refined Smart Nuclei to pair technology-tag selection with a lightweight `critical,high` baseline safety net when ROI is justified, skip baseline-only scans without opportunity evidence, scope justified baseline-only runs to validated opportunity hosts, and report the coverage strategy in metadata and reports.
- Hardened Smart Nuclei baseline ROI further so post-tag baselines only run for uncovered high-confidence or validated opportunity hosts, with explicit baseline reason, skip reason, ROI, and target metadata.
- Hardened historical JavaScript reuse so blocked live pages can still feed endpoint and secret extraction when historical JS artifacts exist.
- Added endpoint signal controls that suppress third-party API noise while preserving in-scope endpoints recovered from live and historical JavaScript.
- Added screenshot timing telemetry and Advanced Recon source-level ROI metrics to expose slow captures and low-yield historical sources.
- Added report dashboard guidance with a Where Should I Start section and separated Research Opportunity Score from Program Risk Score.
- Tightened the report dashboard further with a primary start-here lead, compact secondary targets, collapsed supporting evidence, and clearer Research Opportunity vs Program Risk language.
- Reworked the Executive Summary into a decision dashboard that emphasizes opportunity level, attack surface, Nuclei outcome, and scan outcome before raw inventory.
- Fixed report logo embedding for the shipped branding asset while retaining an oversized-asset safety cap.
- Extended historical JavaScript reuse so Advanced Recon records secret-pattern evidence and the Secrets module merges those historical artifacts when live JavaScript is blocked.
- Kept public package metadata in Beta status for honest release-candidate/public-testing positioning.
- Improved asset-priority explainability with per-signal scoring details, strongest factors, confidence labels, historical/live distinctions, and clearer report presentation.
- Fixed release-candidate validation issues around custom Nuclei template directories, UTF-8 BOM target lists/artifacts, Nuclei Not Run summary labels, and estimated request metrics.
- Added `advanced` CLI command and integrated it into the full workflow before screenshots and Nuclei.
- Added report sections for Advanced Recon Intelligence, Top Priority Assets, Historical Attack Surface, Interesting Paths, Security Header Assets, and quality-control ratios.
- Added professional Rich CLI branding, status language, summaries, cache commands, resume flow, and version reporting.
- Added passive source integrations for Chaos, BufferOver, URLScan, and optional RapidDNS, Anubis, HackerTarget.
- Added source-tagged subdomain JSON/JSONL outputs and lightweight passive-source cache.
- Added probe fingerprints for server, CDN, WAF, and framework hints.
- Added screenshot target filtering for duplicate titles/content lengths, placeholders, and existing captures.
- Replaced nuclei severity-only behavior and the old full profile label with explicit safe, balanced, and aggressive safety profiles.
- Added request ceilings, per-host concurrency limits, request-rate pacing, and active-profile metadata for probe, JavaScript, screenshots, Nuclei, full scans, and reports.
- Changed Nuclei module timeout handling to monitor-only by default, with configurable wall-clock timeout enforcement and clear Timed Out reporting.
- Added recon intelligence outputs for technology, infrastructure, cloud references, risk scoring, and smart template selection.
- Added JSON/JSONL automation outputs for probe, subdomains, parameters, and nuclei.
- Made the dark report theme the default and improved metrics, screenshot gallery, severity display, search, attack-surface summary, report-logo rendering, active-profile display, and collapsible Performance Analytics.
- Added low-overhead scan and per-module performance metrics for full workflow reports.
- Added release media assets for README showcase, including CLI preview, report preview, and social preview images.
- Hardened target path normalization, fresh module state handling, intelligence preflight validation, and Windows-safe banner rendering.
- Added Docker support, pytest coverage, release metadata alignment, and cleanup rules.

## 0.1.0

- Initial BladeRecon package with subdomain discovery, probing, parameters, screenshots, nuclei wrapper, and reports.
