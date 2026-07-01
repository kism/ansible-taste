"""Check that every task name is unique across the whole project."""

from collections import defaultdict
from pathlib import Path

import yaml

from ansible_taste.utils.logger import get_logger

from .base import Issue

RULE_ID = "unique-step-names"

logger = get_logger(__name__)


def run(files: list[Path]) -> list[Issue]:
    """Flag task names that appear more than once across all files."""
    name_locations: dict[str, list[str]] = defaultdict(list)

    for file in files:
        for task in _load_tasks(file):
            name = task.get("name") if isinstance(task, dict) else None
            if isinstance(name, str):
                name_locations[name].append(str(file))

    return [
        Issue(rule_id=RULE_ID, message=f"Duplicate task name: {name!r}", locations=locations)
        for name, locations in name_locations.items()
        if len(locations) > 1
    ]


def _load_tasks(file: Path) -> list[object]:
    try:
        tasks = yaml.safe_load(file.read_text())
    except yaml.YAMLError:
        logger.warning("Skipping %s, not valid YAML", file)
        return []

    return tasks if isinstance(tasks, list) else []
