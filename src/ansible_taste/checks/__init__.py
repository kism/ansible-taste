"""Registry of all available checks."""

from . import become_user_root, comment_ratio, unique_names, when_overrides
from .base import Check

ALL_CHECKS: list[Check] = [
    Check(rule_id=unique_names.RULE_ID, run=unique_names.run),
    Check(rule_id=comment_ratio.RULE_ID, run=comment_ratio.run),
    Check(rule_id=when_overrides.RULE_ID, run=when_overrides.run),
    Check(rule_id=become_user_root.RULE_ID, run=become_user_root.run),
]
