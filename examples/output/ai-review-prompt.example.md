# AI Review Prompt

Use the context below to review this pull request.

Focus on correctness, missing tests, compatibility, security-sensitive changes, and maintainability.

Important constraints:
- Do not assume hidden code outside the provided context.
- Prefer concrete, actionable feedback.
- Avoid noisy style-only comments unless they affect correctness or maintainability.
- Treat the output as suggestions for a human maintainer to verify.

## Pull Request

Title: Add token refresh support
Author: demo-user
URL: https://github.com/octo-org/example-repo/pull/123

Metadata:
- State: open
- Draft: false
- Base branch: main
- Head branch: feature/token-refresh
- Commits: 3
- Labels: enhancement, auth

Description:
Adds token refresh support and updates related documentation.

## Changed Files

- src/auth/token.py: modified, source, +120/-20
- src/auth/refresh.py: added, source, +80/-0
- README.md: modified, docs, +16/-4
- package.json: modified, dependency, +4/-2
- .github/workflows/ci.yml: modified, ci, +6/-33

## Risk Signals

- high: High-risk area changed - This PR changes paths configured as high risk in Reviewpack configuration.
- medium: Source changed without tests - Source files changed, but no test files were detected.
- medium: Dependency files changed - Dependency changes can affect installation, compatibility, and security.
- medium: CI workflow changed - CI changes can affect required checks, automation, or release behavior.

## Suggested Review Focus

- Review behavior changes: Source files changed.
- Check test coverage: Source files changed without detected test updates.
- Check documentation accuracy: Documentation files changed.
- Review dependency impact: Dependency files changed.
- Review CI behavior: CI workflow files changed.
- Review detected risk signals: Reviewpack detected deterministic risk signals.

## Requested Review Output

Please provide:
1. A short summary of the change.
2. The top risks to review.
3. Missing or weak test coverage, if any.
4. Documentation or release-note concerns, if any.
5. Specific questions the maintainer should ask before merging.
