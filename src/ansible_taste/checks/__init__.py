"""Registry of all available checks."""

from . import comment_ratio, unique_names
from .base import Check

ALL_CHECKS: list[Check] = [
    Check(rule_id=unique_names.RULE_ID, run=unique_names.run),
    Check(rule_id=comment_ratio.RULE_ID, run=comment_ratio.run),
]
