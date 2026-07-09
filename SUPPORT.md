# Support

BladeRecon is a volunteer-maintained open-source security tool. Please keep
support requests reproducible, scoped, and free of sensitive target data.

## Before Opening An Issue

Run:

```bash
bladerecon --version
bladerecon doctor
```

If you are working from a source checkout, also run `python -m pytest`.

For scan-specific problems, also check:

```text
results/<target>/latest_run.json
results/<target>/runs/<run-id>/scan_state.json
results/<target>/runs/<run-id>/logs/errors.log
results/<target>/runs/<run-id>/logs/scan_meta.json
```

## Where To Ask

- Bugs and regressions: use the Bug Report template.
- Report quality or prioritization issues: use the Report Quality Feedback
  template.
- Scoped improvements: use the Feature Request template.
- Sensitive vulnerabilities in BladeRecon itself: follow `SECURITY.md`.

## Data Safety

Do not post live credentials, private bug bounty data, customer hostnames,
tokens, screenshots with sensitive content, or full reports from unauthorized
targets. Prefer `example.com` reproductions or sanitized snippets.
