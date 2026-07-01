import argparse
from pathlib import Path

import pytest

from ansible_taste import __main__


def _mock_args(path: Path) -> argparse.Namespace:
    return argparse.Namespace(path=path, v=0)


def test_main_pass(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", lambda self: _mock_args(tmp_path))

    __main__.main()

    assert "is in good taste" in capsys.readouterr().out


def test_main_fail(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    tasks_dir = tmp_path / "roles" / "foo" / "tasks"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "main.yml").write_text("- name: Install package\n- name: Install package\n")

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", lambda self: _mock_args(tmp_path))

    with pytest.raises(SystemExit) as exc_info:
        __main__.main()

    assert exc_info.value.code == 1
    assert "is in poor taste" in capsys.readouterr().out
