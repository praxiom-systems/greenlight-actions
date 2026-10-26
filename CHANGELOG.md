# Changelog

All notable changes to Greenlight Actions will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Dual-mode approval documentation and matching environment/dispatch workflow examples.
- Automatic selection guidance, explicit mode overrides, setup recovery, and configuration conflict handling for the matching backend release.
- Confirmed live dispatch testing in a private repository owned by a GitHub Free personal account, with both buttons and comments and passing/failing results.

### Fixed

- Corrected repository support: the current environment gate works for public repositories on all GitHub plans; private and internal repositories require GitHub Enterprise.
- Clarified public-repository benefits and billing, the environment protection rule setup, native approval alternatives, and environment approval timeouts.

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
