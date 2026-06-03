# Trusted Publishing

This document describes the intended trusted publishing setup for future Reviewpack TestPyPI and PyPI releases.

Reviewpack is not yet published to TestPyPI or PyPI.

The current goal is to document a safe, manual, and auditable publishing setup before the first package publication.

## What trusted publishing means

Trusted publishing allows a package index such as TestPyPI or PyPI to trust a specific GitHub repository and workflow.

Instead of storing a long-lived PyPI API token in GitHub secrets, the publishing workflow can use GitHub's OIDC identity to request a short-lived publishing credential.

This reduces the need for long-lived tokens.

## Why Reviewpack prefers trusted publishing

Reviewpack should prefer trusted publishing because it aligns with the project's security and privacy goals:

- No long-lived PyPI API token stored in repository secrets
- Publishing permissions are scoped to a specific repository and workflow
- Publishing happens through an explicit GitHub Actions workflow
- Publishing can be protected with GitHub environments
- Publishing remains auditable through GitHub Actions logs

## Expected workflow

Reviewpack's publishing workflow is:

    .github/workflows/publish.yml

The workflow is manually triggered through:

    workflow_dispatch

It supports:

- dry-run validation
- TestPyPI publishing
- PyPI publishing

The default `dry-run` value is true.

## Expected GitHub environments

Reviewpack expects these GitHub environments:

    testpypi
    pypi

These environments can be configured in GitHub repository settings.

Recommended environment protections:

- Required reviewers for `pypi`
- Optional required reviewers for `testpypi`
- Clear environment names matching the publish workflow
- No unnecessary secrets unless token-based publishing is used

## Expected trusted publisher configuration

For TestPyPI, the trusted publisher should be configured with values similar to:

    Repository owner: Yuanzitech
    Repository name: reviewpack
    Workflow name: publish.yml
    Environment name: testpypi

For PyPI, the trusted publisher should be configured with values similar to:

    Repository owner: Yuanzitech
    Repository name: reviewpack
    Workflow name: publish.yml
    Environment name: pypi

The exact configuration should be verified in the TestPyPI and PyPI project settings when the package project is created.

## Manual workflow inputs

The publish workflow supports two manual inputs.

### repository

Target package repository.

Supported values:

- testpypi
- pypi

### dry-run

Whether to build and validate only.

Default:

    true

When `dry-run` is true, the workflow should build and validate distributions without publishing.

When `dry-run` is false, the workflow may publish to the selected target repository.

## Recommended first-time setup sequence

Recommended order:

1. Confirm main branch CI is passing.
2. Confirm Package workflow is passing.
3. Confirm GitHub release has been created for the version.
4. Create or configure the TestPyPI project.
5. Configure TestPyPI trusted publisher for the repository and workflow.
6. Create the GitHub `testpypi` environment.
7. Run Publish workflow with `repository: testpypi` and `dry-run: true`.
8. Run Publish workflow with `repository: testpypi` and `dry-run: false`.
9. Verify installation from TestPyPI.
10. Configure PyPI trusted publisher.
11. Create the GitHub `pypi` environment.
12. Run Publish workflow with `repository: pypi` and `dry-run: true`.
13. Run Publish workflow with `repository: pypi` and `dry-run: false`.
14. Verify installation from PyPI.

## Safety notes

Do not publish to PyPI until:

- The package name is confirmed
- Version numbers are final
- TestPyPI verification passes or is intentionally skipped
- Release notes are final
- CI and Package workflows are green
- Maintainers understand that published package versions cannot be overwritten

## Token fallback

Trusted publishing is preferred.

If token-based publishing is used instead:

- Use scoped tokens when possible
- Store tokens only in GitHub Actions secrets
- Never commit tokens
- Never print tokens in logs
- Rotate tokens if exposure is suspected

## Privacy notes

Trusted publishing does not change Reviewpack runtime behavior.

It only affects how maintainers publish Reviewpack packages.

It should not introduce:

- Runtime telemetry
- AI provider calls
- Source upload behavior
- Raw diff upload behavior
- Token logging
