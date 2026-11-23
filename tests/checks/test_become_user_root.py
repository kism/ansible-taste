from pathlib import Path

from ansible_taste.checks.become_user_root import RULE_ID, run


def test_become_user_root_flagged_including_in_blocks(tmp_path: Path) -> None:
    file = tmp_path / "main.yml"
    file.write_text(
        "- name: a\n  become_user: root\n  become: true\n- name: b\n  block:\n    - name: c\n      become_user: root\n",
    )

    issues = run([file])

    assert [issue.locations[0] for issue in issues] == [f"{file}:2", f"{file}:7"]
    assert {issue.rule_id for issue in issues} == {RULE_ID}


def test_other_users_and_invalid_yaml_pass(tmp_path: Path) -> None:
    good = tmp_path / "good.yml"
    good.write_text("- name: a\n  become: true\n  become_user: postgres\n")
    bad = tmp_path / "bad.yml"
    bad.write_text("- name: [unclosed\n")

    assert run([good, bad]) == []
