## Summary

<!-- What release-quality problem does this PR solve? -->

## Scope

- [ ] No new recon modules
- [ ] No AI, plugin, or roadmap feature work
- [ ] User-facing behavior is documented if changed
- [ ] Sensitive target data and generated scan artifacts are excluded

## Validation

```bash
python -m pytest
python -m compileall bladerecon
python -m build
```

## Notes For Reviewers

<!-- Mention runtime impact, report wording changes, packaging impact, or known risks. -->
