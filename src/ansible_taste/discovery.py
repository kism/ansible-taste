"""Find Ansible role tasks files to scan."""

from fnmatch import fnmatch
from pathlib import Path


def find_task_files(root: Path, exclude_paths: list[str]) -> list[Path]:
    """Find roles/<role>/tasks/*.yml|*.yaml files under root, honouring exclude_paths globs."""
    files = sorted({*root.glob("roles/*/tasks/*.yml"), *root.glob("roles/*/tasks/*.yaml")})

    return [f for f in files if not _is_excluded(f.relative_to(root), exclude_paths)]


def _is_excluded(relative_path: Path, exclude_paths: list[str]) -> bool:
    return any(fnmatch(relative_path.as_posix(), pattern) for pattern in exclude_paths)
