# Entity types and status transitions — program design

This document records the program design for the first `psg-domain` change. It covers file layout, key types and signatures, call flow, import boundaries, and the vertical slice plan. Implementation bodies come later. The architecture doc is `dom-c1-architecture.md`.

## Design judgment

| Test | Result |
| --- | --- |
| Deletion | `workflow.py` holds tables and three functions. Cut it and logic scatters. Keep one module. |
| Small surface | Three public workflow functions plus entity structs. Tables stay private. |
| Seam | No ports yet. Persistence loads entities; domain validates. The full GraphRepository seam waits for the persistence change. |
| Locality | Transitions, guards, and their tables live together in `workflow.py`. Entities stay in `entities.py`. |
| Test through surface | Tests construct structs and call `transition` and the guards directly. No database and no HTTP. |

**Partial boundary.** This change has no repository port. The persistence change adds typed load helpers before write orchestration.

## Call flow

### Move Change or Milestone to `in_progress`

```
caller (later: persistence write orchestration)
├── assert_dependencies_clear(targets)
│   └── _is_dependency_cleared(target)  # per-family cleared check
└── transition(entity, WorkflowStatus.in_progress)
    ├── _transition_table_for(status)   # pick table from enum type
    └── msgspec.structs.replace(...)    # return new entity
```

### Move Milestone to `done`

```
caller
├── assert_milestone_completeable(milestone, scheduled_tasks, scheduled_bugs)
│   └── _is_resolved(task|bug)        # shares _RESOLVED_TRIAGE with dependency guard
└── transition(milestone, WorkflowStatus.done)
```

### Illegal transition (wrong step)

```
caller
└── transition(entity, new_status)
    └── raise InvalidTransitionError(current, requested, allowed)
```

### Wrong status family

```
caller
└── transition(entity, new_status)
    └── raise InvalidTransitionError(current, requested, allowed=[])
```

### Same status (no-op)

```
caller
└── transition(entity, entity.status)
    └── return entity unchanged
```

## File layout

```
packages/psg-domain/
├── pyproject.toml                          # NEW — msgspec dep, hatch build, pytest testpaths
├── src/psg_domain/
│   ├── __init__.py                         # NEW — re-export public surface
│   ├── entities.py                         # NEW — enums, code aliases, structs
│   ├── errors.py                           # NEW — three domain errors
│   └── workflow.py                         # NEW — tables, transition, guards
└── tests/
    ├── test_entities.py                    # NEW — struct smoke with valid codes
    ├── test_transition.py                  # NEW — all four enum tables
    └── test_guards.py                      # NEW — dependency and milestone guards

.importlinter                               # NEW — forbidden contract
pyproject.toml                              # MOD — uncomment psg-domain workspace source
pytest.ini                                  # MOD — add packages/psg-domain/tests to testpaths
ruff.toml                                   # MOD — known-first-party += psg_domain
.pre-commit-config.yaml                     # MOD — enable import-linter hook; add import-linter dep
uv.lock                                     # MOD — sync after workspace member added
```

The root `src/psg/` stub stays untouched.

## Types and signatures

### `entities.py`

```python
# Code aliases (msgspec Meta pattern)
ProjectCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+$")]
MilestoneCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-MS\d+$")]
ChangeCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-C\d+$")]
FactCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-F\d+$")]
TaskCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-T\d+$")]
ValidationCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-V\d+$")]
BugCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-B\d+$")]
IdeaCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-I\d+$")]

class ChangeKind(StrEnum):
    new_feature = "new_feature"
    feature_update = "feature_update"
    cross_cutting = "cross_cutting"
    refactor = "refactor"

class WorkflowStatus(StrEnum): ...       # pending, in_progress, done
class ProjectStatus(StrEnum): ...     # pending, in_progress, obsolete
class LifecycleStatus(StrEnum): ...      # active, superseded  (no obsolete)
class TriageStatus(StrEnum): ...         # open, done, wontfix, converted

class BugSeverity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class ValidationScenario(Struct, kw_only=True):
    description: str

class Project(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ProjectCode
    status: ProjectStatus = ProjectStatus.pending

class Milestone(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: MilestoneCode
    status: WorkflowStatus = WorkflowStatus.pending
    # no sequence field

class Change(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ChangeCode
    kind: ChangeKind                       # required, no default
    status: WorkflowStatus = WorkflowStatus.pending
    # no sequence field

class Fact(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: FactCode
    status: LifecycleStatus = LifecycleStatus.active
    superseded_by: int | None = None

class Task(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: TaskCode
    status: TriageStatus = TriageStatus.open
    change_id: int | None = None
    milestone_id: int | None = None
    converted_to_code: str = ""

class Validation(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ValidationCode
    status: LifecycleStatus = LifecycleStatus.active
    scenarios: list[ValidationScenario] = []
    coverage: list[str] = []
    change_id: int | None = None
    superseded_by: int | None = None

class Bug(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: BugCode
    status: TriageStatus = TriageStatus.open
    severity: BugSeverity = BugSeverity.medium
    change_id: int | None = None
    milestone_id: int | None = None
    converted_to_code: str = ""

class Idea(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: IdeaCode
    status: TriageStatus = TriageStatus.open
    converted_to_code: str = ""

class DocumentRef(Struct, kw_only=True):
    doc_type: str
    path: str
    project_id: int | None = None
    change_id: int | None = None
    # no status, no workspace_id in architecture table — match architecture doc

StatusOwning = Project | Milestone | Change | Fact | Task | Validation | Bug | Idea
DependencyTarget = StatusOwning          # guard inspects .status on each target
```

### `errors.py`

```python
class InvalidTransitionError(Exception):
    current: str
    requested: str
    allowed: list[str]

class BlockedByDependencyError(Exception):
    blocking_codes: list[str]

class MilestoneIncompleteError(Exception):
    milestone_code: str
    blocking_codes: list[str]
```

### `workflow.py`

```python
VALID_WORKFLOW_TRANSITIONS: dict[WorkflowStatus, list[WorkflowStatus]]
VALID_PROJECT_STATUS_TRANSITIONS: dict[ProjectStatus, list[ProjectStatus]]
VALID_LIFECYCLE_TRANSITIONS: dict[LifecycleStatus, list[LifecycleStatus]]
VALID_TRIAGE_TRANSITIONS: dict[TriageStatus, list[TriageStatus]]

_RESOLVED_TRIAGE: frozenset[TriageStatus]  # done, wontfix, converted — shared by both guards

StatusValue = WorkflowStatus | ProjectStatus | LifecycleStatus | TriageStatus

def transition[E: StatusOwning](entity: E, new_status: StatusValue) -> E: ...

def assert_dependencies_clear(targets: Sequence[DependencyTarget]) -> None: ...

def assert_milestone_completeable(
    milestone: Milestone,
    scheduled_tasks: Sequence[Task],
    scheduled_bugs: Sequence[Bug],
) -> None: ...
```

Private helpers (not exported):

```python
def _allowed_transitions(current: enum.Enum) -> list[enum.Enum]: ...
def _is_dependency_cleared(target: DependencyTarget) -> bool: ...
def _is_resolved(item: Task | Bug) -> bool: ...
```

`_is_dependency_cleared` dispatches on `type(target.status)`:

| Status enum | Cleared when |
| --- | --- |
| `WorkflowStatus` | `done` |
| `ProjectStatus` | `in_progress`, `obsolete` |
| `TriageStatus` | member of `_RESOLVED_TRIAGE` |
| `LifecycleStatus` | `active`, `superseded` (never blocks) |

`_is_resolved` checks `item.status in _RESOLVED_TRIAGE`.

### `__init__.py`

Re-export entity structs, enums, the three workflow functions, and the three errors.

## Import boundaries

```
tests ──► psg_domain.workflow
       ──► psg_domain.entities
       ──► psg_domain.errors

psg_domain ──► msgspec
            ──► stdlib only (enum, typing, msgspec.structs)

FORBIDDEN from psg_domain:
  psg, psg_persistence, psg_api, psg_cli
  FastAPI, Typer, Pydantic, httpx, SQLAlchemy, aiosqlite
```

Inner policy (`psg_domain`) names no transport, ORM, or sibling package. Guards take entity structs, not database rows. Persistence (later) maps rows to structs before it calls guards.

The import-linter contract lists `psg_domain` as the source and the forbidden modules above. Set `include_external_packages = true`.

## Vertical slices

Three slices. Each ends with `uv run pytest packages/psg-domain -m unit` green. Update these docs before slice 1 if they drift.

### Slice 1 — Package and entity model

**Ship.** `packages/psg-domain` workspace member, uncomment `psg-domain` in root `pyproject.toml`, `entities.py` with all enums and structs, minimal smoke tests (construct each struct with valid codes and `workspace_id`, assert defaults).

**Observable.** `uv sync`, `uv run mypy packages/psg-domain`, pytest collects and passes struct tests.

**Out of scope.** Workflow, guards, import-linter, negative code-pattern tests.

### Slice 2 — State machine

**Ship.** `errors.py`, `workflow.transition`, four transition tables, `test_transition.py`.

**Tests pin.**

- Legal step on every enum (including `pending` to `obsolete`, triage terminals stay terminal)
- Skipped steps rejected
- Terminal to anything rejected
- Wrong enum family rejected with `allowed=[]`
- Same status returns unchanged entity
- `InvalidTransitionError` fields populated (non-empty `allowed` on illegal step)

**Observable.** Full transition table coverage green.

### Slice 3 — Guards and repo boundaries

**Ship.** `assert_dependencies_clear`, `assert_milestone_completeable`, `test_guards.py`, `.importlinter`, prek hook uncommented, root config updates (pytest testpaths, ruff first-party, `import-linter` dev dep).

**Tests pin.**

- Empty dependency list passes
- Per-family cleared sets: at least Project (`in_progress`), Change (`done`), and Task (`wontfix`); LifecycleStatus never blocks; uncleared statuses block with sorted `blocking_codes`
- Thin Milestone `in_progress` path (empty deps pass)
- Milestone with all scheduled tasks and bugs resolved passes
- Open scheduled task or bug blocks with `MilestoneIncompleteError(milestone_code, blocking_codes)`; codes sorted

**Observable.** `uv run lint-imports` passes; prek import-linter hook enabled; full unit suite green.

## Bindings

| Source | Binding |
| --- | --- |
| Architecture doc | Four enums, one `transition`; per-family dependency-cleared sets (`ProjectStatus`: `pending` / `in_progress` / `obsolete`; `LifecycleStatus` never blocks); guards take entity lists; no `sequence` on Change or Milestone; `LifecycleStatus` without `obsolete`; `milestone_id` on Task and Bug |
| Project seed | Fact and Task taxonomy; `workspace_id` on rows; blocked is a projection, not a status |
| ADRs | None registered yet for DOM |

No conflicts between the architecture doc and the change goal or deliverables.
