---
name: Bug Report
about: Report a bug, regression, or unexpected behavior in BladeRecon
title: "[Bug]: "
labels:
  - bug
assignees: ""
---

# Bug Summary

Provide a short description of the problem.

---

# BladeRecon Information

- BladeRecon version:
- Install method:
  - [ ] pip
  - [ ] pipx
  - [ ] Source
- Python version:
- Operating System:
- Architecture (x64 / ARM64):
- Shell (PowerShell, Bash, Zsh, etc.):

---

# Scan Information

- Target:
- Scan type:
  - [ ] Full
  - [ ] Resume
  - [ ] Report
  - [ ] Single Module

- Profile:
  - [ ] Safe
  - [ ] Balanced
  - [ ] Aggressive

---

# Optional Components

- Nuclei installed:
- Nuclei version:
- Playwright Chromium installed:
- Playwright version:

---

# Command Executed

```bash

```

---

# Steps To Reproduce

1.
2.
3.

---

# Expected Behavior

Describe what should have happened.

---

# Actual Behavior

Describe what actually happened.

---

# Does this affect scan accuracy?

- [ ] Yes
- [ ] No
- [ ] Not sure

---

# Severity

- [ ] Critical
- [ ] High
- [ ] Medium
- [ ] Low

---

# Regression

- [ ] This worked in a previous BladeRecon version.

Previous version (if known):

---

# Bug Category

- [ ] CLI
- [ ] Runtime
- [ ] Detection
- [ ] Intelligence
- [ ] Report
- [ ] Resume
- [ ] Nuclei
- [ ] Screenshots
- [ ] Packaging
- [ ] Documentation
- [ ] Other

---

# Run Information

If available, include:

- Output path:
- Run ID:
- Module that failed:
- Module that timed out:
- Module that was skipped:

---

# Logs

Paste relevant terminal output.

```text

```

---

# Recommended Attachments

If possible, attach sanitized copies of:

- latest_run.json
- scan_state.json
- scan_meta.json
- report.md
- report.html (optional)
- module metadata.json
- screenshots (if relevant)

---

# Validation Performed

If applicable:

- [ ] python -m pytest
- [ ] python -m compileall bladerecon
- [ ] python -m build

---

# Data Safety Checklist

Before submitting:

- [ ] I removed secrets, API keys, tokens, cookies, and credentials.
- [ ] I removed customer or third-party confidential data.
- [ ] I only included data from targets I am authorized to scan.
- [ ] Attached logs and reports have been sanitized.

---

# Additional Context

Add anything else that may help reproduce or understand the issue.

Examples:

- Screenshots
- Network conditions
- Proxy/VPN
- Special configuration
- Related issue numbers