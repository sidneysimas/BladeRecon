## Summary

Briefly describe the purpose of this pull request.

What problem does it solve?

---

## Type of Change

- [ ] Bug fix
- [ ] Reliability improvement
- [ ] Runtime optimization
- [ ] Detection improvement
- [ ] Report improvement
- [ ] Documentation
- [ ] Packaging
- [ ] Tests
- [ ] CI/CD
- [ ] Refactoring
- [ ] Other

---

## Scope

Please confirm:

- [ ] No new recon modules
- [ ] No AI, plugins, or roadmap features
- [ ] No unnecessary dependencies
- [ ] User-facing behavior is documented if changed
- [ ] Sensitive target data and generated scan artifacts are excluded
- [ ] Existing behavior remains backward compatible (or breaking changes are documented)

---

## Validation

Run before requesting review:

```bash
python -m pytest
python -m compileall bladerecon
python -m build
```

Validation completed:

- [ ] Tests passed
- [ ] Compile check passed
- [ ] Package build passed

---

## Runtime Impact

How does this change affect runtime?

- [ ] Faster
- [ ] No measurable change
- [ ] Slightly slower (justified)
- [ ] Unknown

If applicable, explain:

---

## Report Impact

Does this change affect generated reports?

- [ ] No
- [ ] HTML
- [ ] Markdown
- [ ] Report wording
- [ ] Report prioritization
- [ ] Risk score
- [ ] Opportunity scoring

If yes, describe:

---

## Breaking Changes

- [ ] None

If yes, explain:

---

## Reviewer Notes

Anything reviewers should pay attention to?

Examples:

- Runtime implications
- Detection changes
- Metadata changes
- Packaging changes
- Report wording
- Known limitations
- Edge cases

---

## Checklist

Before requesting review:

- [ ] Code follows the existing project style
- [ ] Tests were added or updated where appropriate
- [ ] Documentation was updated (if needed)
- [ ] No debug code or temporary files remain
- [ ] No secrets, tokens, or customer data are included
- [ ] Generated scan artifacts are not committed