# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Greenlight Actions, please report it responsibly.

**Preferred:** Use [GitHub's private vulnerability reporting](https://github.com/rrlamichhane/greenlight-actions/security/advisories/new) to submit a report directly on this repository.

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
- Feature requests or usability issues — please use [GitHub Issues](https://github.com/rrlamichhane/greenlight-actions/issues)

## Architecture

Greenlight Actions is fully stateless. It has no database, no file storage, and no persistent state. Webhook payloads are processed in memory and discarded. The app never reads, clones, or stores source code, and never accesses repository secrets or environment variables.
