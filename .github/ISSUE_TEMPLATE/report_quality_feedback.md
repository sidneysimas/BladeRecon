---
name: Report Quality Feedback
about: Help improve BladeRecon reports, prioritization, confidence, and researcher guidance
title: "[Report Quality]: "
labels:
  - report-quality
assignees: ""
---

# Summary

Briefly describe the report quality issue or suggestion.

---

# Target Information

**Do not include unauthorized third-party target names.**

Target type:

- [ ] Bug bounty program
- [ ] Internal application
- [ ] Staging environment
- [ ] Production environment
- [ ] Static website
- [ ] API-heavy application
- [ ] Cloud infrastructure
- [ ] Other

---

# BladeRecon Information

- BladeRecon version:
- Scan profile:
  - [ ] Safe
  - [ ] Balanced
  - [ ] Aggressive

- Scan type:
  - [ ] Full
  - [ ] Resume
  - [ ] Report

---

# Report Area

Which section needs improvement?

- [ ] Executive Summary
- [ ] Opportunity Prioritization
- [ ] Investigation Queue
- [ ] Campaigns
- [ ] Risk Score
- [ ] Technology
- [ ] Endpoints
- [ ] Parameters
- [ ] Secrets
- [ ] Screenshots
- [ ] Historical Findings
- [ ] Nuclei
- [ ] Recommendations
- [ ] Performance Analytics
- [ ] Overall Layout
- [ ] Other

---

# Scan Context

- Nuclei status:
- Opportunity count:
- Risk score:
- Relevant module status:
- Timed out modules:
- Skipped modules:

---

# What Was Helpful?

Describe what made the report useful.

---

# What Was Confusing Or Misleading?

Describe any section that:

- was unclear
- repeated information
- exaggerated confidence
- hid uncertainty
- wasted space
- distracted from important findings

---

# Why Did It Matter?

Examples:

- Changed investigation priority
- Increased false confidence
- Added unnecessary noise
- Made runtime difficult to interpret
- Slowed manual triage
- Missed an important finding

---

# Suggested Improvement

Describe how BladeRecon could present the information better.

---

# Supporting Evidence

Attach or summarize **sanitized** artifacts if available.

Examples:

- report.md
- report.html screenshots
- scan_state.json
- latest_run.json
- module metadata.json
- Opportunity snippets

---

# Data Safety Checklist

Before submitting:

- [ ] I removed secrets, API keys, cookies, tokens, and credentials.
- [ ] I removed customer or third-party confidential data.
- [ ] I only included data from targets I am authorized to share.
- [ ] Attached reports and logs have been sanitized.

---

# Additional Context

Include any additional notes, screenshots, comparisons, or examples from other security tools that may help improve the report.