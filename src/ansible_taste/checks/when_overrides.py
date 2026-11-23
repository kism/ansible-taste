"""Check that failed_when/changed_when/ignore_errors overrides are explained by a comment."""

import re
from pathlib import Path

from .base import Issue

RULE_ID = "unexplained-when-override"

# ponytail: line regex, not YAML - the trailing comment is source text the parser drops.
# Only literal true/false, not the yes/no spellings; widen if those turn up.
_PATTERN = re.compile(
    r"^\s*(?P<key>failed_when|changed_when|ignore_errors):\s+(?P<value>true|false)\s*(?P<rest>.*)$",
)

# Values that silence or fake a task's result; the other literal is either the default or a real condition.
_FLAGGED_VALUES = {
    "changed_when": {"true", "false"},
    "failed_when": {"false"},
    "ignore_errors": {"true"},
}


def run(files: list[Path]) -> list[Issue]:
    """Flag bare `failed_when: false`, `changed_when: true|false` and `ignore_errors: true` with no comment why."""
    issues = []

    for file in files:
        for lineno, line in enumerate(file.read_text().splitlines(), start=1):
            match = _PATTERN.match(line)
            # rest is either a trailing comment (explained) or more expression (not a bare literal).
            if not match or match["rest"] or match["value"] not in _FLAGGED_VALUES[match["key"]]:
                continue
            message = f"{match['key']}: {match['value']} without a comment explaining why"
            issues.append(Issue(rule_id=RULE_ID, message=message, locations=[f"{file}:{lineno}"]))

    return issues
