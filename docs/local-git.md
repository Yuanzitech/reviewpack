# Local Git Diff Mode

Reviewpack can generate a review context pack from a local git diff.

This mode is designed for local-first workflows. It does not require network access, GitHub API access, AI provider tokens, or external services.

## Command

    reviewpack local --base main --head HEAD --output .reviewpack

## What it does

The local mode runs:

    git diff --numstat base...head

It uses the result to collect:

- Changed file paths
- Added line counts
- Deleted line counts

Reviewpack then applies local deterministic rules to generate:

- PR summary
- Risk checklist
- AI-ready review prompt
- JSON artifact

## Example

From a local repository:

    reviewpack local --base main --head HEAD --output .reviewpack

With a custom config:

    reviewpack local --base main --head HEAD --config .reviewpack.yml --output .reviewpack

With a custom title:

    reviewpack local --base main --head HEAD --title "Feature review" --output .reviewpack

## Output

The command writes:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

## Privacy behavior

Local git diff mode:

- Does not use network access
- Does not call GitHub APIs
- Does not call AI providers
- Does not upload source code
- Does not upload raw diffs
- Does not collect environment variables
- Does not inspect terminal history
- Does not require API tokens

It only reads local git diff statistics through git diff --numstat.

## Limitations

The first local git mode only reads file paths and line counts.

It does not yet collect:

- Raw diff content
- Commit messages
- Branch names for AI context
- Related issues
- CI results
- Test coverage results

These may be added later with explicit privacy controls.
