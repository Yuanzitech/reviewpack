# GitHub Action

Reviewpack can run as a GitHub Action in pull request workflows.

The GitHub Action generates a Reviewpack output directory and uploads it as a workflow artifact.

It does not post pull request comments by default.

It does not call AI providers.

It does not approve or merge pull requests.

## Basic usage

Add a workflow file such as:

    name: Reviewpack

    on:
      pull_request:

    jobs:
      reviewpack:
        runs-on: ubuntu-latest

        permissions:
          contents: read
          pull-requests: read

        steps:
          - name: Check out repository
            uses: actions/checkout@v4

          - name: Run Reviewpack
            uses: Yuanzitech/reviewpack@v0.6.1
            with:
              mode: github
              pr-url: ${{ github.event.pull_request.html_url }}
              github-token: ${{ github.token }}

## Output

The action writes Reviewpack output files to:

    .reviewpack/

By default, this directory is uploaded as a workflow artifact named:

    reviewpack-output

The output may include:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-handoff.md
    .reviewpack/ai-context.md
    .reviewpack/reviewpack.json

If AI input preview is enabled, it also writes:

    .reviewpack/ai-input-preview.md

## Downloading artifacts

After the workflow finishes:

1. Open the GitHub Actions workflow run.
2. Find the Artifacts section.
3. Download the artifact named `reviewpack-output`.
4. Unzip the artifact locally.
5. Open the generated Reviewpack files.

Recommended first files to read:

    pr-summary.md
    reviewer-checklist.md
    risk-checklist.md
    release-note-hints.md

For AI handoff, start with:

    ai-handoff.md

If the AI assistant cannot read multiple files, upload:

    ai-context.md

If only copy and paste is available, use:

    ai-review-prompt.md

## Optional PR comment mode

Reviewpack can optionally post or update a short PR comment.

This is disabled by default.

Enable it with:

    comment: "true"

Example:

    name: Reviewpack

    on:
      pull_request:

    jobs:
      reviewpack:
        runs-on: ubuntu-latest

        permissions:
          contents: read
          pull-requests: write

        steps:
          - name: Check out repository
            uses: actions/checkout@v4

          - name: Run Reviewpack with PR comment
            uses: Yuanzitech/reviewpack@v0.6.1
            with:
              mode: github
              pr-url: ${{ github.event.pull_request.html_url }}
              github-token: ${{ github.token }}
              comment: "true"

The comment is intentionally short.

It points maintainers to:

    reviewpack-output
    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md
    ai-handoff.md
    ai-context.md
    ai-review-prompt.md

It does not paste the full review pack into the pull request.

## Comment update behavior

Reviewpack comments include a stable hidden marker:

    <!-- reviewpack-comment -->

If a previous Reviewpack comment exists, comment mode updates it.

If no previous Reviewpack comment exists, comment mode creates one.

This avoids duplicate Reviewpack comments on repeated workflow runs.

## Permissions

Artifact-only mode can use:

    permissions:
      contents: read
      pull-requests: read

Comment mode requires:

    permissions:
      contents: read
      pull-requests: write

Comment mode also requires:

    github-token: ${{ github.token }}
    pr-url: ${{ github.event.pull_request.html_url }}

Reviewpack does not store this token and does not write this token to generated output files.

## Fork pull request limitations

For pull requests from forks, GitHub may restrict write permissions for the workflow token.

This means optional comment mode may fail to create or update a PR comment on forked pull requests.

If that happens, use artifact-only mode instead:

    comment: "false"

Artifact generation can still work without PR comment mode.

Recommended default for broad open-source usage:

    permissions:
      contents: read
      pull-requests: read

Recommended setting only when comment mode is intentionally enabled:

    permissions:
      contents: read
      pull-requests: write

Avoid using `pull_request_target` unless the workflow security implications are fully understood.

## Troubleshooting

### pr-url is required

GitHub mode requires:

    pr-url: ${{ github.event.pull_request.html_url }}

Comment mode also requires `pr-url`.

### github-token is required for comment mode

Comment mode requires:

    github-token: ${{ github.token }}

If `github-token` is missing, Reviewpack cannot call the GitHub comments API.

### 401 Unauthorized

The token may be missing, invalid, or expired.

### 403 Forbidden

This may be caused by rate limits or insufficient token permissions.

For comment mode, confirm the workflow has:

    pull-requests: write

For artifact-only mode, use:

    pull-requests: read

### 404 Not Found

The pull request may not exist, or the repository may not be accessible with the current token.

### Fork PR comment failures

For forked pull requests, GitHub may restrict write permissions.

Use artifact-only mode if comment mode is not allowed.

### Artifact missing

Confirm artifact upload is enabled:

    upload-artifact: "true"

The action uploads hidden `.reviewpack/` output directories by default.

## Inputs

### mode

Supported values:

    github
    local

Default:

    github

### pr-url

GitHub pull request URL.

Required when mode is `github`.

Required when comment mode is enabled.

### github-token

Optional GitHub token for GitHub API requests.

Required when comment mode is enabled.

Recommended in GitHub Actions:

    github-token: ${{ github.token }}

### comment

Post or update a short Reviewpack summary comment on the pull request.

Default:

    false

Enable with:

    comment: "true"

### base

Base git ref for local mode.

Default:

    main

### head

Head git ref for local mode.

Default:

    HEAD

### output

Output directory for generated Reviewpack files.

Default:

    .reviewpack

### preview-ai-input

Generate a local AI input preview file.

Default:

    false

### upload-artifact

Upload the Reviewpack output directory as a workflow artifact.

Default:

    true

### artifact-name

Name of the uploaded artifact.

Default:

    reviewpack-output

## GitHub mode

GitHub mode fetches pull request metadata and changed file statistics from the GitHub API.

It may collect:

- Pull request title
- Pull request author
- Pull request description
- Pull request URL
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

It does not collect raw diffs or full source code by default.

## Local mode

Local mode runs Reviewpack using local git diff statistics.

Example:

    - name: Run Reviewpack in local mode
      uses: Yuanzitech/reviewpack@v0.6.1
      with:
        mode: local
        base: main
        head: HEAD

For pull request workflows, local mode depends on checkout depth and available refs.

Recommended checkout for local mode:

    - name: Check out repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

## AI handoff from artifacts

The action does not call AI providers.

Instead, it generates files that users can inspect and intentionally share.

Recommended AI handoff order:

1. If the AI assistant can read files, provide `ai-handoff.md`.
2. If the AI assistant cannot read multiple files but can accept one uploaded file, upload `ai-context.md`.
3. If only copy and paste is available, use `ai-review-prompt.md`.

Suggested instruction:

    Please read ai-handoff.md and follow it.

## Privacy behavior

The GitHub Action follows Reviewpack's privacy-first design.

The action:

- Does not call AI providers
- Does not post PR comments by default
- Does not approve PRs
- Does not merge PRs
- Does not upload source code to external AI services
- Does not send raw diffs to AI providers
- Uploads generated Reviewpack files only as GitHub Actions artifacts by default
- Posts only a short pointer comment when comment mode is explicitly enabled

## Related examples

See:

    examples/github-action.yml
    examples/github-action-local.yml
    examples/github-action-comment.yml

## Limitations

The current GitHub Action integration does not yet support:

- Inline review comments
- GitHub Enterprise hosts
- AI provider calls
- Release publishing
- Automatic labels
- Automatic approval or merge

These may be added later as explicit opt-in features.
