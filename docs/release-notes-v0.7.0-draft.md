# Reviewpack v0.7.0

Reviewpack v0.7.0 is a stabilization foundation release.

This release focuses on making Reviewpack's user-facing contracts clearer, better documented, and better protected by tests.

It does not add AI provider integration.

It does not enable raw diff collection by default.

It does not enable PR comments by default.

## Highlights

### Artifact contract documentation and validation

Reviewpack now documents its current pre-1.0 artifact contract.

New and updated docs include:

    docs/artifact-contract.md
    docs/output-artifacts.md

The artifact contract documents current expectations for:

    .reviewpack/
    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md
    ai-review-prompt.md
    ai-handoff.md
    ai-context.md
    ai-input-preview.md
    reviewpack.json

This release also adds contract tests for output artifact generation, default output files, configurable output files, and artifact documentation links.

### Configuration schema documentation and examples

Reviewpack now has clearer documentation for `.reviewpack.yml`.

New and updated docs include:

    docs/config-schema.md
    docs/configuration.md

This release adds practical configuration examples:

    examples/config/minimal.reviewpack.yml
    examples/config/python-project.reviewpack.yml
    examples/config/javascript-typescript-project.reviewpack.yml
    examples/config/monorepo.reviewpack.yml

These examples help users adapt Reviewpack to common repository types.

The public JSON output configuration key remains:

    outputs:
      json: true

Internally, Reviewpack still maps this to:

    json_output

Users should normally keep using the public `json` key.

### JSON schema draft and integration guidance

Reviewpack now includes a draft pre-1.0 JSON schema for `reviewpack.json`:

    schemas/reviewpack-result.schema.json

The schema documents the current shape of:

    pr
    changed_files
    stats
    risk_signals
    review_focus
    metadata

This release also adds JSON integration guidance:

    docs/integration-json.md

The guide recommends that integration authors:

- pin Reviewpack versions for production integrations
- treat unknown fields as allowed
- treat optional fields as optional
- prefer `reviewpack.json` over parsing Markdown artifacts
- avoid depending on exact Markdown wording
- treat risk signals as deterministic review signals, not security guarantees

### GitHub Action contract validation

Reviewpack's GitHub Action is now better protected by contract tests.

This release adds tests for:

- Action input names
- Action default values
- opt-in comment mode
- artifact upload behavior
- hidden artifact upload support
- GitHub mode and local mode command paths
- next-step guidance
- example workflows
- comment mode permissions
- fork pull request limitation documentation

The GitHub Action still does not post PR comments by default.

Optional PR comment mode still requires:

    comment: "true"

### Output examples alignment

Reviewpack now includes a more complete set of example output artifacts under:

    examples/output/

New example files include:

    examples/output/README.md
    examples/output/pr-summary.example.md
    examples/output/ai-review-prompt.example.md
    examples/output/reviewpack.example.json

Existing example files remain available:

    examples/output/risk-checklist.example.md
    examples/output/reviewer-checklist.example.md
    examples/output/release-note-hints.example.md
    examples/output/ai-handoff.example.md
    examples/output/ai-context.example.md

These examples help users understand generated artifacts before running Reviewpack.

### v1.0 readiness planning

Reviewpack now includes a v1.0 readiness checklist:

    docs/v1-readiness.md

The checklist tracks stabilization areas such as:

- CLI stability
- artifact stability
- JSON output stability
- configuration stability
- GitHub Action stability
- privacy model stability
- release process stability
- documentation completeness

This release does not make Reviewpack a stable 1.0 product.

Instead, it lays the foundation for moving toward a future stable contract.

## What's changed since v0.6.1

### Added

- Artifact contract documentation
- Configuration schema documentation
- JSON output documentation
- JSON integration guidance
- Draft JSON schema for `reviewpack.json`
- v1.0 readiness checklist
- Contract tests for output artifacts
- Contract tests for configuration schema keys
- Contract tests for JSON output structure
- Contract tests for documentation links
- GitHub Action contract tests
- GitHub Action example workflow tests
- Practical `.reviewpack.yml` examples
- Invalid configuration guidance
- Output example README
- PR summary output example
- AI review prompt output example
- JSON output example

### Changed

- Configuration documentation now includes practical examples
- Configuration schema docs now explain invalid configuration behavior
- Output artifacts documentation now references example outputs
- Artifact contract documentation now references example outputs
- JSON integration guide now clarifies pre-1.0 schema expectations
- GitHub Action docs now include stronger troubleshooting and permission guidance
- Documentation link tests now cover schema files, config examples, and output examples
- TestPyPI install verification default updated to 0.7.0
- PyPI install verification default updated to 0.7.0

### Fixed

- Nothing.

## Compatibility notes

This release does not intentionally change runtime behavior.

This release does not change output file names.

This release does not change the public `.reviewpack.yml` key:

    outputs:
      json: true

This release does not change the default privacy model.

The draft JSON schema is pre-1.0 and should not be treated as a final compatibility guarantee.

## Privacy notes

Reviewpack v0.7.0 keeps the privacy-first defaults.

Reviewpack still does not:

- call AI providers by default
- collect raw diffs by default
- upload full source code by default
- post PR comments by default
- approve pull requests
- merge pull requests

Optional PR comment mode remains explicitly opt-in.

## Upgrade

Install or upgrade from PyPI:

    pip install --upgrade reviewpack

Verify:

    reviewpack version
    reviewpack demo
    reviewpack handoff
    reviewpack guide

For GitHub Action users, update workflow references after the GitHub release is published:

    uses: Yuanzitech/reviewpack@v0.7.0

## Suggested validation

After installation, verify the package with:

    python -W error::UserWarning -c "import reviewpack.config"
    reviewpack version
    reviewpack demo --output .reviewpack-070
    reviewpack handoff --output .reviewpack-070
    reviewpack guide

Expected generated files include:

    .reviewpack-070/pr-summary.md
    .reviewpack-070/risk-checklist.md
    .reviewpack-070/reviewer-checklist.md
    .reviewpack-070/release-note-hints.md
    .reviewpack-070/ai-review-prompt.md
    .reviewpack-070/ai-handoff.md
    .reviewpack-070/ai-context.md
    .reviewpack-070/reviewpack.json

## Next steps

After v0.7.0, the next recommended milestone is:

    v0.8.0 GitHub Workflow Hardening

Potential focus areas include:

- fork pull request behavior
- pull request trigger safety guidance
- comment mode failure behavior
- private repository examples
- monorepo workflow examples
- GitHub Enterprise host design
