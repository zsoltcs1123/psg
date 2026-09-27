from collections.abc import Sequence
from typing import Literal

from msgspec import Struct

from psg_domain.entities import (
    Bug,
    Change,
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
    WorkflowStatus,
)

EntityKind = Literal[
    "projects",
    "milestones",
    "changes",
    "facts",
    "validations",
    "tasks",
    "bugs",
    "ideas",
]

_OPEN_WORKFLOW = frozenset({WorkflowStatus.pending, WorkflowStatus.in_progress})
_OPEN_TRIAGE = frozenset({TriageStatus.pending, TriageStatus.in_progress})


class DependencyEdge(Struct, kw_only=True):
    dependent_id: int
    dependency_id: int


class OpenTotal(Struct, kw_only=True):
    open: int
    total: int


class ChildProjectRef(Struct, kw_only=True):
    code: str
    title: str
    status: str


class MilestoneListItem(Struct, kw_only=True):
    code: str
    title: str
    status: str


class ProjectOverview(Struct, kw_only=True):
    changes: OpenTotal
    milestones: OpenTotal
    tasks: OpenTotal
    bugs: OpenTotal
    ideas: OpenTotal
    facts: int
    validations: int
    document_refs: int
    child_projects: list[ChildProjectRef]
    milestones_list: list[MilestoneListItem]


class DetailSection(Struct, kw_only=True):
    label: str
    lines: list[str]


class DependencyRef(Struct, kw_only=True):
    code: str
    title: str


class EntityDetail(Struct, kw_only=True):
    code: str
    title: str
    type: str
    status: str
    sections: list[DetailSection]
    dependencies: list[DependencyRef]
    required_by: list[DependencyRef]


class EntityListItem(Struct, kw_only=True):
    code: str
    title: str
    status: str


class EntityListGroup(Struct, kw_only=True):
    parent_code: str
    parent_title: str
    items: list[EntityListItem]


class EntityList(Struct, kw_only=True):
    groups: list[EntityListGroup]


class ChangeOrderItem(Struct, kw_only=True):
    code: str
    title: str
    status: str


class ChangeOrder(Struct, kw_only=True):
    has_cycle: bool
    changes: list[ChangeOrderItem]


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

    def resolve(self, entity_id: int) -> Entity | None:
        if entity_id in self.projects:
            return self.projects[entity_id]
        if entity_id in self.changes:
            return self.changes[entity_id]
        if entity_id in self.milestones:
            return self.milestones[entity_id]
        for collection in (
            self.facts,
            self.validations,
            self.tasks,
            self.bugs,
            self.ideas,
        ):
            for item in collection:
                if item.id == entity_id:
                    return item
        return None


def project_overview(
    project: Project,
    *,
    entities: Sequence[Entity],
    document_refs: Sequence[DocumentRef],
) -> ProjectOverview:
    index = _EntityIndex(entities)
    subtree_ids = _subtree_project_ids(project.id, index.projects)

    subtree_changes = [c for c in index.changes.values() if c.project_id in subtree_ids]
    subtree_milestones = [m for m in index.milestones.values() if m.project_id in subtree_ids]
    subtree_tasks = [t for t in index.tasks if t.project_id in subtree_ids]
    subtree_bugs = [b for b in index.bugs if b.project_id in subtree_ids]
    subtree_ideas = [i for i in index.ideas if i.project_id in subtree_ids]
    subtree_facts = [f for f in index.facts if f.project_id in subtree_ids]
    subtree_validations = [v for v in index.validations if v.project_id in subtree_ids]
    subtree_docs = [ref for ref in document_refs if ref.project_id in subtree_ids]

    child_projects = sorted(
        [
            ChildProjectRef(code=p.code, title=p.title, status=p.status.value)
            for p in index.projects.values()
            if p.parent_id == project.id
        ],
        key=lambda r: r.code,
    )
    milestones_list = sorted(
        [
            MilestoneListItem(code=m.code, title=m.title, status=m.status.value)
            for m in index.milestones.values()
            if m.project_id == project.id
        ],
        key=lambda r: r.code,
    )

    return ProjectOverview(
        changes=_workflow_open_total(subtree_changes),
        milestones=_workflow_open_total(subtree_milestones),
        tasks=_triage_open_total(subtree_tasks),
        bugs=_triage_open_total(subtree_bugs),
        ideas=_triage_open_total(subtree_ideas),
        facts=sum(1 for f in subtree_facts if f.status == LifecycleStatus.active),
        validations=sum(1 for v in subtree_validations if v.status == LifecycleStatus.active),
        document_refs=len(subtree_docs),
        child_projects=child_projects,
        milestones_list=milestones_list,
    )


def entity_detail(
    entity: Entity,
    *,
    entities: Sequence[Entity],
    edges: Sequence[DependencyEdge],
) -> EntityDetail:
    index = _EntityIndex(entities)
    entity_type = _entity_type(entity)
    status = _entity_status_value(entity)
    sections = _detail_sections(entity)
    entity_ids = _entity_id_set(index)
    dependencies = _resolve_dependency_refs(
        edges,
        entity_id=entity.id,
        match="dependent",
        index=index,
        entity_ids=entity_ids,
    )
    required_by = _resolve_dependency_refs(
        edges,
        entity_id=entity.id,
        match="dependency",
        index=index,
        entity_ids=entity_ids,
    )
    return EntityDetail(
        code=entity.code,
        title=entity.title,
        type=entity_type,
        status=status,
        sections=sections,
        dependencies=dependencies,
        required_by=required_by,
    )


def list_entities(
    kind: EntityKind,
    entities: Sequence[Entity],
    *,
    parent_code: str | None = None,
) -> EntityList:
    index = _EntityIndex(entities)
    groups = _build_list_groups(kind, index)
    if parent_code is not None:
        groups = [g for g in groups if g.parent_code == parent_code]
    return EntityList(groups=groups)


def order_changes(
    changes: Sequence[Change],
    *,
    edges: Sequence[DependencyEdge],
) -> ChangeOrder:
    if not changes:
        return ChangeOrder(has_cycle=False, changes=[])

    change_by_id = {change.id: change for change in changes}
    change_ids = set(change_by_id)
    relevant = [
        edge
        for edge in edges
        if edge.dependent_id in change_ids and edge.dependency_id in change_ids
    ]

    in_degree = dict.fromkeys(change_ids, 0)
    successors: dict[int, list[int]] = {change_id: [] for change_id in change_ids}
    for edge in relevant:
        successors[edge.dependency_id].append(edge.dependent_id)
        in_degree[edge.dependent_id] += 1

    ready = sorted(
        [change_id for change_id in change_ids if in_degree[change_id] == 0],
        key=lambda change_id: change_by_id[change_id].code,
    )
    ordered_ids: list[int] = []
    while ready:
        current_id = ready.pop(0)
        ordered_ids.append(current_id)
        for successor_id in successors[current_id]:
            in_degree[successor_id] -= 1
            if in_degree[successor_id] == 0:
                ready.append(successor_id)
        ready.sort(key=lambda change_id: change_by_id[change_id].code)

    if len(ordered_ids) != len(change_ids):
        input_order = [
            ChangeOrderItem(
                code=change.code,
                title=change.title,
                status=change.status.value,
            )
            for change in changes
        ]
        return ChangeOrder(has_cycle=True, changes=input_order)

    return ChangeOrder(
        has_cycle=False,
        changes=[
            ChangeOrderItem(
                code=change_by_id[change_id].code,
                title=change_by_id[change_id].title,
                status=change_by_id[change_id].status.value,
            )
            for change_id in ordered_ids
        ],
    )


def _subtree_project_ids(root_id: int, projects: dict[int, Project]) -> set[int]:
    ids: set[int] = {root_id}
    queue = [root_id]
    while queue:
        parent_id = queue.pop()
        for project in projects.values():
            if project.parent_id == parent_id and project.id not in ids:
                ids.add(project.id)
                queue.append(project.id)
    return ids


def _workflow_open_total(items: Sequence[Change | Milestone]) -> OpenTotal:
    total = len(items)
    open_count = sum(1 for item in items if item.status in _OPEN_WORKFLOW)
    return OpenTotal(open=open_count, total=total)


def _triage_open_total(items: Sequence[Task | Bug | Idea]) -> OpenTotal:
    total = len(items)
    open_count = sum(1 for item in items if item.status in _OPEN_TRIAGE)
    return OpenTotal(open=open_count, total=total)


def _entity_type(entity: Entity) -> str:
    if isinstance(entity, Project):
        return "project"
    if isinstance(entity, Milestone):
        return "milestone"
    if isinstance(entity, Change):
        return "change"
    if isinstance(entity, Fact):
        return "fact"
    if isinstance(entity, Validation):
        return "validation"
    if isinstance(entity, Task):
        return "task"
    if isinstance(entity, Bug):
        return "bug"
    return "idea"


def _entity_status_value(entity: Entity) -> str:
    return entity.status.value


def _detail_sections(entity: Entity) -> list[DetailSection]:
    sections: list[DetailSection] = []
    if isinstance(entity, Project):
        _append_string_section(sections, "description", entity.description)
    elif isinstance(entity, Milestone):
        _append_string_section(sections, "goal", entity.goal)
        _append_lines_section(sections, "success criteria", entity.success_criteria)
    elif isinstance(entity, Change):
        _append_string_section(sections, "goal", entity.goal)
        _append_lines_section(sections, "deliverables", entity.deliverables)
        _append_lines_section(sections, "notes", entity.notes)
    elif isinstance(entity, Fact):
        _append_string_section(sections, "body", entity.body)
    elif isinstance(entity, Validation):
        _append_lines_section(sections, "scenarios", entity.scenarios)
        _append_lines_section(sections, "coverage", entity.coverage)
    elif isinstance(entity, Task):
        _append_string_section(sections, "body", entity.body)
    elif isinstance(entity, Bug):
        _append_string_section(sections, "description", entity.description)
        _append_lines_section(sections, "repro notes", entity.repro_notes)
        _append_lines_section(sections, "notes", entity.notes)
    elif isinstance(entity, Idea):
        _append_string_section(sections, "body", entity.body)
    return sections


def _append_string_section(
    sections: list[DetailSection],
    label: str,
    text: str,
) -> None:
    if text:
        sections.append(DetailSection(label=label, lines=[text]))


def _append_lines_section(
    sections: list[DetailSection],
    label: str,
    lines: Sequence[str],
) -> None:
    if lines:
        sections.append(DetailSection(label=label, lines=list(lines)))


def _entity_id_set(index: _EntityIndex) -> set[int]:
    ids: set[int] = set(index.projects) | set(index.changes) | set(index.milestones)
    for collection in (
        index.facts,
        index.validations,
        index.tasks,
        index.bugs,
        index.ideas,
    ):
        for item in collection:
            ids.add(item.id)
    return ids


def _resolve_dependency_refs(
    edges: Sequence[DependencyEdge],
    *,
    entity_id: int,
    match: Literal["dependent", "dependency"],
    index: _EntityIndex,
    entity_ids: set[int],
) -> list[DependencyRef]:
    refs: list[DependencyRef] = []
    for edge in edges:
        if match == "dependent" and edge.dependent_id != entity_id:
            continue
        if match == "dependency" and edge.dependency_id != entity_id:
            continue
        other_id = edge.dependency_id if match == "dependent" else edge.dependent_id
        if other_id not in entity_ids:
            continue
        other = index.resolve(other_id)
        if other is None:
            continue
        refs.append(DependencyRef(code=other.code, title=other.title))
    refs.sort(key=lambda ref: ref.code)
    return refs


def _build_list_groups(kind: EntityKind, index: _EntityIndex) -> list[EntityListGroup]:
    if kind == "projects":
        return _project_list_groups(index)
    if kind == "milestones":
        return _scoped_list_groups(list(index.milestones.values()), index)
    if kind == "changes":
        return _scoped_list_groups(list(index.changes.values()), index)
    if kind == "facts":
        return _scoped_list_groups(index.facts, index)
    if kind == "validations":
        return _scoped_list_groups(index.validations, index)
    if kind == "tasks":
        return _scoped_list_groups(index.tasks, index)
    if kind == "bugs":
        return _scoped_list_groups(index.bugs, index)
    return _scoped_list_groups(index.ideas, index)


def _project_list_groups(index: _EntityIndex) -> list[EntityListGroup]:
    by_parent: dict[int | None, list[Project]] = {}
    for project in index.projects.values():
        by_parent.setdefault(project.parent_id, []).append(project)

    groups: list[EntityListGroup] = []
    for parent_id, projects in by_parent.items():
        parent_code, parent_title = _parent_labels(parent_id, index)
        items = sorted(
            [
                EntityListItem(
                    code=project.code,
                    title=project.title,
                    status=project.status.value,
                )
                for project in projects
            ],
            key=lambda item: item.code,
        )
        groups.append(
            EntityListGroup(parent_code=parent_code, parent_title=parent_title, items=items)
        )
    groups.sort(key=lambda group: group.parent_code)
    return groups


def _scoped_list_groups(
    items: Sequence[Milestone | Change | Fact | Validation | Task | Bug | Idea],
    index: _EntityIndex,
) -> list[EntityListGroup]:
    by_project: dict[
        int | None,
        list[Milestone | Change | Fact | Validation | Task | Bug | Idea],
    ] = {}
    for item in items:
        by_project.setdefault(item.project_id, []).append(item)

    groups: list[EntityListGroup] = []
    for project_id, group_items in by_project.items():
        parent_code, parent_title = _parent_labels(project_id, index)
        list_items = sorted(
            [
                EntityListItem(
                    code=item.code,
                    title=item.title,
                    status=item.status.value,
                )
                for item in group_items
            ],
            key=lambda list_item: list_item.code,
        )
        groups.append(
            EntityListGroup(
                parent_code=parent_code,
                parent_title=parent_title,
                items=list_items,
            )
        )
    groups.sort(key=lambda group: group.parent_code)
    return groups


def _parent_labels(parent_id: int | None, index: _EntityIndex) -> tuple[str, str]:
    if parent_id is None:
        return "", ""
    parent = index.projects.get(parent_id)
    if parent is None:
        return "", ""
    return parent.code, parent.title
