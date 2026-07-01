"""Main Entrypoint."""

import argparse
import sys
from pathlib import Path

from rich import traceback

from .checks.base import Issue
from .config import load_config
from .constants import PROGRAM_NAME, PROGRAM_NAME_WITH_VERSION
from .scanner import scan
from .utils.logger import get_logger, setup_logger_cli

traceback.install(extra_lines=2)
logger = get_logger(__name__)


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=PROGRAM_NAME_WITH_VERSION)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Path to the Ansible project to scan (default: current directory).",
    )
    parser.add_argument(
        "-v",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times).",
    )
    return parser.parse_args()


def _print_issues(path: Path, issues: list[Issue]) -> None:
    print(f"{path} is in poor taste:\n")  # noqa: T201 CLI output, not logging
    for issue in issues:
        print(f"[{issue.rule_id}] {issue.message}")  # noqa: T201 CLI output, not logging
        for location in issue.locations:
            print(f"  - {location}")  # noqa: T201 CLI output, not logging


def main() -> None:
    """Main Entrypoint."""
    args = _get_args()
    setup_logger_cli(args.v)
    logger.info("%s", PROGRAM_NAME_WITH_VERSION)

    config = load_config(Path.cwd())
    issues = scan(args.path, config)

    if issues:
        _print_issues(args.path, issues)
        sys.exit(1)

    print(f"{args.path} is in good taste.")  # noqa: T201 CLI output, not logging


if __name__ == "__main__":
    main()  # pragma: no cover
