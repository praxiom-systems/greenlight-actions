# Marketplace Listing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up the greenlight-actions public repo with all files needed for a GitHub Marketplace listing — README, LICENSE, supporting docs, and issue templates.

**Architecture:** Flat repo structure. README.md serves as the Marketplace landing page and primary documentation. Supporting files (LICENSE, SECURITY.md, SUPPORT.md, CHANGELOG.md) at the root. Issue templates in `.github/ISSUE_TEMPLATE/`. Screenshots directory at `assets/screenshots/`.

**Tech Stack:** Markdown, GitHub YAML issue template forms

**Spec:** `docs/superpowers/specs/2026-04-03-marketplace-listing-design.md`

**Reference:** Internal repo at `../greenlight-actions-internal` — the README there is the content source, adapted for a public/Marketplace audience.

---

### Task 1: LICENSE

**Files:**
- Create: `LICENSE`

- [ ] **Step 1: Create the LICENSE file**

```
MIT License

Copyright (c) 2026 Praxiom Systems LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Commit**

```bash
git add LICENSE
git commit -m "Add MIT license"
```

---

### Task 2: README.md

**Files:**
- Modify: `README.md` (replace placeholder content)

**Context:** Adapt content from `../greenlight-actions-internal/README.md` for a public/Marketplace audience. More product-focused, less developer-focused. Do NOT include Contributing or Self-Hosting sections (those belong in the internal repo). DO include a link to the Praxiom Systems website.

- [ ] **Step 1: Write the full README**

Replace the entire contents of `README.md` with the following. This is the complete file:

```markdown
# Greenlight Actions

Gate CI behind manual approval. Zero wasted minutes.

[![Install](https://img.shields.io/badge/Install-GitHub_Marketplace-blue)](https://github.com/apps/greenlight-actions)

Greenlight adds a gate to your existing CI pipeline. Workflows still trigger on every push, but the actual work pauses until a developer clicks "Run CI" on the pull request. No more burned minutes on WIP commits, typo fixes, or mid-rebase pushes.

<!-- TODO: Add screenshot of PR check with "Run CI" button -->

---

## How It Works

1. **You push code to a PR.** Your workflow triggers normally, but the CI job pauses at the Greenlight gate. A check appears with a "Run CI" button.
2. **You click when ready.** One click approves the gate and your CI job continues. No context switching, no CLI commands, no waiting for a build you did not want.
3. **You push again, the gate resets.** Every new commit re-triggers the workflow and pauses it again, so stale green checks never linger on changed code.

Your workflow file stays the same. Greenlight only controls _when_ the work runs.

> **How is this different from polling-based solutions?** Greenlight uses GitHub's [deployment protection rules](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/creating-custom-deployment-protection-rules). The workflow truly pauses — zero Actions minutes are consumed while waiting for approval.

---

## Get Started

### 1. Install Greenlight

[Install Greenlight](https://github.com/apps/greenlight-actions) on your GitHub organization or repositories. Setup takes under a minute.

### 2. Add the Greenlight Environment to Your Job

Add `environment: greenlight` to any job you want Greenlight to gate. Keep your existing triggers — Greenlight works alongside them.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    environment: greenlight
    steps:
      - uses: actions/checkout@v4
      # ... your existing steps unchanged
```

### 3. Open a Pull Request

Push a branch and open a PR. Your workflow will start, pause at the `greenlight` environment gate, and you will see a "Greenlight Actions: CI" check with a "Run CI" button. Click it when your code is ready.

That is it. No config files, no dashboard, no CLI.

### Workflows That Also Run on Push

If your workflow also runs on `push` (e.g., to run CI after merging to `main`), conditionally apply the environment so the gate only fires on PRs:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    environment: ${{ github.event_name == 'pull_request' && 'greenlight' || '' }}
    steps:
      - uses: actions/checkout@v4
      # ... your existing steps unchanged
```

On a pull request, the job uses the `greenlight` environment and pauses at the gate. On a push to `main`, the expression evaluates to an empty string (no environment), so the job runs immediately with no gate.

> **Why not use environment branch restrictions instead?** GitHub's environment branch restrictions (Settings > Environments > Deployment branches) will _fail_ the job on disallowed branches rather than skip the gate. The conditional environment approach above is more reliable and does not require a paid GitHub plan for private repositories.

---

## Why Greenlight

| Problem | How Greenlight Helps |
|---------|---------------------|
| CI runs on every push, burning minutes on WIP code | Workflows trigger normally but pause until you click "Run CI" — no compute burned on WIP |
| Red checks on incomplete work train people to ignore failures | Checks stay neutral ("waiting for you to greenlight") until explicitly triggered |
| Stale green checks on outdated commits give false confidence | Every new push re-triggers the workflow and pauses at the gate again |
| Gating CI requires custom scripts or branch rules | One-click install, one-line workflow change |
| Third-party CI tools require credentials and config | Stateless, serverless — add one line to your workflow and you are done |

### Alternatives Compared

| Alternative | Limitation Greenlight Solves |
|------------|---------------------------|
| GitHub Environment Required Reviewers | Requires Enterprise ($21/user/mo) for private repos |
| Polling-based approval Actions | Burns Actions minutes while waiting for approval |
| Removing `pull_request` trigger entirely | Terrible DX — requires navigating to Actions tab, entering branch name |
| `concurrency` + `cancel-in-progress` | Doesn't prevent the initial trigger, just cancels overlapping runs |

---

## Security and Privacy

Greenlight is designed to touch as little as possible.

- **Stateless.** No database, no file storage, no persistent state of any kind. Every request is processed and forgotten.
- **No code access.** Greenlight never reads, clones, or stores your source code. It only interacts with the Checks and Deployments APIs.
- **No secrets exposure.** It never sees or handles your repository secrets, tokens, or environment variables.
- **No logging of content.** Webhook payloads are processed in memory and discarded. Nothing is written to disk or sent to third parties.
- **Minimal permissions.** Only the permissions strictly required to create check runs and approve deployment protection rules.

### Permissions Explained

Greenlight requests the minimum permissions required to function:

| Permission | Access | Why |
|------------|--------|-----|
| **Checks** | Read & Write | Create the "Greenlight Actions: CI" check run on PRs, update its status when CI starts |
| **Actions** | Read & Write | Approve deployment protection rules to allow gated CI jobs to proceed |
| **Deployments** | Read & Write | Respond to deployment protection rule requests from GitHub |
| **Pull Requests** | Read | Read PR metadata (branch, SHA, repository) to associate checks with the correct commit |

The app subscribes to two webhook events:
- **Deployment protection rule** (`requested`) — to create the check run with a "Run CI" button when a workflow pauses at the `greenlight` environment gate
- **Check run** (`requested_action`) — to respond when a developer clicks the "Run CI" button

---

## FAQ

**No check is appearing on my PR.**
Make sure the job in your workflow has `environment: greenlight` set. The Greenlight gate only activates when the workflow reaches that environment.

**The check appeared but nothing happens when I click "Run CI".**
Verify that the Greenlight app is installed on the repository (not just the organization). Check Settings > Integrations > GitHub Apps.

**Does Greenlight work on forked PRs?**
No. Deployment protection rules are a repository-level feature and do not apply to workflows triggered from forks.

**Can I gate multiple jobs in the same workflow?**
Yes. Add `environment: greenlight` to each job you want to gate. Each job gets its own independent "Run CI" button.

**Does Greenlight work with private repositories?**
Yes. Deployment protection rules work on both public and private repositories on all GitHub plans.

---

## Support

See [SUPPORT.md](SUPPORT.md) for how to get help, report bugs, or request features.

---

## License

[MIT](LICENSE) — Copyright (c) 2026 [Praxiom Systems LLC](https://praxiomsystems.com/)
```

Note the `<!-- TODO: Add screenshot -->` comment near the top — the user will replace this with actual screenshots.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Replace placeholder README with full product documentation"
```

---

### Task 3: CHANGELOG.md

**Files:**
- Create: `CHANGELOG.md`

- [ ] **Step 1: Create the CHANGELOG**

```markdown
# Changelog

All notable changes to Greenlight Actions will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-04-03

### Added

- Initial public release
- Gate CI behind manual approval on pull requests
- Zero Actions minutes burned while waiting (deployment protection rules)
- One-click "Run CI" button on PR checks
- Every push re-gates — no stale green checks
- Fully stateless architecture — no database, no persistent storage
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "Add changelog with initial release entry"
```

---

### Task 4: SECURITY.md

**Files:**
- Create: `SECURITY.md`

- [ ] **Step 1: Create SECURITY.md**

```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Greenlight Actions, please report it responsibly.

**Preferred:** Use [GitHub's private vulnerability reporting](https://github.com/rrlamichhane/greenlight-actions/security/advisories/new) to submit a report directly on this repository.

**Email:** If you prefer email, contact us at security@praxiomsystems.com.

### What to Expect

- **Acknowledgement** within 48 hours of your report
- **Assessment and timeline** within 5 business days
- **Resolution** as quickly as possible, depending on severity

### What Qualifies as a Security Issue

- Webhook signature bypass or verification flaws
- Unauthorized approval of deployment protection rules
- Information disclosure through the app's API interactions
- Any way to escalate permissions beyond what the app requests

### What Is NOT a Security Issue

- Bugs in CI workflow configuration (these are GitHub Actions issues)
- Feature requests or usability issues — please use [GitHub Issues](https://github.com/rrlamichhane/greenlight-actions/issues)

## Architecture

Greenlight Actions is fully stateless. It has no database, no file storage, and no persistent state. Webhook payloads are processed in memory and discarded. The app never reads, clones, or stores source code, and never accesses repository secrets or environment variables.
```

- [ ] **Step 2: Commit**

```bash
git add SECURITY.md
git commit -m "Add security policy with disclosure instructions"
```

---

### Task 5: SUPPORT.md

**Files:**
- Create: `SUPPORT.md`

- [ ] **Step 1: Create SUPPORT.md**

```markdown
# Support

## Getting Help

- **Bug reports:** [File a bug report](https://github.com/rrlamichhane/greenlight-actions/issues/new?template=bug_report.yml)
- **Feature requests:** [Request a feature](https://github.com/rrlamichhane/greenlight-actions/issues/new?template=feature_request.yml)
- **Security issues:** See [SECURITY.md](SECURITY.md) for responsible disclosure

## Before Filing an Issue

1. Check the [FAQ](README.md#faq) for common questions
2. Search [existing issues](https://github.com/rrlamichhane/greenlight-actions/issues) to avoid duplicates

## Response Times

Greenlight Actions is maintained by [Praxiom Systems LLC](https://praxiomsystems.com/). We provide best-effort community support. There is no SLA for the free tier.

## Source Code

The application source code is maintained in a [separate repository](https://github.com/praxiom-systems/greenlight-actions-internal).
```

- [ ] **Step 2: Commit**

```bash
git add SUPPORT.md
git commit -m "Add support guide"
```

---

### Task 6: Issue Templates

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`

- [ ] **Step 1: Create bug report template**

Create `.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug Report
description: Report a problem with Greenlight Actions
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug. Please fill out the details below so we can investigate.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: What happened? What did you expect to happen?
    validations:
      required: true

  - type: dropdown
    id: repo-visibility
    attributes:
      label: Repository Visibility
      description: Is the affected repository public or private?
      options:
        - Public
        - Private
    validations:
      required: true

  - type: textarea
    id: workflow
    attributes:
      label: Workflow File
      description: Paste the relevant portion of your workflow YAML (especially the job with `environment: greenlight`)
      render: yaml

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened?
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Any other information that might help (screenshots, links to workflow runs, etc.)
```

- [ ] **Step 2: Create feature request template**

Create `.github/ISSUE_TEMPLATE/feature_request.yml`:

```yaml
name: Feature Request
description: Suggest an improvement or new feature
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting an improvement. Please describe the problem you're trying to solve and your ideal solution.

  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this feature solve? What are you trying to do?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How would you like this to work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Have you considered any alternative approaches?

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Any other information or screenshots
```

- [ ] **Step 3: Commit**

```bash
git add .github/ISSUE_TEMPLATE/bug_report.yml .github/ISSUE_TEMPLATE/feature_request.yml
git commit -m "Add bug report and feature request issue templates"
```

---

### Task 7: Screenshots Directory and CLAUDE.md

**Files:**
- Create: `assets/screenshots/.gitkeep`
- Create: `.claude/CLAUDE.md`

- [ ] **Step 1: Create screenshots directory**

```bash
mkdir -p assets/screenshots
touch assets/screenshots/.gitkeep
```

- [ ] **Step 2: Create CLAUDE.md**

Create `.claude/CLAUDE.md` with project context for future sessions:

```markdown
# Greenlight Actions (Public Repo)

This is the public-facing repository for Greenlight Actions — a GitHub App that gates CI behind manual approval on pull requests.

## Repository Purpose

This repo serves as the:
- **GitHub Marketplace listing** — README is the landing page
- **Documentation hub** — how it works, setup guide, FAQ
- **Issue tracker** — bug reports and feature requests from users

## Source Code

The application source code is in a separate repository:
- Local: `../greenlight-actions-internal`
- GitHub: https://github.com/praxiom-systems/greenlight-actions-internal

## Key Details

- **Company:** Praxiom Systems LLC (https://praxiomsystems.com/)
- **License:** MIT
- **Architecture:** Stateless Cloudflare Worker, two-event flow (deployment protection rule → check run)
- **Permissions:** Checks R&W, Actions R&W, Deployments R&W, Pull Requests Read
```

- [ ] **Step 3: Commit**

```bash
git add assets/screenshots/.gitkeep .claude/CLAUDE.md
git commit -m "Add screenshots directory and project CLAUDE.md"
```

---

### Task 8: Final Verification

- [ ] **Step 1: Verify all files exist**

```bash
ls -la README.md LICENSE CHANGELOG.md SECURITY.md SUPPORT.md
ls -la .github/ISSUE_TEMPLATE/bug_report.yml .github/ISSUE_TEMPLATE/feature_request.yml
ls -la assets/screenshots/.gitkeep
ls -la .claude/CLAUDE.md
```

Expected: All files listed with no errors.

- [ ] **Step 2: Verify git status is clean**

```bash
git status
```

Expected: `nothing to commit, working tree clean`

- [ ] **Step 3: Review README renders correctly**

```bash
cat README.md | head -5
```

Expected: Starts with `# Greenlight Actions`

- [ ] **Step 4: Verify issue template YAML is valid**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/ISSUE_TEMPLATE/bug_report.yml')); print('bug_report.yml: valid')"
python3 -c "import yaml; yaml.safe_load(open('.github/ISSUE_TEMPLATE/feature_request.yml')); print('feature_request.yml: valid')"
```

Expected: Both print "valid"
