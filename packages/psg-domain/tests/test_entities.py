import pytest
from psg_domain.entities import (
    Bug,
    BugSeverity,
    Change,
    ChangeKind,
    DocumentRef,
    Fact,
    Idea,
    LifecycleStatus,
    Milestone,
    Project,
    ProjectStatus,
    Task,
    TriageStatus,
    Validation,
    ValidationScenario,
    WorkflowStatus,
)


@pytest.mark.unit
def test_project_defaults() -> None:
    project = Project(workspace_id=1, code="myapp")
    assert project.id == 0
    assert project.status is ProjectStatus.pending


@pytest.mark.unit
def test_milestone_defaults() -> None:
    milestone = Milestone(workspace_id=1, code="myapp-MS1")
    assert milestone.status is WorkflowStatus.pending


@pytest.mark.unit
def test_change_defaults() -> None:
    change = Change(workspace_id=1, code="myapp-C1", kind=ChangeKind.new_feature)
    assert change.status is WorkflowStatus.pending


@pytest.mark.unit
def test_fact_defaults() -> None:
    fact = Fact(workspace_id=1, code="myapp-F1")
    assert fact.status is LifecycleStatus.active
    assert fact.superseded_by is None


@pytest.mark.unit
def test_task_defaults() -> None:
    task = Task(workspace_id=1, code="myapp-T1")
    assert task.status is TriageStatus.open
    assert task.change_id is None
    assert task.milestone_id is None
    assert task.converted_to_code == ""


@pytest.mark.unit
def test_validation_defaults() -> None:
    validation = Validation(workspace_id=1, code="myapp-V1")
    assert validation.status is LifecycleStatus.active
    assert validation.scenarios == []
    assert validation.coverage == []


@pytest.mark.unit
def test_bug_defaults() -> None:
    bug = Bug(workspace_id=1, code="myapp-B1")
    assert bug.status is TriageStatus.open
    assert bug.severity is BugSeverity.medium


@pytest.mark.unit
def test_idea_defaults() -> None:
    idea = Idea(workspace_id=1, code="myapp-I1")
    assert idea.status is TriageStatus.open
    assert idea.converted_to_code == ""


@pytest.mark.unit
def test_validation_scenario() -> None:
    scenario = ValidationScenario(description="smoke path")
    assert scenario.description == "smoke path"


@pytest.mark.unit
def test_document_ref() -> None:
    ref = DocumentRef(doc_type="design", path="docs/design.md")
    assert ref.project_id is None
    assert ref.change_id is None
