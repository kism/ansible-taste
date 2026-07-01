from pathlib import Path

from ansible_taste.config import Config, load_config


def test_load_config_missing_file(tmp_path: Path) -> None:
    assert load_config(tmp_path) == Config(exclude_paths=[], skip_list=[])


def test_load_config_parses_keys(tmp_path: Path) -> None:
    (tmp_path / ".ansible-taste").write_text("exclude_paths:\n  - roles/legacy/*\nskip_list:\n  - comment-ratio\n")

    config = load_config(tmp_path)

    assert config == Config(exclude_paths=["roles/legacy/*"], skip_list=["comment-ratio"])


def test_load_config_missing_keys_default_empty(tmp_path: Path) -> None:
    (tmp_path / ".ansible-taste").write_text("exclude_paths:\n  - roles/legacy/*\n")

    config = load_config(tmp_path)

    assert config == Config(exclude_paths=["roles/legacy/*"], skip_list=[])
