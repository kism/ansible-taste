import argparse
import logging

import pytest

from ansible_taste import __main__


def test_main(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    caplog.set_level(logging.INFO)

    mock_args = argparse.Namespace(v=0, message="Hello, World!")
    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", lambda self: mock_args)

    __main__.main()
    assert "Hello, World!" in caplog.text
    assert "ansible-taste v0.0.1" in caplog.text
    assert "Hello, World!" in caplog.text
