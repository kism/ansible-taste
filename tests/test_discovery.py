from pathlib import Path

from ansible_taste.discovery import find_task_files


def _make_role(root: Path, role: str) -> Path:
    tasks_dir = root / "roles" / role / "tasks"
    tasks_dir.mkdir(parents=True)
    return tasks_dir


def test_find_task_files_yml_and_yaml(tmp_path: Path) -> None:
    tasks_dir = _make_role(tmp_path, "foo")
    (tasks_dir / "main.yml").write_text("- name: a\n")
    (tasks_dir / "extra.yaml").write_text("- name: b\n")

    files = find_task_files(tmp_path, [])

    assert {f.name for f in files} == {"main.yml", "extra.yaml"}


def test_find_task_files_ignores_other_dirs(tmp_path: Path) -> None:
    tasks_dir = _make_role(tmp_path, "foo")
    (tasks_dir / "main.yml").write_text("- name: a\n")

    vars_dir = tmp_path / "roles" / "foo" / "vars"
    vars_dir.mkdir()
    (vars_dir / "main.yml").write_text("x: 1\n")

    nested = tasks_dir / "subdir"
    nested.mkdir()
    (nested / "nested.yml").write_text("- name: c\n")

    files = find_task_files(tmp_path, [])

    assert [f.name for f in files] == ["main.yml"]


def test_find_task_files_respects_exclude_paths(tmp_path: Path) -> None:
    _make_role(tmp_path, "foo")
    (tmp_path / "roles" / "foo" / "tasks" / "main.yml").write_text("- name: a\n")
    _make_role(tmp_path, "legacy")
    (tmp_path / "roles" / "legacy" / "tasks" / "main.yml").write_text("- name: b\n")

    files = find_task_files(tmp_path, ["roles/legacy/*"])

    assert len(files) == 1
    assert "legacy" not in str(files[0])
