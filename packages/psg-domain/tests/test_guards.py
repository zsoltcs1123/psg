import pytest

from psg_domain.entities import (
    Bug,
    Change,
    ChangeType,
    Fact,
    Idea,
    LifecycleStatus,
    Milestone,
    Project,
    ProjectStatus,
    Task,
    TriageStatus,
    WorkflowStatus,
)
from psg_domain.errors import BlockedByDependencyError, MilestoneIncompleteError
from psg_domain.workflow import assert_dependencies_clear, assert_milestone_completeable

_WS = 1


@pytest.mark.unit
def test_empty_dependency_list_passes() -> None:
    assert_dependencies_clear([])


@pytest.mark.unit
def test_project_in_progress_clears_dependency() -> None:
    project = Project(workspace_id=_WS, code="app", status=ProjectStatus.in_progress)
    assert_dependencies_clear([project])


@pytest.mark.unit
def test_change_done_clears_dependency() -> None:
    change = Change(
        workspace_id=_WS,
        code="app-C1",
        type=ChangeType.new_feature,
        status=WorkflowStatus.done,
    )
    assert_dependencies_clear([change])


@pytest.mark.unit
def test_task_wontfix_clears_dependency() -> None:
    task = Task(workspace_id=_WS, code="app-T1", status=TriageStatus.wontfix)
    assert_dependencies_clear([task])


@pytest.mark.unit
def test_lifecycle_status_never_blocks() -> None:
    fact = Fact(workspace_id=_WS, code="app-F1", status=LifecycleStatus.active)
    assert_dependencies_clear([fact])
    superseded = Fact(workspace_id=_WS, code="app-F2", status=LifecycleStatus.superseded)
    assert_dependencies_clear([superseded])


@pytest.mark.unit
def test_uncleared_targets_block_with_sorted_codes() -> None:
    project = Project(workspace_id=_WS, code="z-proj", status=ProjectStatus.pending)
    change = Change(
        workspace_id=_WS,
        code="a-C1",
        type=ChangeType.refactor,
        status=WorkflowStatus.pending,
    )
    task = Task(workspace_id=_WS, code="m-T1", status=TriageStatus.pending)
    with pytest.raises(BlockedByDependencyError) as exc_info:
        assert_dependencies_clear([project, change, task])
    assert exc_info.value.blocking_codes == ["a-C1", "m-T1", "z-proj"]


@pytest.mark.unit
def test_milestone_in_progress_with_empty_deps_passes() -> None:
    assert_dependencies_clear([])


@pytest.mark.unit
def test_milestone_complete_when_all_scheduled_members_terminal() -> None:
    milestone = Milestone(workspace_id=_WS, code="app-MS1")
    change = Change(
        workspace_id=_WS,
        code="app-C1",
        type=ChangeType.new_feature,
        status=WorkflowStatus.done,
    )
    task = Task(workspace_id=_WS, code="app-T1", status=TriageStatus.converted)
    bug = Bug(workspace_id=_WS, code="app-B1", status=TriageStatus.wontfix)
    idea = Idea(workspace_id=_WS, code="app-I1", status=TriageStatus.done)
    assert_milestone_completeable(milestone, [change], [task], [bug], [idea])


@pytest.mark.unit
def test_milestone_incomplete_when_change_not_done() -> None:
    milestone = Milestone(workspace_id=_WS, code="app-MS1")
    change = Change(
        workspace_id=_WS,
        code="app-C1",
        type=ChangeType.new_feature,
        status=WorkflowStatus.in_progress,
    )
    with pytest.raises(MilestoneIncompleteError) as exc_info:
        assert_milestone_completeable(milestone, [change], [], [], [])
    assert exc_info.value.milestone_code == "app-MS1"
    assert exc_info.value.blocking_codes == ["app-C1"]


@pytest.mark.unit
def test_milestone_incomplete_when_pending_triage_members() -> None:
    milestone = Milestone(workspace_id=_WS, code="app-MS1")
    change = Change(
        workspace_id=_WS,
        code="app-C1",
        type=ChangeType.new_feature,
        status=WorkflowStatus.pending,
    )
    task = Task(workspace_id=_WS, code="app-T1", status=TriageStatus.pending)
    bug = Bug(workspace_id=_WS, code="app-B1", status=TriageStatus.pending)
    idea = Idea(workspace_id=_WS, code="app-I1", status=TriageStatus.pending)
    with pytest.raises(MilestoneIncompleteError) as exc_info:
        assert_milestone_completeable(milestone, [change], [task], [bug], [idea])
    assert exc_info.value.blocking_codes == ["app-B1", "app-C1", "app-I1", "app-T1"]
