# Notes for writing your Show HN submission

These are planning notes, not submission copy. HN's [guidelines](https://news.ycombinator.com/newsguidelines.html) prohibit generated submission text and generated or AI-edited comments. Write the submission yourself from your own experience rather than pasting these notes or the other drafts.

## What to cover in your own words

- Start the title with `Show HN:` and state plainly what you built.
- Explain the specific CI problem you encountered in work and personal projects. Use a real example if you have one; don't invent costs or time savings.
- Describe the PR button and `/greenlight`, leaving fast checks automatic, and approval for the current commit.
- Explain what this adds over native environment approvals and `workflow_dispatch`.
- Mention the two modes and support for Free private repos through dispatch.
- Be clear that installation requires repository permissions and workflow setup. The backend source is maintained separately; the public repository contains documentation and examples.
- Include the current dispatch limits: same-repository PRs, no merge queues, and no resetting a finished result for a same-commit rerun.
- Say that the app is free and regular Actions billing still applies.

## Give people something to try

- Link to the [public repository and setup](https://github.com/praxiom-systems/greenlight-actions) and the [App listing](https://github.com/marketplace/greenlight-actions).
- Consider adding a short recording of a real PR: quick checks run, expensive work waits, you approve it, and the result appears. There is no recording attached to these notes.
- Be available to answer questions about App permissions, commit matching, workflow context, and the limitations documented in the mode guide.

Read the [Show HN requirements](https://news.ycombinator.com/showhn.html) before submitting. HN also describes [restrictions for accounts unfamiliar with the community](https://news.ycombinator.com/showlim); eligibility is not guaranteed.
