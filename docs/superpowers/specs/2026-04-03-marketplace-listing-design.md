# Greenlight Actions — Public Repo & Marketplace Listing Design

## Overview

Set up the `greenlight-actions` public repository as the product storefront, documentation hub, and issue tracker for the GitHub Marketplace listing. Source code is maintained separately at `https://github.com/praxiom-systems/greenlight-actions-internal`.

## Goals

1. Meet all GitHub Marketplace listing requirements
2. Provide high-ROI documentation that helps users install and trust the app
3. Establish community infrastructure (issue templates, support channels)

## Repository Structure

```
greenlight-actions/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── SECURITY.md
├── SUPPORT.md
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.yml
│       └── feature_request.yml
└── assets/
    └── screenshots/          # User-provided screenshots of approval flow
```

No Marketplace manifest file — configuration is done through the GitHub App settings UI.

## README.md

The README serves as the Marketplace landing page and primary documentation. Flat structure — all content in one file.

### Sections

1. **Header** — App name + one-line tagline: "Gate CI behind manual approval. Zero wasted minutes."

2. **How It Works** — 3-step explanation of the flow:
   - Push to PR triggers workflow
   - Workflow pauses at deployment protection rule gate
   - Developer clicks "Run CI" to approve; workflow resumes
   - Brief technical note: uses deployment protection rules (not polling), so zero Actions minutes burned while waiting. Every push re-gates — no stale green checks.

3. **Get Started** — 3 steps:
   1. Install the app (link to GitHub App install URL)
   2. Add `environment: greenlight` to workflow job
   3. Open a PR — click "Run CI" when ready
   - Include basic workflow YAML snippet

4. **Workflow Examples** — Two examples:
   - Basic: workflow triggered by `push` with `environment: greenlight` on the job
   - Multi-trigger: conditional environment (`${{ github.event_name == 'pull_request' && 'greenlight' || '' }}`) for workflows that run on both `pull_request` and `push`

5. **Why Greenlight** — Comparison table:

   | Alternative | Limitation Greenlight solves |
   |---|---|
   | GitHub Environment Required Reviewers | Requires Enterprise ($21/user/mo) for private repos |
   | Polling-based approval Actions | Burns Actions minutes while waiting |
   | Removing `pull_request` trigger | Bad DX — must navigate to Actions tab manually |
   | `concurrency` + `cancel-in-progress` | Doesn't prevent initial trigger, just cancels overlapping runs |

6. **Permissions** — Table explaining each permission:

   | Permission | Access | Why |
   |---|---|---|
   | Checks | Read & Write | Create and update the check run with "Run CI" button |
   | Actions | Read & Write | Approve deployment protection rules |
   | Deployments | Read & Write | Respond to deployment protection rule requests |
   | Pull Requests | Read | Associate checks with the correct PR commit |

7. **Security & Privacy** — Key points:
   - Fully stateless — no database, no persistent storage
   - Never reads, clones, or stores source code
   - Never accesses repository secrets or environment variables
   - Webhook payloads processed in memory and discarded
   - All webhooks verified with HMAC-SHA256
   - Link to SECURITY.md for disclosure policy

8. **FAQ / Troubleshooting** — Common issues:
   - No check appearing → environment `greenlight` not configured on the job
   - Check stuck → app not installed on the repository
   - Works on forks → no (deployment protection rule limitation)
   - Multiple jobs → each job with `environment: greenlight` gets its own gate

9. **Support** — Link to SUPPORT.md, issue templates

10. **License** — MIT, link to LICENSE

### Content Source

Adapted from the internal repo's README (`../greenlight-actions-internal/README.md`), rewritten for a public/Marketplace audience — more product-focused, less developer-focused.

## LICENSE

MIT License, copyright 2026 Praxiom Systems LLC.

## CHANGELOG.md

[Keep a Changelog](https://keepachangelog.com/) format.

```markdown
## [1.0.0] - 2026-04-03
### Added
- Initial public release
- Gate CI behind manual approval on pull requests
- Zero Actions minutes burned while waiting (deployment protection rules)
- One-click "Run CI" button on PR checks
- Every push re-gates — no stale green checks
- Fully stateless architecture
```

## SECURITY.md

- Use GitHub's private vulnerability reporting (preferred)
- Email fallback for disclosure (security@praxiomsystems.com or user-specified)
- Statement: stateless architecture, no user data stored, no code access
- Response commitment: acknowledge within 48 hours, provide timeline within 5 business days
- Scope: what qualifies as a security issue vs. a regular bug

## SUPPORT.md

- GitHub Issues for bugs and feature requests (with links to templates)
- Note that source code is maintained separately
- Best-effort community support (no SLA)

## Issue Templates

### Bug Report (`bug_report.yml`)
YAML form with fields:
- Description (textarea, required)
- Repository visibility: public or private (dropdown, required)
- Workflow snippet (textarea, optional — for reproducing)
- Expected behavior (textarea, required)
- Actual behavior (textarea, required)
- Additional context (textarea, optional)

### Feature Request (`feature_request.yml`)
YAML form with fields:
- Problem description (textarea, required)
- Proposed solution (textarea, required)
- Alternatives considered (textarea, optional)
- Additional context (textarea, optional)

## Screenshots

User will provide screenshots showing:
- PR check run with "Run CI" button (waiting state)
- Check run in progress (spinner)
- Check run completed (green check with link to workflow)

Screenshots stored in `assets/screenshots/` and referenced from README.

## Out of Scope

- Application source code (separate repo)
- Marketplace configuration UI settings (done in GitHub App settings)
- Logo/icon creation (can be added later)
- Pricing plan configuration (launching as free)
- Landing page beyond README
