# Contributing to BladeRecon

BladeRecon is in v0.2.1 public-testing hardening. Contributions should improve
release quality without expanding scope.

## Good Contributions

- Reliability fixes for failed or partial scans.
- Runtime reductions that preserve intelligence quality.
- Report improvements that help researchers decide what to test first.
- Packaging, installation, documentation, and Windows/WSL usability fixes.
- Tests for empty artifacts, blocked targets, and large-scope behavior.

## Avoid

- New scan modules or new external integrations.
- AI, LLM, or machine-learning features.
- Broad refactors that do not fix a release issue.
- Low-signal inventory expansion.

## Community Standards

Follow `CODE_OF_CONDUCT.md` in all project spaces. Use the GitHub issue
templates for bugs, feature requests, and report-quality feedback so maintainers
can reproduce problems without exposing sensitive third-party target data.

## Local Checks

```bash
python -m pytest
python -m compileall bladerecon
python -m build
bladerecon doctor
```

## Development Install

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
bladerecon --help
```

Use `source .venv/bin/activate` instead of the PowerShell activation command on
Linux, macOS, or WSL.
