# TestPyPI Runbook

This runbook describes the intended manual process for publishing Reviewpack to TestPyPI and verifying the package before a real PyPI release.

Reviewpack is not yet published to TestPyPI or PyPI.

This runbook should be followed when maintainers are ready to test package publication.

## Preconditions

Before starting:

- Main branch CI is passing
- Main branch Package workflow is passing
- The target version is finalized
- `pyproject.toml` version is correct
- `reviewpack/__init__.py` version is correct
- CHANGELOG is updated
- GitHub Release exists for the target version
- Publishing workflow exists at `.github/workflows/publish.yml`
- TestPyPI trusted publishing is configured
- GitHub `testpypi` environment exists

## Step 1: Confirm version

Confirm the version is consistent.

Example for version `0.4.0`:

    GitHub tag: v0.4.0
    pyproject.toml: version = "0.4.0"
    reviewpack/__init__.py: __version__ = "0.4.0"

Package indexes do not allow overwriting an existing version.

If a version was already uploaded to TestPyPI, bump the version before uploading again.

## Step 2: Confirm TestPyPI trusted publisher

In TestPyPI, configure a trusted publisher for Reviewpack.

Expected values:

    Repository owner: Yuanzitech
    Repository name: reviewpack
    Workflow name: publish.yml
    Environment name: testpypi

The package/project name should match the intended PyPI package name.

## Step 3: Confirm GitHub environment

In GitHub repository settings, confirm the environment exists:

    testpypi

Recommended:

- Add required reviewers if desired
- Keep the environment name exactly aligned with the workflow
- Do not add secrets unless token-based publishing is used

## Step 4: Run dry-run workflow

In GitHub:

    Actions -> Publish -> Run workflow

Use:

    repository: testpypi
    dry-run: true

Expected result:

- Build succeeds
- Twine check succeeds
- Wheel inspection succeeds
- Installed wheel smoke test succeeds
- Distribution artifact is uploaded
- No package is published

If dry-run fails, fix the issue before attempting publication.

## Step 5: Publish to TestPyPI

In GitHub:

    Actions -> Publish -> Run workflow

Use:

    repository: testpypi
    dry-run: false

Expected result:

- Build succeeds
- Validation succeeds
- Distribution artifact is uploaded
- Package is published to TestPyPI

If the workflow fails with a trusted publishing error, check:

- TestPyPI trusted publisher configuration
- GitHub environment name
- Workflow name
- Repository owner and repository name
- Whether the package/project exists as expected
- Whether the version was already uploaded

## Step 6: Verify TestPyPI installation

Create a clean virtual environment:

    python -m venv .testpypi
    source .testpypi/bin/activate
    python -m pip install --upgrade pip

Install Reviewpack from TestPyPI:

    python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ reviewpack

The extra PyPI index is used so dependencies can still be resolved from PyPI.

## Step 7: Verify CLI

Run:

    reviewpack version

Then run:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack-testpypi

Expected output files:

    .reviewpack-testpypi/pr-summary.md
    .reviewpack-testpypi/risk-checklist.md
    .reviewpack-testpypi/reviewer-checklist.md
    .reviewpack-testpypi/release-note-hints.md
    .reviewpack-testpypi/ai-review-prompt.md
    .reviewpack-testpypi/reviewpack.json

Optional AI input preview verification:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack-testpypi-ai --preview-ai-input

Expected additional output:

    .reviewpack-testpypi-ai/ai-input-preview.md

## Step 8: Record verification

After successful TestPyPI verification, record:

- Package version
- TestPyPI project URL
- Workflow run URL
- Installation command used
- CLI verification result
- Any issues or warnings

This can be recorded in a GitHub issue, release checklist, or maintainer note.

## Step 9: Clean up

Deactivate the environment:

    deactivate

Remove local test output if desired:

    rm -rf .testpypi .reviewpack-testpypi .reviewpack-testpypi-ai

## Common failures

### Version already exists

Package indexes do not allow overwriting an existing version.

Fix:

- Bump version
- Rebuild
- Publish a new version

### Dependencies not found

TestPyPI does not mirror all PyPI packages.

Fix:

    --extra-index-url https://pypi.org/simple/

### Trusted publishing rejected

Check:

- Repository owner
- Repository name
- Workflow name
- Environment name
- TestPyPI trusted publisher setup
- GitHub environment setup

### CLI command missing

If `reviewpack` is not found after installation, check:

- `pyproject.toml` `[project.scripts]`
- Built wheel contents
- Installed package metadata
- Whether the correct package was installed

## Privacy notes

TestPyPI verification should not change Reviewpack runtime privacy behavior.

Reviewpack should remain:

- Local-first where possible
- AI-optional
- Maintainer-controlled
- Explicit about network access
- Careful with tokens and secrets
