"""Check that failed_when/changed_when overrides are explained by a comment."""

import re
from pathlib import Path

from .base import Issue

RULE_ID = "unexplained-when-override"

# ponytail: line regex, not YAML - the trailing comment is source text the parser drops.
# Only literal true/false, not the yes/no spellings; widen if those turn up.
_PATTERN = re.compile(r"^\s*(?P<key>failed_when|changed_when):\s+(?P<value>true|false)\s*(?P<rest>.*)$")


def run(files: list[Path]) -> list[Issue]:
    """Flag `failed_when: false` / `changed_when: true|false` with no trailing comment saying why."""
    issues = []

    for file in files:
        for lineno, line in enumerate(file.read_text().splitlines(), start=1):
            match = _PATTERN.match(line)
            # rest is either a trailing comment (explained) or more expression (not a bare literal).
            if not match or match["rest"]:
                continue
            if match["key"] == "failed_when" and match["value"] != "false":
                continue
            message = f"{match['key']}: {match['value']} without a comment explaining why"
            issues.append(Issue(rule_id=RULE_ID, message=message, locations=[f"{file}:{lineno}"]))

    return issues
