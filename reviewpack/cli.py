from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from reviewpack.ai_handoff import render_handoff_terminal_text
from reviewpack.ai_preview import write_ai_input_preview
from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.config import ReviewpackConfig, load_config
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.git import collect_changed_files_from_git
from reviewpack.github_client import GitHubAPIError, collect_reviewpack_input_from_github_url
from reviewpack.models import PullRequestInfo, ReviewpackInput
from reviewpack.renderers import write_reviewpack_outputs

app = typer.Typer(
    name="reviewpack",
    help="Privacy-first context packs for AI-assisted pull request review.",
)

console = Console()


@app.command("demo")
def demo(
    output: Path = typer.Option(
        Path(".reviewpack"),
        "--output",
        "-o",
        help="Directory where Reviewpack output files will be written.",
    ),
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Optional path to a .reviewpack.yml config file.",
    ),
    preview_ai_input: bool = typer.Option(
        False,
        "--preview-ai-input",
        help="Generate a local AI input preview file without calling an AI provider.",
    ),
) -> None:
    """Generate a demo review context pack without requiring input files."""

    reviewpack_config = load_config(config)

    reviewpack_input = build_demo_reviewpack_input()
    result = analyze_reviewpack_input(reviewpack_input, reviewpack_config)
    result.metadata["mode"] = "demo"
    result.metadata["network_used"] = False
    result.metadata["ai_used"] = False

    write_reviewpack_outputs(result, output, reviewpack_config)

    if preview_ai_input:
        write_ai_input_preview(result, output)

    print_success(output, reviewpack_config, preview_ai_input=preview_ai_input)


@app.command("from-fixture")
def from_fixture(
    fixture_path: Path = typer.Argument(
        ...,
        help="Path to a Reviewpack fixture JSON file.",
    ),
    output: Path = typer.Option(
        Path(".reviewpack"),
        "--output",
        "-o",
        help="Directory where Reviewpack output files will be written.",
    ),
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Optional path to a .reviewpack.yml config file.",
    ),
    preview_ai_input: bool = typer.Option(
        False,
        "--preview-ai-input",
        help="Generate a local AI input preview file without calling an AI provider.",
    ),
) -> None:
    """Generate a review context pack from a local fixture JSON file."""

    if not fixture_path.exists():
        console.print(f"[red]Fixture file not found:[/red] {fixture_path}")
        console.print("Tip: run [bold]reviewpack demo[/bold] for a first-run example without creating files.")
        raise typer.Exit(code=1)

    raw_json = fixture_path.read_text(encoding="utf-8")
    reviewpack_input = ReviewpackInput.model_validate_json(raw_json)
    reviewpack_config = load_config(config)

    result = analyze_reviewpack_input(reviewpack_input, reviewpack_config)
    write_reviewpack_outputs(result, output, reviewpack_config)

    if preview_ai_input:
        write_ai_input_preview(result, output)

    print_success(output, reviewpack_config, preview_ai_input=preview_ai_input)


@app.command("local")
def local(
    base: str = typer.Option(
        "main",
        "--base",
        "-b",
        help="Base git ref used for local diff.",
    ),
    head: str = typer.Option(
        "HEAD",
        "--head",
        help="Head git ref used for local diff.",
    ),
    repo: Path = typer.Option(
        Path("."),
        "--repo",
        help="Path to the local git repository.",
    ),
    output: Path = typer.Option(
        Path(".reviewpack"),
        "--output",
        "-o",
        help="Directory where Reviewpack output files will be written.",
    ),
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Optional path to a .reviewpack.yml config file.",
    ),
    title: str = typer.Option(
        "Local git diff",
        "--title",
        help="Title used in the generated review pack.",
    ),
    author: str = typer.Option(
        "local",
        "--author",
        help="Author label used in the generated review pack.",
    ),
    preview_ai_input: bool = typer.Option(
        False,
        "--preview-ai-input",
        help="Generate a local AI input preview file without calling an AI provider.",
    ),
) -> None:
    """Generate a review context pack from a local git diff."""

    reviewpack_config = load_config(config)

    try:
        changed_files = collect_changed_files_from_git(
            base=base,
            head=head,
            repo_path=repo,
        )
    except RuntimeError as error:
        console.print(f"[red]Failed to collect local git diff:[/red] {error}")
        raise typer.Exit(code=1) from error

    reviewpack_input = ReviewpackInput(
        pr=PullRequestInfo(
            title=title,
            author=author,
        ),
        changed_files=changed_files,
    )

    result = analyze_reviewpack_input(reviewpack_input, reviewpack_config)
    result.metadata["mode"] = "local_git"
    result.metadata["network_used"] = False
    result.metadata["ai_used"] = False

    write_reviewpack_outputs(result, output, reviewpack_config)

    if preview_ai_input:
        write_ai_input_preview(result, output)

    print_success(output, reviewpack_config, preview_ai_input=preview_ai_input)


@app.command("github")
def github(
    pr_url: str = typer.Argument(
        ...,
        help="GitHub pull request URL.",
    ),
    output: Path = typer.Option(
        Path(".reviewpack"),
        "--output",
        "-o",
        help="Directory where Reviewpack output files will be written.",
    ),
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Optional path to a .reviewpack.yml config file.",
    ),
    token: str | None = typer.Option(
        None,
        "--token",
        help="Optional GitHub token. Prefer REVIEWPACK_GITHUB_TOKEN for local use.",
    ),
    preview_ai_input: bool = typer.Option(
        False,
        "--preview-ai-input",
        help="Generate a local AI input preview file without calling an AI provider.",
    ),
) -> None:
    """Generate a review context pack from GitHub PR metadata."""

    reviewpack_config = load_config(config)

    try:
        reviewpack_input = collect_reviewpack_input_from_github_url(pr_url, token=token)
    except (ValueError, GitHubAPIError) as error:
        console.print(f"[red]Failed to collect GitHub pull request data:[/red] {error}")
        raise typer.Exit(code=1) from error

    result = analyze_reviewpack_input(reviewpack_input, reviewpack_config)
    result.metadata["mode"] = "github"
    result.metadata["network_used"] = True
    result.metadata["ai_used"] = False

    write_reviewpack_outputs(result, output, reviewpack_config)

    if preview_ai_input:
        write_ai_input_preview(result, output)

    print_success(output, reviewpack_config, preview_ai_input=preview_ai_input)


@app.command("handoff")
def handoff(
    output: Path = typer.Option(
        Path(".reviewpack"),
        "--output",
        "-o",
        help="Reviewpack output directory.",
    ),
) -> None:
    """Show a short AI handoff instruction for generated Reviewpack files."""

    handoff_file = output / "ai-handoff.md"

    if not handoff_file.exists():
        console.print(f"[yellow]AI handoff file not found:[/yellow] {handoff_file}")
        console.print(
            "Tip: run [bold]reviewpack demo[/bold], "
            "[bold]reviewpack local[/bold], or "
            "[bold]reviewpack github PR_URL[/bold] first."
        )
        console.print("")

    console.print(render_handoff_terminal_text(output))


@app.command("guide")
def guide() -> None:
    """Show a short product guide for common Reviewpack workflows."""

    console.print(render_guide_text())


@app.command("version")
def version() -> None:
    """Show Reviewpack version."""

    from reviewpack import __version__

    console.print(__version__)


def render_guide_text() -> str:
    """Render a short product-oriented command guide."""

    return "\n".join(
        [
            "Reviewpack quick guide",
            "",
            "New here?",
            "  reviewpack demo",
            "",
            "Have a GitHub PR?",
            "  reviewpack github https://github.com/owner/repo/pull/123",
            "",
            "Working locally before opening a PR?",
            "  reviewpack local",
            "",
            "Have a fixture JSON?",
            "  reviewpack from-fixture simple-pr.json",
            "",
            "Want AI assistance?",
            "  1. Run any Reviewpack command.",
            "  2. If your AI assistant can read files, ask:",
            '     "Please read .reviewpack/ai-handoff.md and follow it."',
            "  3. If your AI assistant cannot read local files, upload:",
            "     .reviewpack/ai-context.md",
            "  4. If only copy and paste is available, use:",
            "     .reviewpack/ai-review-prompt.md",
            "",
            "Default output:",
            "  Reviewpack writes files to .reviewpack/ by default.",
            "",
            "Configuration:",
            "  Reviewpack loads .reviewpack.yml by default when present.",
            "  Use --config PATH to select a custom config file.",
            "",
            "Useful files:",
            "  .reviewpack/pr-summary.md",
            "  .reviewpack/risk-checklist.md",
            "  .reviewpack/reviewer-checklist.md",
            "  .reviewpack/release-note-hints.md",
            "  .reviewpack/ai-handoff.md",
            "  .reviewpack/ai-context.md",
            "  .reviewpack/ai-review-prompt.md",
            "",
            "For CLI options:",
            "  reviewpack --help",
            "  reviewpack demo --help",
            "  reviewpack github --help",
            "",
        ]
    )


def print_success(
    output: Path,
    config: ReviewpackConfig,
    preview_ai_input: bool = False,
) -> None:
    """Print generated output paths."""

    console.print("[green]Reviewpack generated successfully.[/green]")
    console.print(f"Output directory: {output}")
    console.print("")
    console.print("Generated files:")

    if config.outputs.pr_summary:
        console.print(f"- {output / 'pr-summary.md'}")
    if config.outputs.risk_checklist:
        console.print(f"- {output / 'risk-checklist.md'}")
    if config.outputs.reviewer_checklist:
        console.print(f"- {output / 'reviewer-checklist.md'}")
    if config.outputs.release_note_hints:
        console.print(f"- {output / 'release-note-hints.md'}")
    if config.outputs.ai_review_prompt:
        console.print(f"- {output / 'ai-review-prompt.md'}")
    if config.outputs.ai_handoff:
        console.print(f"- {output / 'ai-handoff.md'}")
    if config.outputs.ai_context:
        console.print(f"- {output / 'ai-context.md'}")
    if config.outputs.json_output:
        console.print(f"- {output / 'reviewpack.json'}")

    if preview_ai_input:
        console.print(f"- {output / 'ai-input-preview.md'}")

    console.print("")
    console.print("Next:")

    if config.outputs.ai_handoff:
        console.print(f'- Ask your AI assistant: "Please read {output / "ai-handoff.md"} and follow it."')
    if config.outputs.ai_context:
        console.print(f"- If files cannot be read, upload: {output / 'ai-context.md'}")

    console.print(f"- Or run: reviewpack handoff --output {output}")


if __name__ == "__main__":
    app()
