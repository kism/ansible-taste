"""Main Entrypoint."""

import argparse
import sys
from pathlib import Path

from rich import traceback
from rich.markup import escape

from .checks.base import Issue
from .config import load_config
from .console import console
from .constants import PROGRAM_NAME, PROGRAM_NAME_WITH_VERSION
from .scanner import scan

traceback.install(extra_lines=2)


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=PROGRAM_NAME_WITH_VERSION)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Path to the Ansible project to scan (default: current directory).",
    )
    return parser.parse_args()


def _print_issues(path: Path, issues: list[Issue]) -> None:
    console.print(f"[bold red]{escape(str(path))} is in poor taste:[/bold red]\n")
    for issue in issues:
        console.print(f"[yellow]{escape(f'[{issue.rule_id}]')}[/yellow] {escape(issue.message)}")
        for location in issue.locations:
            console.print(f"  - [dim]{escape(location)}[/dim]")
    console.print(f"\n[bold red]{len(issues)} issue(s) found.[/bold red]")


def main() -> None:
    """Main Entrypoint."""
    args = _get_args()

    config = load_config(Path.cwd())
    issues = scan(args.path, config)

    if issues:
        _print_issues(args.path, issues)
        sys.exit(1)

    console.print(f"[green]{escape(str(args.path))} is in good taste.[/green]")


if __name__ == "__main__":
    main()  # pragma: no cover
