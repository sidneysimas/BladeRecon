# BladeRecon Installation Guide

This guide prepares BladeRecon v0.2.1 for public-testing use.

## Recommended Install

Use `pipx` for the cleanest end-user installation. It keeps BladeRecon isolated
from your system Python while registering the `bladerecon` command globally.

```bash
pipx install bladerecon
bladerecon doctor
```

If `pipx` is not installed:

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

Restart the terminal if your shell cannot find `pipx` or `bladerecon`.

## Alternative Install

Use a virtual environment when `pipx` is not available:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install bladerecon
bladerecon doctor
```

Linux, macOS, and WSL:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install bladerecon
bladerecon doctor
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## First Scan

Run a conservative first scan:

```bash
bladerecon doctor
bladerecon full example.com --profile safe
bladerecon report example.com
```

`bladerecon scan example.com --profile safe` is accepted as an alias for
`bladerecon full example.com --profile safe`.

Reports are written to:

```text
results/example.com/runs/<latest-run-id>/reports/report.html
results/example.com/runs/<latest-run-id>/reports/report.md
```

BladeRecon also writes `results/example.com/latest_run.json`, which points
`bladerecon report example.com` and `bladerecon resume example.com` at the
latest valid isolated run. If no isolated full-run exists, report generation
falls back to the legacy `results/example.com/` module-output layout.

## Optional External Tools

BladeRecon works without optional tools, but some modules will be skipped.
`bladerecon doctor` explains what is available.

Install helper:

```bash
bladerecon install-deps
```

Screenshot support requires Playwright Chromium:

```bash
python -m playwright install chromium
```

Nuclei support requires the Nuclei binary and templates. On Windows,
`bladerecon install-deps` installs the prebuilt Nuclei v3 binary. On Linux,
macOS, and WSL, it uses the Go install workflow when Go is available.

Manual Nuclei install:

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -version
bladerecon doctor
```

If Nuclei is not installed, BladeRecon skips Nuclei scans gracefully.

## Source Install For Development

```bash
git clone https://github.com/mohamedxk9tb/BladeRecon.git
cd BladeRecon
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
bladerecon doctor
```

Linux, macOS, and WSL:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
bladerecon doctor
```

## Docker

Build:

```bash
docker build -t bladerecon .
```

Run doctor:

```bash
docker run --rm bladerecon doctor
```

Persist results:

```bash
docker run --rm -v "%cd%\results:/app/results" bladerecon full example.com --profile safe
```

PowerShell can also use:

```powershell
docker run --rm -v "${PWD}\results:/app/results" bladerecon full example.com --profile safe
```

## Verification

```bash
bladerecon --help
bladerecon --version
bladerecon doctor
bladerecon cache info
```

Expected release artifacts for maintainers:

```text
dist/bladerecon-0.2.1-py3-none-any.whl
dist/bladerecon-0.2.1.tar.gz
```

Maintainer validation:

```bash
python -m pytest
python -m compileall bladerecon
python -m build
```
