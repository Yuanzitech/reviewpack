# v1.0 Readiness

This document tracks what Reviewpack should stabilize before a v1.0 release.

Reviewpack is currently a PyPI-published early product.

The project is useful today, but v1.0 should represent a stronger compatibility commitment.

## Current maturity

Reviewpack currently supports:

- PyPI installation
- CLI workflows
- GitHub Action workflows
- Demo mode
- Local git diff mode
- GitHub PR metadata mode
- Fixture input
- Configurable rules and outputs
- Structured Markdown artifacts
- Machine-readable JSON output
- AI handoff files
- Optional short PR comment mode
- CI, package, publish, TestPyPI, and PyPI verification workflows

## v1.0 goal

A v1.0 release should mean:

    Reviewpack's core CLI, GitHub Action inputs, output artifact names, configuration schema, JSON output expectations, and privacy model are stable enough for external users and integrations.

## Readiness checklist

### CLI stability

- [ ] Command names are stable
- [ ] Core command options are stable
- [ ] Error messages are clear enough for common failures
- [ ] First-run workflow is stable
- [ ] Local mode behavior is documented
- [ ] GitHub mode behavior is documented
- [ ] Fixture mode behavior is documented
- [ ] Configuration loading behavior is documented

Important commands:

    reviewpack demo
    reviewpack github
    reviewpack local
    reviewpack from-fixture
    reviewpack handoff
    reviewpack guide
    reviewpack version

### Artifact stability

- [ ] Default output directory is stable
- [ ] Output file names are stable
- [ ] Markdown artifact purposes are documented
- [ ] Artifact reading order is documented
- [ ] AI handoff behavior is documented
- [ ] Optional AI input preview behavior is documented
- [ ] Artifact compatibility expectations are documented

Important files:

    pr-summary.md
    risk-checklist.md
    reviewer-checklist.md
    release-note-hints.md
    ai-review-prompt.md
    ai-handoff.md
    ai-context.md
    reviewpack.json

### JSON output stability

- [ ] Top-level JSON fields are documented
- [ ] Pull request metadata fields are documented
- [ ] Changed file fields are documented
- [ ] Stats fields are documented
- [ ] Risk signal fields are documented
- [ ] Review focus fields are documented
- [ ] Metadata fields are documented
- [ ] JSON schema versioning is considered
- [ ] Backward compatibility expectations are documented

### Configuration stability

- [ ] `.reviewpack.yml` schema is documented
- [ ] Public keys are stable
- [ ] Defaults are documented
- [ ] Validation behavior is documented
- [ ] Invalid config behavior is documented
- [ ] Example configs are available
- [ ] Backward compatibility expectations are documented

Current top-level config sections:

    outputs
    risk
    paths

### GitHub Action stability

- [ ] GitHub Action inputs are documented
- [ ] Artifact upload behavior is stable
- [ ] Optional comment mode behavior is documented
- [ ] Required permissions are documented
- [ ] Fork PR limitations are documented
- [ ] Local mode Action behavior is documented
- [ ] GitHub mode Action behavior is documented
- [ ] Failure modes are documented

Important inputs:

    mode
    pr-url
    base
    head
    output
    preview-ai-input
    upload-artifact
    artifact-name
    github-token
    comment

### Privacy model stability

- [ ] No AI calls by default is documented
- [ ] No raw diff collection by default is documented
- [ ] No full source code upload by default is documented
- [ ] Token handling is documented
- [ ] GitHub metadata collection boundaries are documented
- [ ] AI handoff behavior is documented
- [ ] Optional PR comment behavior is documented

### Release process stability

- [ ] CI workflow is stable
- [ ] Package workflow is stable
- [ ] Publish workflow is stable
- [ ] TestPyPI verification workflow is stable
- [ ] PyPI verification workflow is stable
- [ ] Release checklist is updated
- [ ] Version bump process is documented
- [ ] Release notes process is documented

### Documentation completeness

- [ ] README is clear for first-time users
- [ ] Simplified Chinese README is synchronized for major features
- [ ] Installation guide is current
- [ ] Commands guide is current
- [ ] GitHub guide is current
- [ ] GitHub Action guide is current
- [ ] Configuration guide is current
- [ ] Artifact contract is documented
- [ ] JSON output is documented
- [ ] Roadmap is current
- [ ] Privacy model is current

## Before v1.0

Before v1.0, Reviewpack should avoid making compatibility promises that are too strong.

Recommended language:

    pre-1.0 artifact contract
    current schema expectations
    subject to refinement before v1.0
    stable where possible

Avoid promising:

    permanent schema stability
    no breaking changes
    complete API stability

## Potential v0.7 focus

The v0.7 series should focus on stabilization:

- configuration schema refinement
- artifact contract refinement
- JSON output documentation
- GitHub Action validation
- fork PR behavior documentation
- comment mode failure handling
- integration examples

## Potential v0.8 focus

The v0.8 series may focus on validation and integration hardening:

- broader GitHub Action testing
- optional GitHub Enterprise host design
- more configuration examples
- more JSON integration examples
- stronger release checklist

## Potential v0.9 focus

The v0.9 series should prepare for v1.0:

- freeze core CLI surface
- freeze artifact names
- freeze key GitHub Action inputs
- define compatibility policy
- define deprecation policy
- define migration policy
- finalize v1.0 release criteria

## Not required for v1.0

These are not required for v1.0:

- direct AI provider integration
- SaaS backend
- IDE plugin
- MCP server
- raw diff collection by default
- automatic approval
- automatic merge
- noisy PR comments by default

Reviewpack can be a strong v1.0 product without these features.
