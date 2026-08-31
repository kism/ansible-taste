"""Load the .ansible-taste config file."""

from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_FILENAME = ".ansible-taste"


@dataclass(frozen=True)
class Config:
    """Parsed .ansible-taste config."""

    exclude_paths: list[str]
    skip_list: list[str]


def load_config(cwd: Path) -> Config:
    """Load .ansible-taste from cwd, defaulting to empty config if absent."""
    config_path = cwd / CONFIG_FILENAME
    if not config_path.is_file():
        return Config(exclude_paths=[], skip_list=[])

    raw = yaml.safe_load(config_path.read_text()) or {}
    return Config(
        exclude_paths=raw.get("exclude_paths") or [],
        skip_list=raw.get("skip_list") or [],
    )
