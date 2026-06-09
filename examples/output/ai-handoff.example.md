# AI Handoff

Please read the Reviewpack files in this directory and use them to review the pull request.

Start with:

- ai-review-prompt.md
- pr-summary.md
- risk-checklist.md
- reviewer-checklist.md
- release-note-hints.md

## Pull Request

- Title: Add token refresh support
- Author: demo-user
- URL: https://github.com/octo-org/example-repo/pull/123

## Instructions for the AI assistant

- Use the Reviewpack artifacts as review context.
- Do not assume hidden code or files that are not available.
- Do not claim that raw source code was inspected unless source code was provided separately.
- Prefer concrete, actionable maintainer feedback.
- Focus on correctness, tests, compatibility, security-sensitive changes, and maintainability.
- Treat Reviewpack output as context for human review, not as ground truth.

## If files are not accessible

If local files cannot be accessed, ask the user to upload or paste:

- ai-review-prompt.md

If the user can upload multiple files, also ask for:

- pr-summary.md
- risk-checklist.md
- reviewer-checklist.md
- release-note-hints.md

## Privacy notes

- Reviewpack does not call an AI provider by default.
- Reviewpack does not upload raw diffs or full source code by default.
- Reviewpack does not require branch names or commit messages for this handoff.
- The user remains in control of what is shared with AI tools.
