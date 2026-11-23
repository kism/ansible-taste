# ansible-taste

[![Check](https://github.com/kism/ansible-taste/actions/workflows/check.yml/badge.svg)](https://github.com/kism/ansible-taste/actions/workflows/check.yml)
[![CheckType](https://github.com/kism/ansible-taste/actions/workflows/check_types.yml/badge.svg)](https://github.com/kism/ansible-taste/actions/workflows/check_types.yml)
[![Test](https://github.com/kism/ansible-taste/actions/workflows/test.yml/badge.svg)](https://github.com/kism/ansible-taste/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/kism/ansible-taste/graph/badge.svg?token=FPGDA0ODT7)](https://codecov.io/gh/kism/ansible-taste)

A CLI style-guide linter for Ansible projects. It scans `roles/<role>/tasks/*.yml`
files for "bad taste" issues and exits non-zero if any are found.

Checks:

- **unique-step-names** - task `name`s must be unique across the whole
  project. Names containing a Jinja expression (`{{ ... }}`) are only
  compared within the same file, not across files.
- **comment-ratio** - flags a file where whole-line comments make up 30%
  or more of its non-blank lines.
- **unexplained-when-override** - flags `failed_when: false`,
  `changed_when: true|false` and `ignore_errors: true` unless a trailing
  comment explains why, e.g. `ignore_errors: true  # service may not exist yet`.
- **redundant-become-user-root** - flags `become_user: root`, which is
  already the default for `become`.

## Install

```bash
uv venv
source .venv/bin/activate
uv sync --all-extras # omit --all-extras for prod
```

## Usage

```bash
python -m ansible_taste [path]   # defaults to current directory
ansible-taste [path]             # once installed via the project's script entry point
```

`path` is the root of the Ansible project to scan (the directory containing
`roles/`). Exits `0` if no issues are found, `1` otherwise.

## Config

Add a `.ansible-taste` YAML file to the directory you run the command from
(not the scanned `path`) to customize behavior:

```yaml
exclude_paths: # glob patterns, matched against paths relative to the scanned root
  - "roles/vendored/*"
skip_list: # rule IDs to disable
  - unique-step-names
```

Both keys are optional; a missing file or missing keys default to empty lists.
