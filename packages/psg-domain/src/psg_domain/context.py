from collections.abc import Sequence

from msgspec import Struct

from psg_domain.entities import (
    Bug,
    Change,
    DependencyTarget,
    DocumentRef,
    Entity,
    Fact,
    Idea,
    LifecycleStatus,
    Milestone,
    Project,
    Task,
    TriageStatus,
    Validation,
)

_OPEN_TRIAGE = frozenset({TriageStatus.pending, TriageStatus.in_progress})


class HistoryEvent(Struct, kw_only=True):
    at: str
    op: str
    summary: str = ""


class ContextDocRef(Struct, kw_only=True):
    doc_type: str
    path: str


class ContextAncestor(Struct, kw_only=True):
    code: str
    title: str
    type: str


class ContextChangeRef(Struct, kw_only=True):
    code: str
    title: str
    status: str


class ContextMilestoneRef(Struct, kw_only=True):
    code: str
    title: str
    status: str
    changes: list[ContextChangeRef] = []


class ContextTriageRef(Struct, kw_only=True):
    code: str
    title: str
    status: str


class ContextFactRef(Struct, kw_only=True):
    code: str
    title: str
    status: str


class ContextValidationRef(Struct, kw_only=True):
    code: str
    title: str
    status: str
    scenarios: list[str] = []


class ProjectContextLayer(Struct, kw_only=True):
    code: str
    title: str
    status: str
    description: str = ""
    milestones: list[ContextMilestoneRef] = []
    unscheduled_changes: list[ContextChangeRef] = []
    facts: list[ContextFactRef] = []
    tasks: list[ContextTriageRef] = []
    bugs: list[ContextTriageRef] = []
    ideas: list[ContextTriageRef] = []
    validations: list[ContextValidationRef] = []
    superseded_validation_count: int = 0


class ChangeContextLayer(Struct, kw_only=True):
    code: str
    title: str
    status: str
    type: str
    goal: str = ""
    deliverables: list[str] = []
    notes: list[str] = []
    dependency_codes: list[str] = []
    tasks: list[ContextTriageRef] = []
    bugs: list[ContextTriageRef] = []
    validations: list[ContextValidationRef] = []
    attached_docs: list[ContextDocRef] = []


class MilestoneContextLayer(Struct, kw_only=True):
    code: str
    title: str
    status: str
    goal: str = ""
    success_criteria: list[str] = []
    changes: list[ContextChangeRef] = []
    tasks: list[ContextTriageRef] = []
    bugs: list[ContextTriageRef] = []
    ideas: list[ContextTriageRef] = []


class TaskContextLayer(Struct, kw_only=True):
    code: str
    title: str
    status: str
    body: str = ""
    converted_to_code: str = ""
    linked_change: ContextChangeRef | None = None


class BugContextLayer(Struct, kw_only=True):
    code: str
    title: str
    status: str
    severity: str
    description: str = ""
    repro_notes: list[str] = []
    notes: list[str] = []
    converted_to_code: str = ""


class IdeaContextLayer(Struct, kw_only=True):
    code: str
    title: str
    status: str
    body: str = ""
    converted_to_code: str = ""


class ContextBundle(Struct, kw_only=True):
    target_code: str
    target_type: str
    ancestors: list[ContextAncestor] = []
    document_refs: list[ContextDocRef] = []
    recent_history: list[HistoryEvent] = []
    project: ProjectContextLayer | None = None
    change: ChangeContextLayer | None = None
    milestone: MilestoneContextLayer | None = None
    task: TaskContextLayer | None = None
    bug: BugContextLayer | None = None
    idea: IdeaContextLayer | None = None


class _EntityIndex:
    def __init__(self, entities: Sequence[Entity]) -> None:
        self.projects: dict[int, Project] = {}
        self.changes: dict[int, Change] = {}
        self.milestones: dict[int, Milestone] = {}
        self.facts: list[Fact] = []
        self.validations: list[Validation] = []
        self.tasks: list[Task] = []
        self.bugs: list[Bug] = []
        self.ideas: list[Idea] = []
        for entity in entities:
            if isinstance(entity, Project):
                self.projects[entity.id] = entity
            elif isinstance(entity, Change):
                self.changes[entity.id] = entity
            elif isinstance(entity, Milestone):
                self.milestones[entity.id] = entity
            elif isinstance(entity, Fact):
                self.facts.append(entity)
            elif isinstance(entity, Validation):
                self.validations.append(entity)
            elif isinstance(entity, Task):
                self.tasks.append(entity)
            elif isinstance(entity, Bug):
                self.bugs.append(entity)
            elif isinstance(entity, Idea):
                self.ideas.append(entity)


def assemble_context(
    target: Project | Milestone | Change | Task | Bug | Idea | Fact | Validation,
    *,
    entities: Sequence[Entity],
    dependency_targets: Sequence[DependencyTarget],
    document_refs: Sequence[DocumentRef],
    history: Sequence[HistoryEvent],
) -> ContextBundle:
    if isinstance(target, (Fact, Validation)):
        raise ValueError(f"unsupported context target: {type(target).__name__}")

    index = _EntityIndex(entities)
    target_type = _target_type_for(target)
    owning_project = _owning_project(target, index)
    bundle_docs = _bundle_document_refs(document_refs, owning_project)
    ancestors = _build_ancestors(target, index)
    history_copy = [HistoryEvent(at=e.at, op=e.op, summary=e.summary) for e in history]

    return ContextBundle(
        target_code=target.code,
        target_type=target_type,
        ancestors=ancestors,
        document_refs=bundle_docs,
        recent_history=history_copy,
        project=_project_layer(target, index) if isinstance(target, Project) else None,
        change=_change_layer(target, index, dependency_targets, document_refs)
        if isinstance(target, Change)
        else None,
        milestone=_milestone_layer(target, index) if isinstance(target, Milestone) else None,
        task=_task_layer(target, index) if isinstance(target, Task) else None,
        bug=_bug_layer(target) if isinstance(target, Bug) else None,
        idea=_idea_layer(target) if isinstance(target, Idea) else None,
    )


def _target_type_for(
    target: Project | Milestone | Change | Task | Bug | Idea,
) -> str:
    if isinstance(target, Project):
        return "project"
    if isinstance(target, Change):
        return "change"
    if isinstance(target, Milestone):
        return "milestone"
    if isinstance(target, Task):
        return "task"
    if isinstance(target, Bug):
        return "bug"
    return "idea"


def _owning_project(
    target: Project | Milestone | Change | Task | Bug | Idea, index: _EntityIndex
) -> Project | None:
    if isinstance(target, Project):
        return target
    project_id = target.project_id
    if project_id is None:
        return None
    return index.projects.get(project_id)


def _bundle_document_refs(
    document_refs: Sequence[DocumentRef],
    owning_project: Project | None,
) -> list[ContextDocRef]:
    if owning_project is None:
        return []
    return [
        ContextDocRef(doc_type=ref.doc_type, path=ref.path)
        for ref in document_refs
        if ref.project_id == owning_project.id and ref.change_id is None
    ]


def _build_ancestors(
    target: Project | Milestone | Change | Task | Bug | Idea,
    index: _EntityIndex,
) -> list[ContextAncestor]:
    if isinstance(target, Project):
        return _project_parent_chain(target.parent_id, index)

    owning = _owning_project(target, index)
    if owning is None:
        return []

    chain = _project_parent_chain(owning.parent_id, index)
    chain.append(
        ContextAncestor(code=owning.code, title=owning.title, type="project"),
    )
    return chain


def _project_parent_chain(parent_id: int | None, index: _EntityIndex) -> list[ContextAncestor]:
    collected: list[Project] = []
    pid = parent_id
    while pid is not None:
        project = index.projects.get(pid)
        if project is None:
            break
        collected.append(project)
        pid = project.parent_id
    collected.reverse()
    return [ContextAncestor(code=p.code, title=p.title, type="project") for p in collected]


def _change_ref(change: Change) -> ContextChangeRef:
    return ContextChangeRef(
        code=change.code,
        title=change.title,
        status=change.status.value,
    )


def _triage_ref(item: Task | Bug | Idea) -> ContextTriageRef:
    return ContextTriageRef(code=item.code, title=item.title, status=item.status.value)


def _validation_ref(validation: Validation) -> ContextValidationRef:
    return ContextValidationRef(
        code=validation.code,
        title=validation.title,
        status=validation.status.value,
        scenarios=list(validation.scenarios),
    )


def _is_open_triage(status: TriageStatus) -> bool:
    return status in _OPEN_TRIAGE


def _project_layer(project: Project, index: _EntityIndex) -> ProjectContextLayer:
    milestones = [m for m in index.milestones.values() if m.project_id == project.id]
    milestone_refs: list[ContextMilestoneRef] = []
    for milestone in milestones:
        scheduled = [
            _change_ref(c)
            for c in index.changes.values()
            if c.project_id == project.id and c.milestone_id == milestone.id
        ]
        milestone_refs.append(
            ContextMilestoneRef(
                code=milestone.code,
                title=milestone.title,
                status=milestone.status.value,
                changes=scheduled,
            )
        )

    unscheduled = [
        _change_ref(c)
        for c in index.changes.values()
        if c.project_id == project.id and c.milestone_id is None
    ]

    facts = [
        ContextFactRef(code=f.code, title=f.title, status=f.status.value)
        for f in index.facts
        if f.project_id == project.id and f.status == LifecycleStatus.active
    ]

    tasks = [
        _triage_ref(t)
        for t in index.tasks
        if t.project_id == project.id and _is_open_triage(t.status)
    ]
    bugs = [
        _triage_ref(b)
        for b in index.bugs
        if b.project_id == project.id and _is_open_triage(b.status)
    ]
    ideas = [
        _triage_ref(i)
        for i in index.ideas
        if i.project_id == project.id and _is_open_triage(i.status)
    ]

    validations = [
        _validation_ref(v)
        for v in index.validations
        if v.project_id == project.id and v.status == LifecycleStatus.active
    ]
    superseded_count = sum(
        1
        for v in index.validations
        if v.project_id == project.id and v.status == LifecycleStatus.superseded
    )

    return ProjectContextLayer(
        code=project.code,
        title=project.title,
        status=project.status.value,
        description=project.description,
        milestones=milestone_refs,
        unscheduled_changes=unscheduled,
        facts=facts,
        tasks=tasks,
        bugs=bugs,
        ideas=ideas,
        validations=validations,
        superseded_validation_count=superseded_count,
    )


def _change_layer(
    change: Change,
    index: _EntityIndex,
    dependency_targets: Sequence[DependencyTarget],
    document_refs: Sequence[DocumentRef],
) -> ChangeContextLayer:
    dependency_codes = [_dependency_code(t) for t in dependency_targets]
    tasks = [
        _triage_ref(t)
        for t in index.tasks
        if t.change_id == change.id and _is_open_triage(t.status)
    ]
    bugs = [
        _triage_ref(b) for b in index.bugs if b.change_id == change.id and _is_open_triage(b.status)
    ]
    validations = [
        _validation_ref(v)
        for v in index.validations
        if v.change_id == change.id and v.status == LifecycleStatus.active
    ]
    attached = [
        ContextDocRef(doc_type=ref.doc_type, path=ref.path)
        for ref in document_refs
        if ref.change_id == change.id
    ]
    return ChangeContextLayer(
        code=change.code,
        title=change.title,
        status=change.status.value,
        type=change.type.value,
        goal=change.goal,
        deliverables=list(change.deliverables),
        notes=list(change.notes),
        dependency_codes=dependency_codes,
        tasks=tasks,
        bugs=bugs,
        validations=validations,
        attached_docs=attached,
    )


def _dependency_code(target: DependencyTarget) -> str:
    return target.code


def _milestone_layer(milestone: Milestone, index: _EntityIndex) -> MilestoneContextLayer:
    scheduled = [_change_ref(c) for c in index.changes.values() if c.milestone_id == milestone.id]
    tasks = [
        _triage_ref(t)
        for t in index.tasks
        if t.milestone_id == milestone.id and _is_open_triage(t.status)
    ]
    bugs = [
        _triage_ref(b)
        for b in index.bugs
        if b.milestone_id == milestone.id and _is_open_triage(b.status)
    ]
    ideas = [
        _triage_ref(i)
        for i in index.ideas
        if i.milestone_id == milestone.id and _is_open_triage(i.status)
    ]
    return MilestoneContextLayer(
        code=milestone.code,
        title=milestone.title,
        status=milestone.status.value,
        goal=milestone.goal,
        success_criteria=list(milestone.success_criteria),
        changes=scheduled,
        tasks=tasks,
        bugs=bugs,
        ideas=ideas,
    )


def _task_layer(task: Task, index: _EntityIndex) -> TaskContextLayer:
    linked: ContextChangeRef | None = None
    if task.change_id is not None:
        change = index.changes.get(task.change_id)
        if change is not None:
            linked = _change_ref(change)
    return TaskContextLayer(
        code=task.code,
        title=task.title,
        status=task.status.value,
        body=task.body,
        converted_to_code=task.converted_to_code,
        linked_change=linked,
    )


def _bug_layer(bug: Bug) -> BugContextLayer:
    return BugContextLayer(
        code=bug.code,
        title=bug.title,
        status=bug.status.value,
        severity=bug.severity.value,
        description=bug.description,
        repro_notes=list(bug.repro_notes),
        notes=list(bug.notes),
        converted_to_code=bug.converted_to_code,
    )


def _idea_layer(idea: Idea) -> IdeaContextLayer:
    return IdeaContextLayer(
        code=idea.code,
        title=idea.title,
        status=idea.status.value,
        body=idea.body,
        converted_to_code=idea.converted_to_code,
    )
