# Privacy Policy

**Effective date:** April 3, 2026

Greenlight Actions is operated by [Praxiom Systems LLC](https://praxiomsystems.com/).

## What Greenlight Does

Greenlight Actions is a GitHub App that gates CI workflows behind manual approval on pull requests. It receives webhook events from GitHub, creates check runs, and approves deployment protection rules when a user clicks "Run CI."

## Data We Collect

**None.** Greenlight Actions does not collect, store, or transmit any user data.

### Technical Details

- **Stateless architecture.** There is no database, file storage, cache, or persistent state of any kind.
- **Webhook payloads** are processed in memory and discarded immediately after the request completes. Nothing is written to disk or forwarded to third parties.
- **No source code access.** The app never reads, clones, or stores your source code.
- **No secrets access.** The app never sees repository secrets, tokens, or environment variables.
- **No analytics or tracking.** There are no cookies, tracking pixels, or analytics scripts.

### What GitHub Sends Us

GitHub sends webhook payloads containing:
- Repository name and owner
- Pull request branch and commit SHA
- Workflow run ID and environment name

This data is used solely to create and update check runs and approve deployment protection rules. It is not logged, stored, or shared.

## Third-Party Services

Greenlight Actions runs on [Cloudflare Workers](https://workers.cloudflare.com/). Cloudflare may collect standard request metadata (IP addresses, request headers) as part of their infrastructure. See [Cloudflare's privacy policy](https://www.cloudflare.com/privacypolicy/) for details.

## Permissions

Greenlight requests the minimum GitHub permissions required to function. See the [permissions table](README.md#permissions-explained) for a full explanation of each permission and why it is needed.

## Changes to This Policy

If this policy changes, the updated version will be published in this repository with a new effective date. Since we collect no data, meaningful changes are unlikely.

## Contact

For privacy questions, contact us at greenlight@praxiomsystems.com.
