from pathlib import Path

from ansible_taste.checks.comment_ratio import RULE_ID as COMMENT_RATIO_RULE_ID
from ansible_taste.checks.unique_names import RULE_ID as UNIQUE_NAMES_RULE_ID
from ansible_taste.config import Config
from ansible_taste.scanner import scan


def _make_project(root: Path) -> None:
    tasks_dir = root / "roles" / "foo" / "tasks"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "main.yml").write_text(
        "- name: Install package\n- name: Install package\n# a\n# b\n# c\n# d\n",
    )


def test_skip_list_disables_a_check(tmp_path: Path) -> None:
    _make_project(tmp_path)

    issues = scan(tmp_path, Config(exclude_paths=[], skip_list=[COMMENT_RATIO_RULE_ID]))

    assert [issue.rule_id for issue in issues] == [UNIQUE_NAMES_RULE_ID]


def test_both_checks_report_together(tmp_path: Path) -> None:
    _make_project(tmp_path)

    issues = scan(tmp_path, Config(exclude_paths=[], skip_list=[]))

    assert {issue.rule_id for issue in issues} == {UNIQUE_NAMES_RULE_ID, COMMENT_RATIO_RULE_ID}
