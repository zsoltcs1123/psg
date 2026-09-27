from collections.abc import Sequence

import msgspec.structs

from psg_domain.entities import (
    Bug,
    Change,
    DependencyTarget,
    Entity,
    Idea,
    LifecycleStatus,
    Milestone,
    ProjectStatus,
    Task,
    TriageStatus,
    WorkflowStatus,
)
from psg_domain.errors import (
    BlockedByDependencyError,
    InvalidTransitionError,
    MilestoneIncompleteError,
)

VALID_WORKFLOW_TRANSITIONS: dict[WorkflowStatus, list[WorkflowStatus]] = {
    WorkflowStatus.pending: [WorkflowStatus.in_progress],
    WorkflowStatus.in_progress: [WorkflowStatus.done],
    WorkflowStatus.done: [],
}

VALID_PROJECT_STATUS_TRANSITIONS: dict[ProjectStatus, list[ProjectStatus]] = {
    ProjectStatus.pending: [ProjectStatus.in_progress, ProjectStatus.obsolete],
    ProjectStatus.in_progress: [ProjectStatus.obsolete],
    ProjectStatus.obsolete: [],
}

VALID_LIFECYCLE_TRANSITIONS: dict[LifecycleStatus, list[LifecycleStatus]] = {
    LifecycleStatus.active: [LifecycleStatus.superseded],
    LifecycleStatus.superseded: [],
}

VALID_TRIAGE_TRANSITIONS: dict[TriageStatus, list[TriageStatus]] = {
    TriageStatus.pending: [
        TriageStatus.in_progress,
        TriageStatus.done,
        TriageStatus.wontfix,
        TriageStatus.converted,
    ],
    TriageStatus.in_progress: [
        TriageStatus.done,
        TriageStatus.wontfix,
        TriageStatus.converted,
    ],
    TriageStatus.done: [],
    TriageStatus.wontfix: [],
    TriageStatus.converted: [],
}

_RESOLVED_TRIAGE: frozenset[TriageStatus] = frozenset(
    {TriageStatus.done, TriageStatus.wontfix, TriageStatus.converted}
)

StatusValue = WorkflowStatus | ProjectStatus | LifecycleStatus | TriageStatus


def _status_value(status: StatusValue) -> str:
    return status.value


def _allowed_transitions(current: StatusValue) -> Sequence[StatusValue]:
    if isinstance(current, WorkflowStatus):
        return VALID_WORKFLOW_TRANSITIONS[current]
    if isinstance(current, ProjectStatus):
        return VALID_PROJECT_STATUS_TRANSITIONS[current]
    if isinstance(current, LifecycleStatus):
        return VALID_LIFECYCLE_TRANSITIONS[current]
    return VALID_TRIAGE_TRANSITIONS[current]


def transition[E: Entity](entity: E, new_status: StatusValue) -> E:
    current = entity.status
    if type(new_status) is not type(current):
        raise InvalidTransitionError(
            _status_value(current),
            _status_value(new_status),
            [],
        )
    if new_status == current:
        return entity
    allowed = _allowed_transitions(current)
    if new_status not in allowed:
        raise InvalidTransitionError(
            _status_value(current),
            _status_value(new_status),
            [_status_value(s) for s in allowed],
        )
    return msgspec.structs.replace(entity, status=new_status)


def _is_dependency_cleared(target: DependencyTarget) -> bool:
    status = target.status
    if isinstance(status, WorkflowStatus):
        return status is WorkflowStatus.done
    if isinstance(status, ProjectStatus):
        return status in (ProjectStatus.in_progress, ProjectStatus.obsolete)
    if isinstance(status, TriageStatus):
        return status in _RESOLVED_TRIAGE
    return isinstance(status, LifecycleStatus)


def assert_dependencies_clear(targets: Sequence[DependencyTarget]) -> None:
    blocking = [target.code for target in targets if not _is_dependency_cleared(target)]
    if blocking:
        raise BlockedByDependencyError(sorted(blocking))


def _is_change_complete(change: Change) -> bool:
    return change.status is WorkflowStatus.done


def _is_resolved_triage(item: Task | Bug | Idea) -> bool:
    return item.status in _RESOLVED_TRIAGE


def assert_milestone_completeable(
    milestone: Milestone,
    scheduled_changes: Sequence[Change],
    scheduled_tasks: Sequence[Task],
    scheduled_bugs: Sequence[Bug],
    scheduled_ideas: Sequence[Idea],
) -> None:
    blocking: list[str] = []
    for change in scheduled_changes:
        if not _is_change_complete(change):
            blocking.append(change.code)
    for task in scheduled_tasks:
        if not _is_resolved_triage(task):
            blocking.append(task.code)
    for bug in scheduled_bugs:
        if not _is_resolved_triage(bug):
            blocking.append(bug.code)
    for idea in scheduled_ideas:
        if not _is_resolved_triage(idea):
            blocking.append(idea.code)
    if blocking:
        raise MilestoneIncompleteError(milestone.code, sorted(blocking))
