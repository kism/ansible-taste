"""Check that tasks files aren't mostly commented-out code."""

from pathlib import Path

from .base import Issue

RULE_ID = "comment-ratio"
THRESHOLD = 0.30


def run(files: list[Path]) -> list[Issue]:
    """Flag files where whole-line comments are >= THRESHOLD of non-blank lines."""
    issues = []

    for file in files:
        non_blank = [line for line in file.read_text().splitlines() if line.strip()]
        if not non_blank:
            continue

        comments = [line for line in non_blank if line.strip().startswith("#")]
        ratio = len(comments) / len(non_blank)
        if ratio >= THRESHOLD:
            message = f"{ratio:.0%} of lines are comments (threshold {THRESHOLD:.0%})"
            issues.append(Issue(rule_id=RULE_ID, message=message, locations=[str(file)]))

    return issues
