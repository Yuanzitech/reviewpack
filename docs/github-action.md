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
            uses: Yuanzitech/reviewpack@v0.5.0
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
            uses: Yuanzitech/reviewpack@v0.5.0
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

## Permissions for comment mode

Artifact-only mode can use:

    permissions:
      contents: read
      pull-requests: read

Comment mode requires:

    permissions:
      contents: read
      pull-requests: write

For pull requests from forks, GitHub may restrict write permissions.

If comment mode cannot write a comment, artifact generation can still be used without comment mode.

## Inputs

### mode

Reviewpack mode.

Supported values:

- github
- local

Default:

    github

### pr-url

GitHub pull request URL.

Required when mode is github.

Required when comment mode is enabled.

Example:

    pr-url: ${{ github.event.pull_request.html_url }}

### github-token

Optional GitHub token for GitHub API requests.

Required when comment mode is enabled.

Recommended in GitHub Actions:

    github-token: ${{ github.token }}

Reviewpack does not store this token and does not write it to generated output files.

### comment

Post or update a short Reviewpack summary comment on the pull request.

Default:

    false

Example:

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

Example:

    preview-ai-input: "true"

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

Example:

    - name: Run Reviewpack
      uses: Yuanzitech/reviewpack@v0.5.0
      with:
        mode: github
        pr-url: ${{ github.event.pull_request.html_url }}
        github-token: ${{ github.token }}

## Local mode

Local mode runs Reviewpack using local git diff statistics.

Example:

    - name: Run Reviewpack in local mode
      uses: Yuanzitech/reviewpack@v0.5.0
      with:
        mode: local
        base: main
        head: HEAD

Local mode does not require GitHub API access.

For pull request workflows, local mode depends on the checkout depth and available refs. If local mode cannot find the base ref, adjust the checkout step.

Example checkout for local mode:

    - name: Check out repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

## Token behavior

### Public repositories

For public pull requests, GitHub metadata mode usually works with:

    github-token: ${{ github.token }}

No separate personal access token is normally required.

### Private repositories

For private repositories, use:

    github-token: ${{ github.token }}

Recommended permissions for artifact-only mode:

    permissions:
      contents: read
      pull-requests: read

Recommended permissions for comment mode:

    permissions:
      contents: read
      pull-requests: write

### Local CLI usage

For local CLI usage, prefer the environment variable:

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123

Avoid putting long-lived tokens directly in command history when possible.

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

## Limitations

The current GitHub Action integration does not yet support:

- Inline review comments
- GitHub Enterprise hosts
- AI provider calls
- Release publishing
- Automatic labels
- Automatic approval or merge

These may be added later as explicit opt-in features.
