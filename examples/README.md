# Examples

This directory contains example inputs and outputs for Reviewpack.

## Fixture input

The first Reviewpack milestone supports fixture-based input.

Example fixture:

    examples/fixtures/simple-pr.json

This fixture describes a synthetic pull request with:

- Authentication source changes
- Dependency file changes
- CI workflow changes
- README changes

The data is fictional and does not contain real repository secrets or private information.

## Generate a review pack

After installing Reviewpack locally, run:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

This generates:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

## What to look for

The generated review pack should identify signals such as:

- High-risk auth path changed
- Dependency files changed
- CI workflow changed
- Source files changed
- Suggested review focus areas

## Privacy note

The fixture mode does not use network access.

It does not call GitHub APIs.

It does not call AI providers.

It does not upload code, diffs, branch names, commit messages, or environment variables.
