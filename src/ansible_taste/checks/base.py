"""Shared types for checks."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Issue:
    """A single style violation found by a check."""

    rule_id: str
    message: str
    locations: list[str]


@dataclass(frozen=True)
class Check:
    """A registered check: a rule_id and its run function."""

    rule_id: str
    run: Callable[[list[Path]], list[Issue]]
