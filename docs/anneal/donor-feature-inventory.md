# Donor feature inventory

Status: **reference**. Feature list from `packages/anneal` for PSG rebuild decisions. Each item is keep, discard, maybe, or defer.

Donor path: [`packages/anneal`](https://github.com/zsoltcs1123/agentic-engineering/tree/main/packages/anneal) in [agentic-engineering](https://github.com/zsoltcs1123/agentic-engineering)

---

## Core model

| Feature | What it does | Decision |
| --- | --- | --- |
| Recursive **Project** tree | Nested scope containers | keep |
| **Milestone** | Coarse ordering and completion gates | keep |
| **Change** | Goal, deliverables, workflow | keep |
| **Knowledge** → **Fact** | Durable memory | keep (rename) |
| **Followup** → **Task** | Deferred work | keep (rename) |
| **Validation** | Authored invariants and optional repo coverage claims | keep |
| **Bug** / **Idea** | Triage buckets | keep |
| **ChangeKind** | `new_feature`, `feature_update`, `cross_cutting`, `refactor` | keep |
| **ProjectStatus** | `pending`, `in_progress`, `obsolete` (donor **ProjectLifecycle**: `planned`, `live`, `obsolete`) | keep (rename enum and first two values) |
| **WorkflowStatus** | `pending` → `in_progress` → `done` | keep |
| **LifecycleStatus** | `active` → `superseded` | keep (drop donor `obsolete` on Fact and Validation) |
| **TriageStatus** | `open`, `done`, `wontfix`, `converted` | keep |
| **BugSeverity** | `low`, `medium`, `high`, `critical` | keep |

---

## Graph and links

| Feature | What it does | Decision |
| --- | --- | --- |
| **`depends-on` edges** | Execution ordering and blocked guard | keep (blocked is a guard plus a later read projection, not a status) |
| **Bug → change** traceability | `bug_change` table | keep (absorption: Bug is part of a Change) |
| **Followup/validation → change** | `change_id` FK | keep (Task and Validation absorption) |
| **Supersession** | `superseded_by` on knowledge/validation | keep (Fact and Validation. No `obsolete` on this enum) |
| **Convert** | `converted_to_code` on bug/idea/followup | keep (1:1 promotion to a Change or a Project. Default path for Idea. Rare for Task and Bug) |
| **Milestone scheduling** | Schedule change, followup, bug into milestone | keep |
| **Milestone completion guard** | Block milestone `done` if scheduled items open | keep |
| **Milestone composition** | Nested milestones (DB only, no CLI) | discard |
| **Change `sequence` field** | Manual ordering within project | discard |
| **Topological change ordering** | View layer over deps | keep |

---

## Document refs

| Feature | What it does | Decision |
| --- | --- | --- |
| **Project doc registry** | `vision`, `architecture`, `adr`, custom types | keep |
| **Change doc attach** | Per-change doc refs | keep |
| **`doc` CLI group** | register, attach, list, show | keep |
| Opaque refs (no fetch/render) | Path strings only | keep |

---

## Codes and identity

| Feature | What it does | Decision |
| --- | --- | --- |
| **Hierarchical codes** | `PRJ-C1`, `PRJ-P1`, and so on | keep |
| **Auto code generation** | On create | keep |
| **`recode`** | Rename code and cascade descendants and refs | keep |
| **`move`** | Reparent and recode | keep |

---

## CLI — read

| Command | Purpose | Decision |
| --- | --- | --- |
| `context` | Agent context bundle | keep |
| `view` | Overview, detail, filtered lists | keep |
| `deps` | Dependency subgraph or tree | keep |
| `search` | FTS keyword search | keep |
| `log` | Mutation log viewer | keep |
| `export` | Write views to export dir | maybe |
| `view-set` | Persist default output format | discard |

---

## CLI — write

| Command | Purpose | Decision |
| --- | --- | --- |
| `add *` | Create entities | keep |
| `update` | Field and status updates | keep |
| `edit` | `$EDITOR` YAML snapshot | maybe |
| `delete` | Cascade delete | keep |
| `link` / `unlink` | `depends-on` | keep |
| `schedule` / `unschedule` | Milestone membership | keep |
| `followup` / `bug` / `idea` / `validation` groups | close, convert, supersede | keep (rename followup → task) |

---

## CLI — ops

| Command | Purpose | Decision |
| --- | --- | --- |
| `init` | Workspace, root project, DB | keep |
| `migrate` | SQL migrations | keep |
| `backup` / `restore` | SQLite backup API | keep |
| `reindex` | Rebuild FTS index | keep |
| `upload` | Git-checkpoint global store | discard |
| `install-skills` | Copy skills to `.agents/skills` | keep |

---

## Persistence and workspace

| Feature | What it does | Decision |
| --- | --- | --- |
| **SQLite WAL** | Deploy-time database option | keep |
| **Repo workspace pointer** + **global project DB dir** | Split config from state (`~/.anneal/projects/`) | discard (PSG server hosts state; repo holds API pointer only) |
| **Migration chain** | Schema evolution (58 migrations in donor) | keep logic; trim on greenfield |
| **Mutation log** | Audit who, when, what | keep |
| **`workspace_id` column** | Multi-tenant prep | keep |
| **`row_version`** | Row versioning | maybe |
| **Embedding table stub** | Vector search prep | discard (MVP) |
| **Post-migration Python hooks** | Code rewrites, narrative export | discard |
| **Legacy cleanup** | Old `state.db`, `session.json` | discard (greenfield) |

---

## Search

| Feature | Decision |
| --- | --- |
| FTS5, BM25, snippets | keep |
| `--kind` filter | keep |
| Vector / semantic search stub | discard (MVP) |

---

## Renderers

| Format | Decision |
| --- | --- |
| markdown, text, json, rich (terminal) | keep md and json; maybe drop rich |
| context-specific renderer | keep |

---

## Agent skills

| Skill route | Purpose | Decision |
| --- | --- | --- |
| `/anneal` (→ `/psg`) | Default survey and CRUD loop | keep |
| `implement` | Write-back and triage on close | keep |
| `plan` | Codebase-grounded plan | keep |
| `housekeep` | Audit state vs repo drift | maybe |
| `init` | Onboard new repo hierarchy | keep |
| `OPERATING-CONTRACT.md` template | Host-repo contract | discard |

---

## Already removed in donor (do not resurrect)

| Feature | Evidence |
| --- | --- |
| Task entity (historical) | ADR-004, migration 014 |
| Feature entity | Absorbed into Project, migration 039 |
| Deliverable entity | Field on Change, migration 046 |
| ADR entity | Doc ref only, ADR-009, migration 058 |
| ValidationRun | Migrations 013, 017, 018; ADR-005 |
| Change narrative columns | Migrations 050, 053, 057 |
| Split skills (init, plan, housekeep, deliver) | Merged into one skill |
| Harness: execute, runs, checkers, ready queue | Explicit non-goal |

---

## Not in donor (PSG adds)

| Feature | Decision |
| --- | --- |
| HTTP API as sole client path | keep (MVP) |
| `psg serve` | keep (MVP) |
| Multi-project per workspace | keep (MVP) |
| Postgres adapter | keep (MVP or V1 — see SEED) |
| MCP | defer (V1 if not MVP) |
| Multi-user membership polish | defer (V1) |

---

## Summary

**Keep:** entity system (Fact and Task rename), ChangeKind, deps and traceability, milestones and scheduling, doc refs, codes and recode, context/view/search/log, CRUD CLI (as API client), state machine and guards, FTS, mutation log, skills bundle, sqlite and postgres adapters, HTTP API, `psg serve`, multi-project per workspace.

**Discard:** `upload`, `view-set`, change `sequence`, milestone composition, embedding stub, legacy migration baggage, narrative export hooks, `OPERATING-CONTRACT.md`, donor naming (`anneal` → `psg`), per-repo DB hosting, CLI in-process domain access, `obsolete` on Fact and Validation.

**Maybe:** `export`, `edit`, `row_version`, rich renderer, `housekeep` skill bundling.

**Defer:** MCP (V1 if not MVP), multi-user membership polish (V1).
