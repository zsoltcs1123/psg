# Product State Graph (PSG)

SQL state graph for agent-facing delivery: one server, many products, typed entities, dependency edges, workflow status, and refs to external docs. Agents read and write through one HTTP API.

## Donor

Implementation reference lives in the [agentic-engineering](https://github.com/zsoltcs1123/agentic-engineering) monorepo under `packages/anneal`. PSG is a greenfield rebuild guided by the seed docs below — not a rename-in-place.

## Documentation

- [Project seed](docs/anneal/SEED.md) — product scope, architecture, rebuild plan
- [Donor feature inventory](docs/anneal/donor-feature-inventory.md) — keep / discard / defer from `packages/anneal`
- [DEVELOPING.md](DEVELOPING.md) — tooling and workflow
- [AGENTS.md](AGENTS.md) — AI coding agent guidance

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Quick Start

```bash
uv sync --dev && uv pip install -e .
prek install --hook-type pre-commit --hook-type commit-msg
prek run --all-files
```

## Project Structure

```
psg/
├── packages/              # workspace members (psg-domain, psg-persistence, psg-api, psg-cli)
├── docs/anneal/           # seed and donor inventory
├── pyproject.toml         # workspace root
└── DEVELOPING.md
```

Planned workspace packages: `psg-domain`, `psg-persistence`, `psg-api`, `psg-cli`. See [SEED.md](docs/anneal/SEED.md).

## License

MIT
