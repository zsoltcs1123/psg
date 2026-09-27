# Product State Graph — project seed

Product State Graph (PSG) is an agent-facing state graph for software products. It holds delivery state in SQL: what you build, in what order, what done means, current intent, and what you know. The primary editors and maintainers of the graph are coding agents or harnesses. Human operators use PSG to monitor and steer the product's development.

One PSG server hosts the graph for many products. A developer runs one server for all personal projects. A company runs one server for all company projects. Code repos hold a pointer to the server and a project code. They do not host the database.

This seed describes the product you rebuild in a new repository. The donor is [`packages/anneal`](https://github.com/zsoltcs1123/agentic-engineering/tree/main/packages/anneal) in the [agentic-engineering](https://github.com/zsoltcs1123/agentic-engineering) monorepo — implementation reference only. The Anneal name and metaphor are retired. Move code piece by piece with rigorous engineering. This document does not list migration steps. For a full keep/discard/maybe list of donor features, see [Donor feature inventory](anneal/donor-feature-inventory.md). System structure is in [Architecture](ARCHITECTURE.md).

## Why this product exists

Software delivery spreads across many stores. Source code lives in git. Specs and decisions live in markdown files or a doc site. Research notes may live in a wiki. Metrics live in SQL or some SaaS. Customer docs live elsewhere.

None of those separate stores have a combined answer to the questions an agent needs during delivery:

- How is the project structured?
- What is the project's state?
- What is the current task at hand and how does it relate to the project as a whole?
- Which design documents are needed for the completion of the task?
- In what order should the work be delivered?
- How to verify and validate changes?
- What durable facts should the next agent know?
- What is open, deferred, or broken?
- How to track potential work that arises during delivery?

PSG answers those questions with typed entities, dependency edges, workflow status, and document refs to external stores. Narrative stays in the external stores. PSG indexes their content.

It is the system that aggregates all the stores and provides an optimized context bundle for the task at hand, whether that task is design or planning work, code implementation, or simply answering queries.

PSG is not a wiki, a document store, or an issue tracker. It does not own committed vocabulary. An external glossary owns terms. PSG consumes them.

## What PSG connects to

PSG is store-agnostic. It does not assume a fixed delivery stack. In practice it links to external systems through refs and through tools that read both PSG and those systems.

| External system (example) | Typical store             | How PSG links                                                                                     |
| ------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------- |
| Source code               | git                       | Changes drive implementation. A housekeep skill can catch drift between state and repo.           |
| Specs and decisions       | markdown in git, doc site | `DocumentRef` on projects and changes (`prd`, `architecture`, `adr`, and consumer-defined types). |
| Research                  | wiki, notes repo          | Out of PSG scope. Research may inform specs; PSG does not hold exploratory notes.                 |
| Metrics                   | SQL, SaaS                 | Out of PSG scope. Metrics may inform triage in external tools.                                    |
| Customer docs             | published site            | Out of PSG scope.                                                                                 |

PSG holds structured state and pointers. Deep read and edit of prose, code, and metrics stay in each system's native tool.

PSG does not grow orchestration mechanism: no run entity, no checker hooks, no ready queue, no `psg execute`. An external orchestrator may call the API, dispatch work, and write state back. That orchestrator is not part of PSG.

## Who uses PSG

Coding agents are the primary users. They work in parallel against the same server. Parallel agents need one API front door so writes serialize cleanly and conflicts surface as errors, not silent overwrites.

Humans use the same `psg` CLI. PSG is not a universal UI for delivery work. Read specs where those files live. Edit code in the IDE. Query state with `psg context` and `psg view`.

## What PSG holds

Delivery state is a nested project tree. Every node is a `Project`. Child entities attach to a project. One workspace holds many root projects — one per product you track in that PSG instance.

```
Workspace (tenant: person or org)
└── Project (product A)
    ├── Project (sub-project)
    ├── Milestone
    ├── Change
    ├── Fact
    ├── Validation
    ├── Task
    ├── Bug
    └── Idea
└── Project (product B)
    └── …
```

Dependency edges (`link --depends-on`) are separate from traceability links (`change_id`, `bug_change`, `superseded_by`).

### Entity roles

**Project** — durable container with scope, boundaries, and optional capabilities. Status is `pending`, `in_progress`, or `obsolete`. Projects do not reach `done`. `obsolete` retires the product and keeps the tree.

**Milestone** — time-boxed checkpoint: what must be true for a phase (`goal`, `success_criteria[]`), not how to get there. Status flows `pending` → `in_progress` → `done`. Schedule changes, tasks, bugs, and ideas into a milestone (`schedule` / `unschedule`) to attach scope. A milestone cannot move to `done` while any scheduled member is unresolved: changes must be `done`; tasks, bugs, and ideas must be `done`, `wontfix`, or `converted`. Unschedule an item if it should not gate completion. `success_criteria` are separate observable checks the team verifies at hand-over; they do not replace the guard.

**Change** — substantial round of work with a clear deliverable. Small fixes and repo maintenance should not create changes. Carries a goal, deliverables, and optional document refs to external markdown. Status is `pending` → `in_progress` → `done`. Unfinished dependencies block the move to `in_progress`. Blocked is a read projection, not a stored status.

**Fact** — durable project memory: rationale, constraints, and non-obvious intentional behavior. Not an architecture decision record, not a task. Status is `active` or `superseded`. Facts may supersede earlier facts. A fact with no successor is deleted.

**Validation** — authored invariant with lifecycle and optional repo coverage claims. Outcomes live in the repo. Status is `active` or `superseded`, same machine as Fact.

**Task** — project-owned deferred work. Smaller than a Change. Default here when durability is unclear. Status is triage: `pending`, `in_progress`, `done`, `wontfix`, or `converted`. `pending` may go straight to `done`. A task worked directly may pass through `in_progress`. A task is usually absorbed by a Change through `change_id` and stays `pending` until that work closes it. It converts 1:1 only when the leftover grows into a Change or a Project.

**Bug** — broken behavior. Same triage statuses as Task. A bug fixed directly may be `in_progress`. Usually absorbed by a Change through a change link, then `done`. Rarely converts 1:1.

**Idea** — future direction. Same triage statuses. `in_progress` means the idea is being shaped. Convert is the normal promotion: `converted_to_code` points at a Change or a Project.

**DocumentRef** — typed pointer to a document in an external store (`vision`, `architecture`, `adr`, and consumer-defined types). The donor dropped the first-class ADR entity. Decision prose stays in the external store; PSG holds the ref and status metadata.

### Vocabulary

PSG consumes committed vocabulary from elsewhere. It does not store definitions.

- Entity titles, goals, and deliverables use terms from the project's glossary.
- Fact entries may reference `concept:*` slugs (for example from a `GLOSSARY.md` in a docs repo).
- Do not introduce terms in PSG that are not in the glossary.
- When a term crystallizes, add it to the glossary first. Then use it in PSG and code.

A `concept:*` slug is a stable cross-system identifier. Display names may change. Slugs do not.

## Data design notes

PSG stays a SQL state graph of typed entities. Not a wiki, not git markdown as source of truth, not an issue tracker.

The entity tree above is the locked taxonomy. Use **Fact** and **Task**, not donor names Knowledge and Followup. Do not restore the ADR entity.

Document refs stay opaque strings. PSG lists type and ref in `psg context`. It does not fetch or render external markdown.

## Scope tiers

### MVP

Core service in the new repository.

Ship:

- Domain models and the Workflow module
- ContextAssembly and ViewProjection
- TriageEntity module (Bug, Idea, and Task)
- GraphRepository persistence port and the sqlite adapter
- Workspace module: bearer token auth, membership, and row scoping
- The HTTP API
- Optimistic concurrency
- The CLI: `psg context`, `psg view`, search, CRUD, recode, backup, migrate, and export
- CLI renderers
- `psg serve`
- Agent skills (`/psg`, implement, plan, housekeep, init)
- Multi-project support inside one workspace

Defer MCP to V1 if it blocks MVP.

MVP is also the layer cleanup pass. Donor code in `packages/anneal` works, but seams may be wrong. Split domain, persistence, API, and CLI client without changing behavior unless a constraint is wrong.

### V1

Production multi-user and agent tooling.

Add or harden:

- The postgres adapter
- Multi-user workspace membership (no SSO yet)
- MCP wrapping the HTTP API
- Hosted deployment story (you run the same API image; not a new schema)

V1 does not add k8s orchestration requirements.

## How you rebuild it

Create a new repository for Product State Graph. Treat `packages/anneal` as the donor.

1. **Cut dead seams first.** Delete donor paths marked discard before lifting anything: vector search stub (`queries/search/vector.py`), `upload` CLI, `view-set`, `Change.sequence`, `embedding_id` columns, leftover `adr/markdown.py` (ADR entity removed in ADR-009). Do not port then delete — dead code widens the persistence interface for no gain.
2. **Domain first.** Lift `domain/models.py`, consolidate the Workflow module (pull guards out of `storage/` and `commands/`), collapse triage into TriageEntity, lift ContextAssembly and ViewProjection from `queries/`.
3. **Persistence port second.** Merge `storage/` + `db/` behind GraphRepository. Sqlite adapter only at first. No raw connection outside adapters.
4. **Workspace third.** Schema with `workspace_id` on all rows, membership tables, auth middleware. Bigger than entity rename — do not retrofit after CRUD lands.
5. **API fourth.** Thin FastAPI handlers, Pydantic DTOs, optimistic concurrency (409), workspace scoping on every route.
6. **CLI client fifth.** Replace `cli/_workspace.py` sqlite access with HTTP calls. Keep text renderers client-side.
7. **Skills last.** Bundle after CLI proves the API contract.

Fix a layer when the seam is wrong. If the CLI imports sqlite directly, replace it with API calls.

Keep behavior unless a locked decision says otherwise. Locked: state graph role, Fact and Task taxonomy, no ADR entity, Fact and Validation `active`/`superseded` only (no `obsolete` on that enum), `wontfix` kept, blocked as a read projection not a status, convert as 1:1 promotion vs `change_id` absorption, milestone `done` blocked until every scheduled change, task, bug, and idea is in a terminal status (donor Anneal only gated tasks and bugs and treated scheduled changes as scope-only), workspace tenancy from MVP. Structure locks are in [Architecture](ARCHITECTURE.md).

Run the canonical gate (`prek run --all-files`) before you merge each piece. That gate is the minimum quality loop: formatting, lint, types, tests, and module boundaries. Add a complexity-plus-coverage gate for agent-written code (CRAP or an equivalent) so cleanliness is mechanical, not review-by-diff.

A blank-page rewrite is a risk. The donor has working CLI commands, migrations, and tests. Move and harden beats rewrite from memory. ~70% of donor integration tests assume in-process sqlite — rewrite as domain unit tests, API contract tests, and thin CLI e2e against `psg serve`.

## What we keep and discard from the donor

See [Donor feature inventory](anneal/donor-feature-inventory.md) for the full list with maybe items.

**Keep:** entity system (rename Knowledge → Fact, Followup → Task, ChangeKind → ChangeType), dependency graph, traceability links, milestones, document refs, hierarchical codes and recode, `context` / `view` / `search` / `log`, CRUD commands, state machine and transition guards, FTS search, mutation log, bundled skills (`/psg`, implement, plan, init), sqlite and postgres adapters.

**Discard:** change `sequence`, milestone composition, `upload`, `view-set`, vector search stub and `embedding_id` columns, leftover `adr/markdown.py`, legacy migration hooks, `OPERATING-CONTRACT.md`, donor naming (`anneal` → `psg`), per-repo database hosting, CLI in-process domain access, raw `sqlite3.Connection` as the persistence interface, `obsolete` on Fact and Validation. Do not resurrect removed donor entities (ADR, ValidationRun, deliverable entity, and so on). Cut these in the first PR of the new repo — see How you rebuild it step 1.

**Defer:** MCP (V1 if not MVP), multi-user membership polish (V1).

## Risks and open questions

**Rewrite temptation.** A new repo feels like permission to redesign everything. Resist unless a locked decision requires it. Move working code, then delete dead paths.

## What this is not

| Tool                  | Why it is different                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------ |
| Linear, Jira          | Org-scale issue tracking. PSG **Task** is project-scoped deferred work, not a replacement. |
| Notion, Obsidian      | Document stores. PSG holds structured state, not prose bodies.                             |
| Markdown files in git | Shared files give docs but not a queryable graph, deps, or workflow status.                |
| An orchestrator       | Run tracking, checkers, cadence, land path. May consume PSG; does not live inside it.      |

The donor `packages/anneal` is the starting implementation. Rename the CLI to `psg`, Knowledge to Fact, and Followup to Task in the rebuild. Do not inherit package layout if seams are wrong.

## Success criteria

Rebuild succeeded when:

- An agent runs `psg context` against a running server and gets the same class of answers as the donor.
- One PSG instance holds multiple products in one workspace.
- No narrative prose moved into PSG tables. Document refs still point at external stores.
- External orchestrators consume PSG through the API and MCP, without new PSG entities for runs or queues.

## One line

Product State Graph is the SQL state graph for delivery: one server, many products, typed entities, deps, workflow status, and refs to external docs. Agents query and update it through the API.
