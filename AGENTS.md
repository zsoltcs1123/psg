# AGENTS.md

> Baseline guidance for AI coding agents. For detailed python standards see `.cursor/rules/`.

**psg** — Product State Graph. Python 3.14, uv workspace. Planned packages under `packages/` (`psg-domain`, `psg-persistence`, `psg-api`, `psg-cli`).

Donor implementation: [agentic-engineering](https://github.com/zsoltcs1123/agentic-engineering) `packages/anneal`. Rebuild plan: [docs/SEED.md](docs/SEED.md). System architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Development loop

Read `PRINCIPLES.md` and `DEVELOPING.md` before coding work, answering queries or giving advice.
Iterate with path-local ruff/mypy (`packages/<pkg>`). Canonical gate: `uv run prek run --all-files`.
Commit only after the gate. Commit rules: `DEVELOPING.md`.

## Anneal

The psg project is managed via anneal (the donor system - we use it to build the new one). Use `/anneal` skill to interact with it. When writing anneal content, always apply the `technical-writing` skill.

# Donor repository

PSG rebuilds behavior from the Anneal package in the agentic-engineering monorepo.

| Item              | Location                                                                         |
| ----------------- | -------------------------------------------------------------------------------- |
| Repository        | https://github.com/zsoltcs1123/agentic-engineering                               |
| Donor package     | `packages/anneal`                                                                |
| Seed (this repo)  | [docs/SEED.md](docs/SEED.md)                                                     |
| Architecture      | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)                                     |
| Feature inventory | [docs/anneal/donor-feature-inventory.md](docs/anneal/donor-feature-inventory.md) |

Anneal is reference only. The Anneal name and metaphor are retired in PSG.

Use local checkout `~/repos/agentic-engineering` to access the repo. Fallback to gh CLI.
