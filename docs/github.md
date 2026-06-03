# GitHub Pull Request Support

Reviewpack is preparing support for GitHub pull request workflows.

The first GitHub-related milestone only parses GitHub pull request URLs. It does not call the GitHub API, does not require tokens, and does not use network access.

## Supported URL format

Reviewpack supports GitHub pull request URLs in this format:

    https://github.com/owner/repo/pull/123

The parser extracts:

- Owner
- Repository name
- Pull request number
- Original URL

## Current behavior

The current GitHub URL parser:

- Does not use network access
- Does not call GitHub APIs
- Does not require a GitHub token
- Does not read repository secrets
- Does not inspect local git configuration
- Does not upload source code or diffs

It only parses the URL string explicitly provided by the user.

## Why this exists

GitHub support will be implemented in small steps.

The URL parser is the foundation for future commands such as:

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

Future versions may use GitHub API data to collect:

- Pull request title
- Pull request description
- Changed files
- Additions and deletions
- Labels
- Linked issues
- Review metadata

## Token policy

Future GitHub API support should follow these rules:

- Public repository metadata should work without a token where possible
- Private repositories require explicit user-provided tokens
- Tokens should never be stored by Reviewpack
- Tokens should not be printed in logs
- Tokens should not be included in generated review packs
- Token usage should be documented clearly

## Privacy behavior

Future GitHub integration should remain privacy-first.

By default, Reviewpack should avoid collecting or sending:

- Raw source code
- Raw diffs
- Branch names
- Commit messages
- Environment variables
- Git remote URLs
- Repository secrets
- API tokens

When additional context is needed, it should be opt-in and visible to maintainers.

## Planned command

A future GitHub command may look like this:

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

With optional AI input preview:

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack --preview-ai-input

This future command should still avoid AI calls unless the user explicitly enables AI provider integration.
