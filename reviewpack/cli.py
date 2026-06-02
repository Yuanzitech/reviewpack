from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.config import load_config
from reviewpack.models import ReviewpackInput
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

    console.print("[green]Reviewpack generated successfully.[/green]")
    console.print(f"Output directory: {output}")
    console.print("")
    console.print("Generated files:")
    console.print(f"- {output / 'pr-summary.md'}")
    console.print(f"- {output / 'risk-checklist.md'}")
    console.print(f"- {output / 'ai-review-prompt.md'}")
    console.print(f"- {output / 'reviewpack.json'}")


@app.command("version")
def version() -> None:
    """Show Reviewpack version."""

    from reviewpack import __version__

    console.print(__version__)


if __name__ == "__main__":
    app()
