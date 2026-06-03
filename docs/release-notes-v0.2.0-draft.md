# Reviewpack v0.2.0

Reviewpack v0.2.0 adds maintainer workflow artifacts and the first GitHub Action integration.

This release builds on the v0.1.0 public milestone by making Reviewpack more useful in real pull request review workflows.

## Highlights

### Reviewer checklist output

Reviewpack now generates:

    .reviewpack/reviewer-checklist.md

The reviewer checklist turns Reviewpack analysis into concrete maintainer review steps.

It may include sections such as:

- Core Review
- Compatibility
- Tests
- Documentation
- Dependencies
- CI
- Infrastructure
- Risk
- Release
- Privacy

This helps maintainers review pull requests more consistently without relying on AI.

### Release note hints output

Reviewpack now generates:

    .reviewpack/release-note-hints.md

Release note hints help maintainers decide whether a pull request should be mentioned in release notes or changelogs.

The hints are deterministic and generated from Reviewpack analysis results.

They do not call AI providers and do not generate final release notes automatically.

### GitHub Action integration

Reviewpack now includes a first GitHub Action integration through:

    action.yml

Example workflow:

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
            uses: Yuanzitech/reviewpack@v0.2.0
            with:
              mode: github
              pr-url: ${{ github.event.pull_request.html_url }}
              github-token: ${{ github.token }}

The action generates `.reviewpack/` output inside the workflow and uploads it as a GitHub Actions artifact.

The first action integration does not post PR comments and does not call AI providers.

### Expanded review pack outputs

Reviewpack can now generate:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-input-preview.md
    .reviewpack/reviewpack.json

This makes Reviewpack more useful as a maintainer workflow tool.

## What's changed since v0.1.0

### Added

- Reviewer checklist output
- Release note hints output
- GitHub Action metadata
- GitHub Action usage guide
- GitHub Action workflow example
- Tests for reviewer checklist generation
- Tests for release note hints generation
- Tests for GitHub Action metadata

### Changed

- Package version bumped to 0.2.0
- CLI version bumped to 0.2.0
- README now documents GitHub Action usage
- README now documents reviewer checklist output
- README now documents release note hints output
- CLI output now lists reviewer checklist and release note hints files
- Reviewpack output now includes reviewer checklist and release note hints by default

## Privacy notes

Reviewpack v0.2.0 continues the privacy-first design.

The new reviewer checklist and release note hints are generated locally from Reviewpack analysis results.

They do not require:

- AI provider calls
- Raw diffs
- Full source code
- Branch names
- Commit messages

The GitHub Action integration:

- Does not call AI providers
- Does not post PR comments
- Does not approve pull requests
- Does not merge pull requests
- Uploads generated Reviewpack files as GitHub Actions artifacts

## Known limitations

This release does not yet include:

- PyPI publishing
- `pip install reviewpack`
- Optional PR comments
- AI provider integration
- Local AI provider integration
- Linked issue collection
- CI status collection
- Raw diff analysis

## Next steps

Planned next steps include:

- PyPI packaging readiness
- Installation documentation
- Better GitHub Action ergonomics
- Optional PR comment mode
- Stronger configuration support
- Optional AI provider interface
