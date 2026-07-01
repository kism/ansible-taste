# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`ansible-taste` is a CLI style-guide linter for Ansible projects. It scans
`roles/<role>/tasks/*.yml`/`*.yaml` files for "bad taste" issues (currently:
duplicate task names, and files that are mostly commented-out code) and
exits non-zero if any are found.

## Commands

Setup:

```bash
uv venv
source .venv/bin/activate
uv sync --all-extras
```

Run the linter itself:

```bash
python -m ansible_taste [path]      # defaults to cwd
ansible-taste [path]                # once installed via the [project.scripts] entry point
```

Full local CI check (matches what CI runs — type check, format, lint-fix, tests):

```bash
scripts/run-ci-local.sh
```

Individual tools, config for all of them lives in `pyproject.toml`:

```bash
ty check                  # type checker (not mypy — see Type checking below)
ruff format
ruff check --fix
pytest -q --tb=short
pytest tests/checks/test_unique_names.py::test_duplicate_across_files  # single test
```

Coverage:

```bash
scripts/run-coverage.sh   # coverage run + html + terminal report
python -m http.server -b 127.0.0.1 8000 -d htmlcov   # view the HTML report
```

### Type checking

This repo uses Astral's `ty` as the type checker, not `mypy` — `[tool.mypy]`
config and the mypy dependency have been removed. `.github/workflows/check_types.yml`
runs `ty check .`. Code should still be fully annotated (the package ships
`py.typed`), but don't reach for mypy-specific tooling or config.

### Ruff

`select = ["ALL"]` in `[tool.ruff.lint]` — nearly every rule is enabled, with
a short explicit ignore list (see `pyproject.toml`). Docstrings (`D`) are not
required. `tests/*.py` gets a separate, more permissive set of per-file
ignores (asserts, unannotated args, private member access, etc. are fine in
tests).

## Architecture

Pipeline, wired together in `ansible_taste/scanner.py::scan()` and called
from `ansible_taste/__main__.py::main()`:

```
__main__.main()
  args = _get_args()                      # positional `path` (default cwd), no flags
  config = config.load_config(Path.cwd()) # reads .ansible-taste from CWD, NOT from `path`
  issues = scanner.scan(args.path, config)
    files = discovery.find_task_files(args.path, config.exclude_paths)
    for check in checks.ALL_CHECKS:
      if check.rule_id not in config.skip_list:
        issues += check.run(files)
  if issues: console.print "... is in poor taste" + issues + count; exit 1
  else: console.print "... is in good taste"; exit 0 (implicit)
```

Key points for extending this:

- **Config** (`ansible_taste/config.py`): `.ansible-taste` is a YAML file
  read from the **current working directory**, not the scanned `path` —
  this is intentional (`ansible-taste ../other-repo` still reads config
  from here). Two keys: `exclude_paths` (glob patterns, matched via
  `fnmatch` against the path relative to the scanned root — not
  `Path.match`, since `**` glob support there needs Python 3.13+ and this
  repo targets `>=3.12`) and `skip_list` (rule IDs to disable). Missing
  file or missing keys default to empty lists, no error.

- **Discovery** (`ansible_taste/discovery.py`): only matches the top level
  of `roles/*/tasks/` — `roles/<role>/tasks/*.yml`, not
  `tasks/**/*.yml`. Nested task directories are not scanned.

- **Checks** (`ansible_taste/checks/`): each check is its own module
  (`unique_names.py`, `comment_ratio.py`) exposing a module-level `RULE_ID`
  string and a `run(files: list[Path]) -> list[Issue]` function. There is
  no plugin auto-discovery — `checks/__init__.py` is the registry: it
  explicitly wraps each module's `RULE_ID`/`run` into a `Check` dataclass
  instance and lists them in `ALL_CHECKS`. Add a new check by writing a new
  module with that same `RULE_ID`/`run` shape and adding one line to
  `ALL_CHECKS`.
  - `unique_names`: task names must be unique **across the whole project**,
    not just per-file. Uses `yaml.compose()` (not `safe_load`) per file so
    each task's `name` node retains its source line (`start_mark.line`),
    letting issue locations be `file:line` strings. Malformed YAML is
    reported via the shared console and skipped rather than crashing the
    whole scan.
  - `comment_ratio`: flags a file when whole-line comments (lines whose
    stripped content starts with `#`) are ≥30% of non-blank lines. Trailing
    inline comments (`- name: foo  # note`) do not count. Issue locations
    are file-level only — there's no single line a "too many comments"
    issue points at.

- **Output**: `ansible_taste/console.py` exports a single shared
  `rich.console.Console` instance (`console`). All CLI/check output goes
  through it (rich markup like `[bold red]...[/bold red]`) instead of
  `print()` or a logger — there is no logging framework in this project.
  `Console` auto-detects non-terminal output (e.g. `capsys` in tests), so
  it degrades to plain text automatically when not attached to a tty.

- **Versioning** (`ansible_taste/constants.py`): `PROGRAM_VERSION` comes
  from installed package metadata (`importlib.metadata.version`), and
  `PROGRAM_NAME_WITH_FULL_VERSION` additionally reads `.git/HEAD` and
  `.git/logs/HEAD` directly (no subprocess/git dependency) to append branch
  and short commit hash. `tests/test__meta.py` asserts `pyproject.toml`,
  `uv.lock`, and the installed package version all agree — keep them in
  sync when bumping the version.
