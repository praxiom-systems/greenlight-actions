# Privacy Policy

**Effective date:** October 22, 2026

Greenlight Actions is operated by [Praxiom Systems LLC](https://praxiomsystems.com/).

## What Greenlight Does

Greenlight Actions is a GitHub App that gates CI workflows behind manual approval on pull requests. It receives GitHub webhooks, inspects environment rules and workflow metadata, and creates setup, approval, and result checks. When a user clicks "Run CI" or comments `/greenlight`, it either approves a deployment protection rule or dispatches a workflow. It reads workflow results to update dispatch checks.

## Data We Collect

Greenlight processes the GitHub metadata needed to provide approvals and checks. It has no app-owned database or file storage and does not collect analytics. It creates and updates check records in GitHub as described below.

### Technical Details

- **No app-owned storage.** There is no database or application file storage. Mode selection and routing metadata are recorded in GitHub check runs: repository/PR identifiers, commit SHA, workflow/environment names, check/run identifiers, and the selected mode. These records remain in GitHub subject to GitHub's retention and access controls.
- **Webhook payloads** are processed in memory and discarded immediately after the request completes. Nothing is written to disk or forwarded to third parties.
- **No source code access.** The app never reads, clones, or stores your source code.
- **No secrets access.** The app never sees repository secrets, tokens, or environment variables.
- **No analytics or tracking.** There are no cookies, tracking pixels, or analytics scripts.

### What GitHub Sends Us

GitHub sends webhook payloads containing:

- Repository name and owner
- Pull request branch and commit SHA
- Workflow run ID, status, conclusion, and environment name
- For the `issue_comment` webhook, the body and author metadata for newly-created issue and PR comments on installed repositories

Greenlight checks whether each comment is on a PR and matches `/greenlight` or `/greenlight run`. Non-matching comments and regular issue comments are ignored. Payloads are processed in memory to inspect setup, create/update GitHub checks, approve deployment protection rules, dispatch workflows, and process valid commands and results. Raw webhook payloads and comment bodies are not logged or retained by the App. The small GitHub check records described above are written back to GitHub; source files and repository secrets are not read.

## Third-Party Services

Greenlight Actions runs on [Cloudflare Workers](https://workers.cloudflare.com/). Cloudflare may collect standard request metadata (IP addresses, request headers) as part of their infrastructure. See [Cloudflare's privacy policy](https://www.cloudflare.com/privacypolicy/) for details.

## Permissions

Greenlight requests the minimum GitHub permissions required to function. See the [permissions table](README.md#permissions-explained) for a full explanation of each permission and why it is needed.

## Changes to This Policy

If this policy changes, the updated version will be published in this repository with a new effective date.

## Contact

For privacy questions, contact us at <greenlight@praxiomsystems.com>.
