# AGENTS.md

> Baseline guidance for AI coding agents. For detailed python standards see `.cursor/rules/`.

**psg** — Product State Graph. Python 3.14, uv workspace. Planned packages under `packages/` (`psg-domain`, `psg-persistence`, `psg-api`, `psg-cli`).

Donor implementation: [agentic-engineering](https://github.com/zsoltcs1123/agentic-engineering) `packages/anneal`. Rebuild plan: [docs/anneal/SEED.md](docs/anneal/SEED.md).

## Development loop

Read `PRINCIPLES.md` and `DEVELOPING.md` before coding work, answering queries or giving advice.
Iterate with path-local ruff/mypy (`packages/<pkg>`). Canonical gate: `uv run prek run --all-files`.
Commit only after the gate. Commit rules: `DEVELOPING.md`.
