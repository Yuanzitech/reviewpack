# Reviewpack AI Context

This file combines the most useful Reviewpack context into a single Markdown file.

Use this file when an AI assistant cannot read the full `.reviewpack/` directory.

## Review Objective

Help a human maintainer review this pull request.

Focus on:

- Correctness
- Missing or weak tests
- Compatibility
- Security-sensitive changes
- Documentation and release-note impact
- Maintainer questions before merge

## Known Limitations

- Reviewpack output is context, not ground truth.
- Do not assume hidden code or files that are not included.
- Do not claim that raw source code was inspected unless source code was provided separately.
- Treat this file as review context for a human maintainer to verify.
- Prefer concrete, actionable feedback.

## Pull Request

- Title: Add token refresh support
- Author: demo-user
- URL: https://github.com/octo-org/example-repo/pull/123

## Change Statistics

- Files changed: 5
- Lines added: 226
- Lines deleted: 59
- Source files: 2
- Test files: 0
- Documentation files: 1
- Dependency files: 1
- CI files: 1
- Config files: 0
- Infrastructure files: 0
- Unknown files: 0

## Requested AI Review Output

Please provide:

1. A short summary of the change.
2. The top risks to review.
3. Missing or weak test coverage, if any.
4. Documentation or release-note concerns, if any.
5. Specific questions the maintainer should ask before merging.

## Privacy Notes

- Reviewpack does not call an AI provider by default.
- Reviewpack does not upload raw diffs or full source code by default.
- Reviewpack does not require branch names or commit messages for this context.
- The user remains in control of what is shared with AI tools.
