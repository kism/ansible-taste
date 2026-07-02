# Development

Full local CI check (type check, format, lint-fix, tests):

```bash
scripts/run-ci-local.sh
```

Individual tools, configured in `pyproject.toml`:

```bash
ty check                  # type checker
ruff format
ruff check --fix
pytest -q --tb=short
```

## Test Coverage

```bash
scripts/run-coverage.sh
python -m http.server -b 127.0.0.1 8000 -d htmlcov
```

Open the link in your browser and browse into the `htmlcov` directory.
