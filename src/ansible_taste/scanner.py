"""Wire discovery and checks together."""

from pathlib import Path

from .checks import ALL_CHECKS
from .checks.base import Issue
from .config import Config
from .discovery import find_task_files


def scan(root: Path, config: Config) -> list[Issue]:
    """Find task files under root and run every non-skipped check over them."""
    files = find_task_files(root, config.exclude_paths)

    issues: list[Issue] = []
    for check in ALL_CHECKS:
        if check.rule_id not in config.skip_list:
            issues.extend(check.run(files))

    return issues
