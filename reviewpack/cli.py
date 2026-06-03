from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from reviewpack.ai_preview import write_ai_input_preview
from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.config import load_config
from reviewpack.git import collect_changed_files_from_git
from reviewpack.models import PullRequestInfo, ReviewpackInput
from reviewpack.renderers import write_reviewpack_outputs

app = typer.Typer(
    name="reviewpack",
    help="Privacy-first context packs for AI-assisted pull request review.",
)

console = Console()


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
        raise typer.Exit(code=1)

    raw_json = fixture_path.read_text(encoding="utf-8")
    reviewpack_input = ReviewpackInput.model_validate_json(raw_json)
    reviewpack_config = load_config(config)

    result = analyze_reviewpack_input(reviewpack_input, reviewpack_config)
    write_reviewpack_outputs(result, output)

    if preview_ai_input:
        write_ai_input_preview(result, output)

    print_success(output, preview_ai_input=preview_ai_input)


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

    write_reviewpack_outputs(result, output)

    if preview_ai_input:
        write_ai_input_preview(result, output)

    print_success(output, preview_ai_input=preview_ai_input)


@app.command("version")
def version() -> None:
    """Show Reviewpack version."""

    from reviewpack import __version__

    console.print(__version__)


def print_success(output: Path, preview_ai_input: bool = False) -> None:
    """Print generated output paths."""

    console.print("[green]Reviewpack generated successfully.[/green]")
    console.print(f"Output directory: {output}")
    console.print("")
    console.print("Generated files:")
    console.print(f"- {output / 'pr-summary.md'}")
    console.print(f"- {output / 'risk-checklist.md'}")
    console.print(f"- {output / 'ai-review-prompt.md'}")
    console.print(f"- {output / 'reviewpack.json'}")

    if preview_ai_input:
        console.print(f"- {output / 'ai-input-preview.md'}")


if __name__ == "__main__":
    app()
