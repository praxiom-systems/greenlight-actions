# Publishing the Marketplace listing

The listing has two description fields. Each file contains only the copy for its field; paste the entire file without these publishing instructions.

| Marketplace field | File | Maximum characters |
| --- | --- | --- |
| Introductory description, shown at the top | [marketplace-introduction.md](marketplace-introduction.md) | 500 |
| Detailed description, shown below the introduction | [marketplace-listing.md](marketplace-listing.md) | 2,000 |

Count Markdown, whitespace, and link URLs toward the limits. The detailed description uses absolute links so they work outside this repository. Repository edits do not publish changes to Marketplace.

Check both lengths after editing:

```sh
wc -m docs/marketplace-introduction.md docs/marketplace-listing.md
```

## Copy each description

From the repository root, copy and paste the introduction first, then copy and paste the detailed description. Run each command separately so the second does not overwrite the clipboard before you paste the first.

Linux with X11:

```sh
xclip -selection clipboard < docs/marketplace-introduction.md
```

```sh
xclip -selection clipboard < docs/marketplace-listing.md
```

macOS:

```sh
pbcopy < docs/marketplace-introduction.md
```

```sh
pbcopy < docs/marketplace-listing.md
```

Linux with Wayland and wl-clipboard installed:

```sh
wl-copy < docs/marketplace-introduction.md
```

```sh
wl-copy < docs/marketplace-listing.md
```

## Free plan

Use these values when editing the free plan:

- **Name:** Free
- **Description:** Free for personal projects and teams. Run expensive CI when you're ready.
- **Features:** PR approval button; `/greenlight` comment command; environment and dispatch modes; private repositories on GitHub Free through dispatch.

Confirm the plan is available to both personal accounts and organizations. Remove personal-use-only wording and the claim that every setup needs only one line of YAML.

## Resource links

- **Documentation:** <https://github.com/praxiom-systems/greenlight-actions#readme>
- **Support:** <https://github.com/praxiom-systems/greenlight-actions/blob/main/SUPPORT.md>
- **Privacy policy:** <https://github.com/praxiom-systems/greenlight-actions/blob/main/PRIVACY.md>
- **Terms of Service:** Replace the current link to `SECURITY.md` with the actual published terms. This repository currently has no Terms of Service document; do not relabel the security policy as terms.

## Screenshots and release checks

- Confirm the matching backend is deployed and the production App has the webhook subscriptions and permissions described in the [README](../README.md#security-and-permissions).
- Keep environment screenshots labeled as environment mode. Environment setup must show the enabled Greenlight protection rule, not just an environment with the right name.
- Add a dispatch screenshot showing the Run CI approval and Dispatch CI result checks, and label it as working with private repos on GitHub Free.
- Preview the Markdown, verify links, and check that both account types can select the free plan before publishing.
- Revisit the [live listing](https://github.com/marketplace/greenlight-actions) after saving; repository edits do not update its description or plan settings automatically.
