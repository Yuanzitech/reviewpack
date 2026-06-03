# GitHub Action

Reviewpack can run as a GitHub Action in pull request workflows.

The first GitHub Action integration generates a Reviewpack output directory and uploads it as a workflow artifact.

It does not post pull request comments.

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
            uses: Yuanzitech/reviewpack@v0.1.0
            with:
              mode: github
              pr-url: ${{ github.event.pull_request.html_url }}
              github-token: ${{ github.token }}

## Output

The action writes Reviewpack output files to:

    .reviewpack/

The output may include:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/release-note-hints.md
    .reviewpack/reviewpack.json

If AI input preview is enabled, it also writes:

    .reviewpack/ai-input-preview.md

By default, the action uploads this directory as a workflow artifact named:

    reviewpack-output

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

Example:

    pr-url: ${{ github.event.pull_request.html_url }}

### github-token

Optional GitHub token for GitHub API requests.

Recommended in GitHub Actions:

    github-token: ${{ github.token }}

Reviewpack does not store this token and does not write it to generated output files.

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

It collects:

- Pull request title
- Pull request author
- Pull request description
- Pull request URL
- Changed file paths
- Added line counts
- Deleted line counts

It does not collect raw diffs or full source code by default.

## Local mode

Local mode runs Reviewpack using local git diff statistics.

Example:

    - name: Run Reviewpack in local mode
      uses: Yuanzitech/reviewpack@v0.1.0
      with:
        mode: local
        base: main
        head: HEAD

Local mode does not require GitHub API access.

## Privacy behavior

The GitHub Action follows Reviewpack's privacy-first design.

The first action version:

- Does not call AI providers
- Does not post PR comments
- Does not approve PRs
- Does not merge PRs
- Does not upload source code to external AI services
- Does not send raw diffs to AI providers
- Uploads generated Reviewpack files only as GitHub Actions artifacts

## Permissions

Recommended workflow permissions:

    permissions:
      contents: read
      pull-requests: read

These permissions are enough for the initial metadata-focused workflow.

## Limitations

The first GitHub Action integration does not yet support:

- Posting PR comments
- Inline review comments
- GitHub Enterprise hosts
- AI provider calls
- Release publishing
- Automatic labels
- Automatic approval or merge

These may be added later as explicit opt-in features.
