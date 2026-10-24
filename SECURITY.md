# Security Policy

Greenlight supports native environment approvals and workflow dispatch approvals. Report unauthorized approvals or dispatches, incorrect commit/result association, and unexpected changes of approval mode. The App does not read source files or repository secrets. Small routing and mode records are stored in GitHub check runs; there is no app-owned database or file storage. See the [mode guide](docs/approval-modes.md) for current dispatch limitations, including simultaneous duplicate approvals and same-SHA reruns.

## Reporting a Vulnerability

If you discover a security vulnerability in Greenlight Actions, please report it responsibly.

**Preferred:** Use [GitHub's private vulnerability reporting](https://github.com/praxiom-systems/greenlight-actions/security/advisories/new) to submit a report directly on this repository.

**Email:** If you prefer email, contact us at <greenlight@praxiomsystems.com>.

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
- Feature requests or usability issues — please use [GitHub Issues](https://github.com/praxiom-systems/greenlight-actions/issues)

## Architecture

Greenlight Actions has no app-owned database or file storage. Raw webhook payloads are processed in memory and discarded. GitHub check runs retain the small routing, selected-mode, and result records used across requests. The App never reads, clones, or stores source code, and never accesses repository secrets or environment variables.
