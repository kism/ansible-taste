from pathlib import Path

from ansible_taste.checks.unique_names import RULE_ID, run


def test_no_duplicates(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- name: a\n- name: b\n")

    assert run([file]) == []


def test_duplicate_across_files(tmp_path: Path) -> None:
    file_a = tmp_path / "a.yml"
    file_a.write_text("- name: Install package\n")
    file_b = tmp_path / "b.yml"
    file_b.write_text("- name: Install package\n")

    issues = run([file_a, file_b])

    assert len(issues) == 1
    assert issues[0].rule_id == RULE_ID
    assert set(issues[0].locations) == {f"{file_a}:1", f"{file_b}:1"}


def test_duplicate_within_one_file(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- name: Install package\n- name: Install package\n")

    issues = run([file])

    assert len(issues) == 1
    assert issues[0].locations == [f"{file}:1", f"{file}:2"]


def test_missing_name_does_not_crash(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- debug:\n    msg: hi\n")

    assert run([file]) == []


def test_invalid_yaml_is_skipped(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text("- name: a\n  bad: [unterminated\n")

    assert run([file]) == []


def test_jinja_name_duplicate_across_files_not_flagged(tmp_path: Path) -> None:
    file_a = tmp_path / "a.yml"
    file_a.write_text("- name: Install {{ package_name }}\n")
    file_b = tmp_path / "b.yml"
    file_b.write_text("- name: Install {{ package_name }}\n")

    assert run([file_a, file_b]) == []


def test_jinja_name_duplicate_within_file_flagged(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text(
        "- name: Install {{ package_name }}\n- name: Install {{ package_name }}\n",
    )

    issues = run([file])

    assert len(issues) == 1
    assert issues[0].locations == [f"{file}:1", f"{file}:2"]
