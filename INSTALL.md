# BladeRecon Installation Guide

This guide prepares a local BladeRecon v0.2.0 RC environment.

## Requirements

- Python 3.8 or newer
- pip
- Git
- Optional: Go for Nuclei
- Optional: Playwright Chromium for screenshots
- Optional: Docker Desktop for container usage

## Windows Installation

Open PowerShell in the project directory:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .
bladerecon doctor
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Python Requirements

BladeRecon is packaged through `pyproject.toml`.

Install from source:

```bash
python -m pip install .
```

Install editable for development:

```bash
python -m pip install -e .
```

Install test/build tools if needed:

```bash
python -m pip install pytest build wheel
```

## Go Installation

Nuclei is distributed as a Go binary.

Windows:

1. Install Go from https://go.dev/dl/
2. Restart the terminal.
3. Verify:

```powershell
go version
```

Linux:

```bash
sudo apt update
sudo apt install -y golang-go
go version
```

## Nuclei Installation

Install Nuclei:

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

Ensure Go bin is in PATH.

Windows usually uses:

```text
%USERPROFILE%\go\bin
```

Verify:

```bash
nuclei -version
bladerecon doctor
```

The first install can take several minutes while Go downloads and compiles dependencies. `bladerecon install-deps` shows progress messages while this is happening.

If Nuclei is not installed, BladeRecon skips Nuclei scans gracefully.

## Playwright And Chromium Installation

BladeRecon uses Playwright only for screenshots.

Install Chromium:

```bash
python -m playwright install chromium
```

Verify:

```bash
bladerecon doctor
```

If Chromium is missing, screenshots are skipped and the full workflow continues.

## Verification Steps

```bash
bladerecon --help
bladerecon --version
bladerecon doctor
bladerecon cache info
```

Run a small scan:

```bash
bladerecon subdomain example.com
bladerecon probe example.com --profile safe
bladerecon intelligence example.com
bladerecon advanced example.com --profile safe
bladerecon report example.com
```

Generated reports include offline HTML/Markdown output plus scan performance
analytics when produced by `bladerecon full`. The HTML report uses the dark
theme by default and shows the active safety profile.

## Safety Profile Defaults

BladeRecon defaults to `balanced`. Use `--profile safe` for bug bounty programs
or rate-sensitive targets. `--profile aggressive` is explicit opt-in for faster
scans and higher request ceilings.

```bash
bladerecon full example.com --profile safe
bladerecon nuclei example.com --profile safe --timeout 900
```

## Docker Installation

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
docker run --rm -v "%cd%\results:/app/results" bladerecon full example.com
```

PowerShell can also use:

```powershell
docker run --rm -v "${PWD}\results:/app/results" bladerecon full example.com
```

## Release Validation

For maintainers:

```bash
python -m pytest
python -m compileall bladerecon tests
python -m build
bladerecon doctor
```

Expected artifacts:

```text
dist/bladerecon-0.2.0-py3-none-any.whl
dist/bladerecon-0.2.0.tar.gz
```
