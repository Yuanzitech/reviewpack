# GitHub Pull Request Mode

Reviewpack can generate review context from a GitHub pull request URL.

Example:

    reviewpack github https://github.com/owner/repo/pull/123

Reviewpack writes output to `.reviewpack/` by default.

## What GitHub mode collects

GitHub mode collects metadata from the GitHub API.

It may collect:

- Pull request title
- Pull request author
- Pull request URL
- Pull request description
- Pull request state
- Draft status
- Base branch name
- Head branch name
- Commit count
- Labels
- Changed file paths
- Changed file status
- Added line counts
- Deleted line counts

## What GitHub mode does not collect by default

GitHub mode does not collect by default:

- Raw diffs
- Full source code
- Review comments
- Commit messages
- Secrets
- Local environment variables

Reviewpack does not call AI providers by default.

The user remains in control of which generated artifacts are shared with AI tools.

## Public repositories

For public repositories, GitHub mode usually works without a token.

Example:

    reviewpack github https://github.com/owner/repo/pull/123

However, unauthenticated GitHub API requests may be rate-limited.

## Private repositories and rate limits

Private repositories or rate-limited usage require a GitHub token.

Recommended local usage:

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123

Avoid putting long-lived tokens directly into shell history when possible.

## GitHub Actions

In GitHub Actions, pass the workflow token:

    github-token: ${{ github.token }}

Recommended permissions:

    permissions:
      contents: read
      pull-requests: read

See:

    docs/github-action.md

## Output metadata

When available, GitHub metadata is included in:

    pr-summary.md
    ai-review-prompt.md
    ai-context.md
    reviewpack.json

Example metadata:

    State: open
    Draft: false
    Base branch: main
    Head branch: feature/docs
    Commits: 3
    Labels: documentation, enhancement

Changed files may include status information such as:

    added
    modified
    removed
    renamed

## Error handling

Reviewpack provides friendlier error messages for common GitHub API failures.

### 401 Unauthorized

The token may be missing, invalid, or expired.

### 403 Forbidden

This may be caused by API rate limits or insufficient token permissions.

### 404 Not Found

The pull request may not exist, or the repository may not be accessible with the current token.

## Privacy notes

GitHub mode uses network access to fetch the explicitly requested pull request metadata.

It does not send data to AI providers.

It does not upload source code.

It does not collect raw diffs by default.
