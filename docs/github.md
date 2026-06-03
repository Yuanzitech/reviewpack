# GitHub Pull Request Support

Reviewpack supports GitHub pull request workflows in stages.

The current GitHub mode can fetch pull request metadata and changed file statistics from the GitHub API.

## Supported URL format

Reviewpack supports GitHub pull request URLs in this format:

    https://github.com/owner/repo/pull/123

## Command

Generate a review pack from GitHub PR metadata:

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

Generate a review pack with AI input preview:

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack --preview-ai-input

Use a GitHub token explicitly:

    reviewpack github https://github.com/owner/repo/pull/123 --token YOUR_TOKEN --output .reviewpack

Or use an environment variable:

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

## What GitHub mode collects

The current GitHub mode collects:

- Pull request title
- Pull request author
- Pull request description
- Pull request URL
- Changed file paths
- Added line counts
- Deleted line counts

## What GitHub mode does not collect

The current GitHub mode does not collect:

- Raw diffs
- Full source code
- Branch names
- Commit messages
- Review comments
- Repository secrets
- Environment variables
- Terminal history

## Token policy

GitHub tokens are optional for public repositories, but they may be needed for private repositories or rate limits.

Reviewpack follows these rules:

- Tokens are user-provided
- Tokens are not stored by Reviewpack
- Tokens are not written to generated review packs
- Tokens are not printed in normal CLI output
- Tokens can be provided with `--token`
- Tokens can be provided with `REVIEWPACK_GITHUB_TOKEN`
- `GITHUB_TOKEN` is supported as a fallback for CI environments

## Privacy behavior

GitHub mode uses network access because it calls the GitHub API.

It does not call AI providers.

It does not upload code to Reviewpack services because Reviewpack has no hosted service.

It only reads explicitly requested pull request metadata and changed file statistics from GitHub.

## Output

The command writes:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

When `--preview-ai-input` is enabled, it also writes:

    .reviewpack/ai-input-preview.md

## Limitations

The current GitHub mode does not yet support:

- GitHub Enterprise hosts
- GitLab or Bitbucket
- Linked issue collection
- CI status collection
- Review comment collection
- Raw diff analysis
- GitHub Action PR comments

These may be added later with explicit privacy controls.
