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
- GitHub: <https://github.com/praxiom-systems/greenlight-actions-internal>

## Key Details

- **Company:** Praxiom Systems LLC (<https://praxiomsystems.com/>)
- **License:** MIT
- **Architecture:** Stateless Cloudflare Worker, two-event flow (deployment protection rule → check run)
- **Permissions:** Checks R&W, Actions R&W, Deployments R&W, Pull Requests Read
