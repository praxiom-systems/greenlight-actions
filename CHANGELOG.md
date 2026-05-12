# Changelog

All notable changes to Greenlight Actions will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-05-12

### Added

- PR comment trigger support: users with write, maintain, or admin repository access can comment `/greenlight` or `/greenlight run` to approve pending Greenlight checks.
- `Issue comment` webhook support for PR conversation comments.

## [1.0.0] - 2026-04-03

### Added

- Initial public release
- Gate CI behind manual approval on pull requests
- Zero Actions minutes burned while waiting (deployment protection rules)
- One-click "Run CI" button on PR checks
- Every push re-gates — no stale green checks
- Fully stateless architecture — no database, no persistent storage
