import pytest
from psg_domain.entities import (
    Change,
    ChangeKind,
    Fact,
    LifecycleStatus,
    Milestone,
    Project,
    ProjectStatus,
    StatusOwning,
    Task,
    TriageStatus,
    WorkflowStatus,
)
from psg_domain.errors import InvalidTransitionError
from psg_domain.workflow import StatusValue, transition

_WS = 1


@pytest.mark.unit
@pytest.mark.parametrize(
    ("current", "requested"),
    [
        (WorkflowStatus.pending, WorkflowStatus.in_progress),
        (WorkflowStatus.in_progress, WorkflowStatus.done),
        (ProjectStatus.pending, ProjectStatus.in_progress),
        (ProjectStatus.pending, ProjectStatus.obsolete),
        (ProjectStatus.in_progress, ProjectStatus.obsolete),
        (LifecycleStatus.active, LifecycleStatus.superseded),
        (TriageStatus.open, TriageStatus.done),
        (TriageStatus.open, TriageStatus.wontfix),
        (TriageStatus.open, TriageStatus.converted),
    ],
)
def test_legal_transition(current: StatusValue, requested: StatusValue) -> None:
    entity = _entity_for_status(current)
    result = transition(entity, requested)
    assert result.status is requested
    assert result is not entity


@pytest.mark.unit
@pytest.mark.parametrize(
    "terminal",
    [
        TriageStatus.done,
        TriageStatus.wontfix,
        TriageStatus.converted,
    ],
)
def test_triage_terminal_stays_terminal(terminal: TriageStatus) -> None:
    task = Task(workspace_id=_WS, code="app-T1", status=terminal)
    assert transition(task, terminal) is task


@pytest.mark.unit
@pytest.mark.parametrize(
    ("current", "requested"),
    [
        (WorkflowStatus.pending, WorkflowStatus.done),
        (WorkflowStatus.in_progress, WorkflowStatus.pending),
        (ProjectStatus.in_progress, ProjectStatus.pending),
    ],
)
def test_skipped_or_reverse_transition_rejected(
    current: StatusValue, requested: StatusValue
) -> None:
    entity = _entity_for_status(current)
    with pytest.raises(InvalidTransitionError) as exc_info:
        transition(entity, requested)
    err = exc_info.value
    assert err.allowed


@pytest.mark.unit
@pytest.mark.parametrize(
    ("current", "requested"),
    [
        (WorkflowStatus.done, WorkflowStatus.pending),
        (ProjectStatus.obsolete, ProjectStatus.pending),
        (TriageStatus.converted, TriageStatus.open),
    ],
)
def test_terminal_to_anything_rejected(current: StatusValue, requested: StatusValue) -> None:
    entity = _entity_for_status(current)
    with pytest.raises(InvalidTransitionError):
        transition(entity, requested)


@pytest.mark.unit
def test_wrong_status_family_has_empty_allowed() -> None:
    change = Change(
        workspace_id=_WS,
        code="app-C1",
        kind=ChangeKind.new_feature,
        status=WorkflowStatus.pending,
    )
    with pytest.raises(InvalidTransitionError) as exc_info:
        transition(change, ProjectStatus.in_progress)
    assert exc_info.value.allowed == []


@pytest.mark.unit
def test_same_status_returns_unchanged_entity() -> None:
    milestone = Milestone(
        workspace_id=_WS,
        code="app-MS1",
        status=WorkflowStatus.in_progress,
    )
    assert transition(milestone, WorkflowStatus.in_progress) is milestone


@pytest.mark.unit
def test_invalid_transition_error_fields_on_illegal_step() -> None:
    project = Project(workspace_id=_WS, code="app", status=ProjectStatus.in_progress)
    with pytest.raises(InvalidTransitionError) as exc_info:
        transition(project, ProjectStatus.pending)
    err = exc_info.value
    assert err.current == "in_progress"
    assert err.requested == "pending"
    assert err.allowed == ["obsolete"]


def _entity_for_status(status: StatusValue) -> StatusOwning:
    if isinstance(status, WorkflowStatus):
        return Change(
            workspace_id=_WS,
            code="app-C1",
            kind=ChangeKind.new_feature,
            status=status,
        )
    if isinstance(status, ProjectStatus):
        return Project(workspace_id=_WS, code="app", status=status)
    if isinstance(status, LifecycleStatus):
        return Fact(workspace_id=_WS, code="app-F1", status=status)
    return Task(workspace_id=_WS, code="app-T1", status=status)
