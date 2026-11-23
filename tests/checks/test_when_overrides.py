from pathlib import Path

from ansible_taste.checks.when_overrides import RULE_ID, run


def test_bare_overrides_flagged(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text(
        "- name: a\n  failed_when: false\n- name: b\n  changed_when: false\n- name: c\n  changed_when: true\n",
    )

    issues = run([file])

    assert [issue.locations[0] for issue in issues] == [f"{file}:2", f"{file}:4", f"{file}:6"]
    assert {issue.rule_id for issue in issues} == {RULE_ID}


def test_commented_overrides_pass(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text(
        "- name: a\n"
        "  failed_when: false  # grep exits 1 when nothing matches\n"
        "- name: b\n"
        "  changed_when: true # always reloads\n",
    )

    assert run([file]) == []


def test_unrelated_lines_ignored(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text(
        "- name: a\n"
        "  failed_when: true\n"  # a real condition, not a silencer
        "  changed_when: result.rc != 0\n"
        "  when: false\n",
    )

    assert run([file]) == []


def test_expression_starting_with_literal_passes(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text('- name: a\n  changed_when: false or "Upgraded uv" in configure_uv_update_result.stdout\n')

    assert run([file]) == []


def test_ignore_errors(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text(
        "- name: a\n"
        "  ignore_errors: true\n"
        "- name: b\n"
        "  ignore_errors: true  # service may not exist yet\n"
        "- name: c\n"
        "  ignore_errors: false\n",
    )

    assert [issue.locations[0] for issue in run([file])] == [f"{file}:2"]
