# Development Guide

All commands use `uv run`. Works on all platforms.

## Commands

```bash
uv run ruff format .                                    # Format code
uv run ruff check .                                     # Lint
uv run ruff check --fix .                               # Lint + auto-fix
uv run mypy .                                           # Type check
uv run pytest                                           # Run all tests
uv run pytest -m unit                                   # Unit tests only
uv run pytest -m integration                            # Integration tests only
uv run pytest --cov=src --cov=packages                  # Tests with coverage
uv run prek run --all-files                             # Canonical gate
```

A `Makefile` wraps the same `uv run` commands (`make check`, `make test`, etc.).

## Pre-commit

[prek](https://github.com/j178/prek) runs the gate on `git commit`. Hook list and args live in `.pre-commit-config.yaml`.

```bash
uv sync --dev
uv run prek install --hook-type pre-commit --hook-type commit-msg
```

## Commits

[Conventional Commits](https://www.conventionalcommits.org/) with required scopes. Allowed types and scopes: `.pre-commit-config.yaml` (`conventional-pre-commit` hook).

- One line only: `{type}({scope}): {description}`. No body, no blank line after the subject.
- Description: imperative mood, lowercase start, no trailing period, max 72 characters.

Example: `feat(domain): add workflow transition guards`

Do not use a HEREDOC or `-m` twice to add a body. Do not paste bullet lists into the commit message.

## Version Bumping

[Commitizen](https://commitizen-tools.github.io/commitizen/) bumps version, changelog, and tag from conventional commits:

```bash
uv run cz bump
```

Config: `pyproject.toml` → `[tool.commitizen]`.

## Configuration Files

| File                       | Purpose                                      |
| -------------------------- | -------------------------------------------- |
| `pyproject.toml`           | Project metadata, deps, coverage, commitizen |
| `ruff.toml`                | Linting and formatting                       |
| `mypy.ini`                 | Type checking                                |
| `pytest.ini`               | Test discovery and markers                   |
| `.pre-commit-config.yaml`  | Pre-commit hooks                             |
| `.github/workflows/ci.yml` | CI: same prek gate, frozen lock              |
| `.github/dependabot.yml`   | Weekly uv and Actions version-update PRs     |
| `.editorconfig`            | Editor formatting consistency                |
| `.secrets.baseline`        | Secret detection false positives             |

## CI and dependency updates

GitHub Actions runs `uv run --frozen prek run --all-files` on push and pull requests to `main` / `master`. No automerge. No Codecov (needs a separate account).

Dependabot opens weekly version-update PRs for `uv` and GitHub Actions (Monday 09:00 UTC). Python majors are ignored; minors/patches are grouped. Security alerts are a separate GitHub setting, not this file.

Detailed Python and testing standards: `.cursor/rules/python.mdc`, `.cursor/rules/python-testing.mdc`.
