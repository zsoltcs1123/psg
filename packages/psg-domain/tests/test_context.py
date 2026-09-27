import pytest

from psg_domain.context import HistoryEvent, assemble_context
from psg_domain.entities import (
    Bug,
    Change,
    ChangeType,
    DocumentRef,
    Entity,
    Idea,
    Milestone,
    Project,
    Task,
    TriageStatus,
)


def _workspace_entities() -> list[Entity]:
    project = Project(id=1, workspace_id=1, code="app", title="App")
    milestone = Milestone(
        id=10,
        workspace_id=1,
        code="app-MS1",
        title="M1",
        project_id=1,
    )
    change = Change(
        id=20,
        workspace_id=1,
        code="app-C1",
        title="C1",
        type=ChangeType.new_feature,
        project_id=1,
        milestone_id=10,
    )
    task = Task(id=30, workspace_id=1, code="app-T1", title="T1", project_id=1)
    bug = Bug(id=40, workspace_id=1, code="app-B1", title="B1", project_id=1)
    idea = Idea(id=50, workspace_id=1, code="app-I1", title="I1", project_id=1)
    return [project, milestone, change, task, bug, idea]


@pytest.mark.unit
def test_assemble_context_project_target_sets_project_layer_only() -> None:
    entities = _workspace_entities()
    project = entities[0]
    bundle = assemble_context(
        project,
        entities=entities,
        dependency_targets=[],
        document_refs=[],
        history=[],
    )
    assert bundle.target_code == "app"
    assert bundle.target_type == "project"
    assert bundle.project is not None
    assert bundle.change is None
    assert bundle.milestone is None
    assert bundle.task is None
    assert bundle.bug is None
    assert bundle.idea is None


@pytest.mark.unit
def test_assemble_context_change_target_sets_change_layer_only() -> None:
    entities = _workspace_entities()
    change = entities[2]
    bundle = assemble_context(
        change,
        entities=entities,
        dependency_targets=[],
        document_refs=[],
        history=[],
    )
    assert bundle.target_code == "app-C1"
    assert bundle.target_type == "change"
    assert bundle.change is not None
    assert bundle.project is None


@pytest.mark.unit
def test_assemble_context_milestone_target_sets_milestone_layer_only() -> None:
    entities = _workspace_entities()
    milestone = entities[1]
    bundle = assemble_context(
        milestone,
        entities=entities,
        dependency_targets=[],
        document_refs=[],
        history=[],
    )
    assert bundle.target_code == "app-MS1"
    assert bundle.target_type == "milestone"
    assert bundle.milestone is not None
    assert bundle.project is None


@pytest.mark.unit
def test_assemble_context_task_target_sets_task_layer_only() -> None:
    entities = _workspace_entities()
    task = entities[3]
    bundle = assemble_context(
        task,
        entities=entities,
        dependency_targets=[],
        document_refs=[],
        history=[],
    )
    assert bundle.target_code == "app-T1"
    assert bundle.target_type == "task"
    assert bundle.task is not None
    assert bundle.change is None


@pytest.mark.unit
def test_assemble_context_bug_target_sets_bug_layer_only() -> None:
    entities = _workspace_entities()
    bug = entities[4]
    bundle = assemble_context(
        bug,
        entities=entities,
        dependency_targets=[],
        document_refs=[],
        history=[],
    )
    assert bundle.target_code == "app-B1"
    assert bundle.target_type == "bug"
    assert bundle.bug is not None
    assert bundle.project is None


@pytest.mark.unit
def test_assemble_context_idea_target_sets_idea_layer_only() -> None:
    entities = _workspace_entities()
    idea = entities[5]
    bundle = assemble_context(
        idea,
        entities=entities,
        dependency_targets=[],
        document_refs=[],
        history=[],
    )
    assert bundle.target_code == "app-I1"
    assert bundle.target_type == "idea"
    assert bundle.idea is not None
    assert bundle.project is None


@pytest.mark.unit
def test_project_layer_lists_only_open_tasks() -> None:
    project = Project(id=1, workspace_id=1, code="app", title="App")
    pending = Task(
        id=2,
        workspace_id=1,
        code="app-T1",
        title="Open",
        project_id=1,
        status=TriageStatus.pending,
    )
    done = Task(
        id=3,
        workspace_id=1,
        code="app-T2",
        title="Closed",
        project_id=1,
        status=TriageStatus.done,
    )
    bundle = assemble_context(
        project,
        entities=[project, pending, done],
        dependency_targets=[],
        document_refs=[],
        history=[],
    )
    assert bundle.project is not None
    assert [t.code for t in bundle.project.tasks] == ["app-T1"]


@pytest.mark.unit
def test_document_refs_split_between_bundle_and_change_attached_docs() -> None:
    project = Project(id=1, workspace_id=1, code="app")
    change = Change(
        id=2,
        workspace_id=1,
        code="app-C1",
        type=ChangeType.new_feature,
        project_id=1,
    )
    project_ref = DocumentRef(
        doc_type="readme",
        path="README.md",
        project_id=1,
        change_id=None,
    )
    change_ref = DocumentRef(
        doc_type="spec",
        path="docs/spec.md",
        project_id=1,
        change_id=2,
    )
    bundle = assemble_context(
        change,
        entities=[project, change],
        dependency_targets=[],
        document_refs=[project_ref, change_ref],
        history=[],
    )
    assert len(bundle.document_refs) == 1
    assert bundle.document_refs[0].doc_type == "readme"
    assert bundle.document_refs[0].path == "README.md"
    assert bundle.change is not None
    assert len(bundle.change.attached_docs) == 1
    assert bundle.change.attached_docs[0].doc_type == "spec"
    assert bundle.change.attached_docs[0].path == "docs/spec.md"


@pytest.mark.unit
def test_change_layer_dependency_open_task_and_omits_done_task() -> None:
    project = Project(id=1, workspace_id=1, code="app")
    dep = Project(id=99, workspace_id=1, code="lib", title="Lib")
    change = Change(
        id=2,
        workspace_id=1,
        code="app-C1",
        type=ChangeType.new_feature,
        project_id=1,
    )
    open_task = Task(
        id=3,
        workspace_id=1,
        code="app-T1",
        title="Work",
        change_id=2,
        status=TriageStatus.in_progress,
    )
    done_task = Task(
        id=4,
        workspace_id=1,
        code="app-T2",
        title="Done",
        change_id=2,
        status=TriageStatus.done,
    )
    bundle = assemble_context(
        change,
        entities=[project, change, open_task, done_task],
        dependency_targets=[dep],
        document_refs=[],
        history=[],
    )
    assert bundle.change is not None
    assert bundle.change.dependency_codes == ["lib"]
    assert [t.code for t in bundle.change.tasks] == ["app-T1"]


@pytest.mark.unit
def test_recent_history_copied_onto_bundle() -> None:
    project = Project(id=1, workspace_id=1, code="app")
    event = HistoryEvent(at="2026-01-01", op="create", summary="created")
    bundle = assemble_context(
        project,
        entities=[project],
        dependency_targets=[],
        document_refs=[],
        history=[event],
    )
    assert len(bundle.recent_history) == 1
    assert bundle.recent_history[0].at == "2026-01-01"
    assert bundle.recent_history[0].op == "create"
    assert bundle.recent_history[0].summary == "created"
