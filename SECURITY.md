# Security Policy

BladeRecon is a reconnaissance framework. Please report vulnerabilities in the
framework itself, its packaging, or its generated reports responsibly.

## Supported Versions

Security fixes are prioritized for the latest published release candidate and
the `main` branch.

## Reporting A Vulnerability

Please use GitHub Issues for non-sensitive security bugs. For sensitive reports,
contact the maintainer listed in `pyproject.toml` and include:

- Affected BladeRecon version or commit.
- Operating system and Python version.
- Minimal reproduction steps.
- Impact assessment.
- Any relevant logs or generated artifacts.

Do not include third-party target data, live credentials, or bug bounty program
findings in public issues.

## Scope

In scope:

- Unsafe filesystem handling.
- Command execution or dependency installation issues.
- Report rendering vulnerabilities.
- Incorrect scan scoping or safety-control bypasses.
- Packaging or Docker security issues.

Out of scope:

- Vulnerabilities discovered in third-party targets using BladeRecon.
- Findings produced by Nuclei templates or external tools.
- Network rate limits, WAF blocks, or target-side enforcement behavior.
