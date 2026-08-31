"""Check that every task name is unique across the whole project."""

import re
from collections import defaultdict
from pathlib import Path

import yaml
from rich.markup import escape

from ansible_taste.console import console

from .base import Issue

RULE_ID = "unique-step-names"

_JINJA_PATTERN = re.compile(r"{{.*}}")


def run(files: list[Path]) -> list[Issue]:
    """Flag task names that appear more than once.

    Jinja-templated names (containing ``{{ ... }}``) are only compared
    within the same file, since the same template can legitimately repeat
    across files with different variable values.
    """
    name_locations: dict[str, list[str]] = defaultdict(list)
    jinja_name_locations: dict[tuple[Path, str], list[str]] = defaultdict(list)

    for file in files:
        for name, line in _load_task_names(file):
            location = f"{file}:{line}"
            if _JINJA_PATTERN.search(name):
                jinja_name_locations[(file, name)].append(location)
            else:
                name_locations[name].append(location)

    issues = [
        Issue(rule_id=RULE_ID, message=f"Duplicate task name: {name!r}", locations=locations)
        for name, locations in name_locations.items()
        if len(locations) > 1
    ]
    issues += [
        Issue(rule_id=RULE_ID, message=f"Duplicate task name: {name!r}", locations=locations)
        for (_file, name), locations in jinja_name_locations.items()
        if len(locations) > 1
    ]
    return issues


def _load_task_names(file: Path) -> list[tuple[str, int]]:
    try:
        root = yaml.compose(file.read_text())
    except yaml.YAMLError:
        console.print(f"[yellow]Skipping {escape(str(file))}, not valid YAML[/yellow]")
        return []

    if not isinstance(root, yaml.SequenceNode):
        return []

    names = []
    for task_node in root.value:
        if not isinstance(task_node, yaml.MappingNode):
            continue
        for key_node, value_node in task_node.value:
            if key_node.value == "name" and isinstance(value_node, yaml.ScalarNode):
                names.append((value_node.value, value_node.start_mark.line + 1))

    return names
