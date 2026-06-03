# PyPI Publishing Notes

This document tracks the planned PyPI publishing process for Reviewpack.

Reviewpack is not yet published to PyPI.

The current goal is packaging readiness: make sure the package can be built, inspected, and prepared for a future PyPI release.

## Current status

Reviewpack already has:

- `pyproject.toml`
- Hatchling build backend
- Console script entry point
- Project metadata
- GitHub release tags
- CI tests
- Package build workflow

Reviewpack does not yet have:

- PyPI project publication
- PyPI trusted publishing
- PyPI release workflow
- `pip install reviewpack` availability

## Build package locally

Install build tooling:

    python -m pip install --upgrade pip
    python -m pip install build twine

Build distributions:

    python -m build

This should create:

    dist/*.tar.gz
    dist/*.whl

## Check package metadata

Run:

    python -m twine check dist/*

The check should pass before uploading to PyPI.

## Inspect wheel contents

A Reviewpack wheel should mainly contain:

    reviewpack/
    reviewpack-*.dist-info/

It should not need to include:

    docs/
    tests/
    .github/
    examples/
    issue templates

Those files are useful in the GitHub repository, but they are not required at runtime for the installed CLI.

## Version consistency

Before publishing, confirm that these versions match:

- GitHub tag
- `pyproject.toml`
- `reviewpack/__init__.py`
- GitHub release title

Example:

    GitHub tag: v0.3.0
    pyproject.toml: version = "0.3.0"
    reviewpack/__init__.py: __version__ = "0.3.0"

## Token handling

If using a PyPI API token:

- Do not commit it
- Do not print it in logs
- Store it only in GitHub Actions secrets if needed
- Prefer PyPI trusted publishing when possible

## Recommended future publishing flow

A future publishing workflow may use:

- GitHub release tags
- GitHub Actions
- PyPI trusted publishing
- Manual approval for releases

Suggested release flow:

1. Prepare release PR
2. Update version numbers
3. Update CHANGELOG
4. Merge after CI passes
5. Create GitHub release tag
6. Build package
7. Publish to PyPI through trusted publishing

## Non-goals for current packaging readiness

This packaging readiness step does not:

- Publish to PyPI
- Add AI provider integration
- Change Reviewpack runtime behavior
- Change GitHub Action behavior
- Add automatic release publishing

## Privacy notes

Publishing Reviewpack to PyPI should not change Reviewpack's privacy model.

Reviewpack should continue to be:

- Local-first where possible
- AI-optional
- Maintainer-controlled
- Explicit about network access
- Careful with tokens and secrets
