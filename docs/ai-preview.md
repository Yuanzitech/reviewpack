# AI Input Preview

Reviewpack can generate a local AI input preview file.

This feature does not call an AI provider.

It only writes a local Markdown file showing the type of context that may be sent to an AI provider if AI mode is explicitly enabled in a future version.

## Command

From fixture input:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack --preview-ai-input

From local git diff:

    reviewpack local --base main --head HEAD --output .reviewpack --preview-ai-input

## Output

The command writes:

    .reviewpack/ai-input-preview.md

## Why this exists

AI-assisted review can be useful, but maintainers should know what context is being prepared before anything is sent to an AI provider.

The AI input preview helps users inspect:

- Pull request title
- Pull request description
- Changed file paths
- Change statistics
- Risk signals
- Suggested review focus

## What is excluded by default

The preview documents that Reviewpack excludes the following by default:

- Raw diffs
- Full source code
- Branch names
- Commit messages
- Environment variables
- Terminal history
- Git remote URLs
- API tokens

## Secret redaction

Reviewpack includes a best-effort secret redaction helper for preview text.

It can redact common secret-like patterns such as:

- api_key values
- token values
- password values
- secret values
- Authorization Bearer tokens
- GitHub token-like values
- OpenAI key-like values

This is not a complete secret scanner.

Reviewpack should still avoid collecting sensitive content by default.

## Privacy behavior

AI input preview mode:

- Does not use network access
- Does not call GitHub APIs
- Does not call AI providers
- Does not upload source code
- Does not upload raw diffs
- Does not require API tokens

It is a local inspection tool for maintainers.
