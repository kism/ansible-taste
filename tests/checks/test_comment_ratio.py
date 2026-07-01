from pathlib import Path

from ansible_taste.checks.comment_ratio import RULE_ID, run


def test_under_threshold_passes(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- name: a\n- name: b\n- name: c\n# one comment\n")

    assert run([file]) == []


def test_over_threshold_fails(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- name: a\n# commented step 1\n# commented step 2\n")

    issues = run([file])

    assert len(issues) == 1
    assert issues[0].rule_id == RULE_ID
    assert issues[0].locations == [str(file)]


def test_inline_comments_not_counted(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- name: a  # note\n- name: b  # note\n- name: c  # note\n")

    assert run([file]) == []


def test_blank_lines_excluded_from_denominator(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- name: a\n\n\n\n# comment\n")

    issues = run([file])

    assert len(issues) == 1


def test_empty_file_does_not_crash(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("")

    assert run([file]) == []
