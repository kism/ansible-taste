"""Check for redundant `become_user: root`, which is already become's default."""

from pathlib import Path

import yaml

from .base import Issue

RULE_ID = "redundant-become-user-root"


def run(files: list[Path]) -> list[Issue]:
    """Flag every `become_user: root`, including inside blocks."""
    issues = []

    for file in files:
        try:
            root = yaml.compose(file.read_text())
        except yaml.YAMLError:
            continue  # ponytail: unique-step-names already reports invalid YAML, don't warn twice

        issues += [
            Issue(
                rule_id=RULE_ID,
                message="become_user: root is the default, remove it",
                locations=[f"{file}:{line}"],
            )
            for line in _find_become_user_root(root)
        ]

    return issues


def _find_become_user_root(node: yaml.Node | None) -> list[int]:
    if isinstance(node, yaml.SequenceNode):
        return [line for child in node.value for line in _find_become_user_root(child)]
    if not isinstance(node, yaml.MappingNode):
        return []

    lines = []
    for key_node, value_node in node.value:
        if key_node.value == "become_user" and isinstance(value_node, yaml.ScalarNode) and value_node.value == "root":
            lines.append(value_node.start_mark.line + 1)
        lines += _find_become_user_root(value_node)
    return lines
