import pytest

from psg_domain.entities import (
    Change,
    ChangeType,
    Fact,
    LifecycleStatus,
    Project,
    WorkflowStatus,
)
from psg_domain.view import (
    DependencyEdge,
    entity_detail,
    list_entities,
    order_changes,
    project_overview,
)


@pytest.mark.unit
def test_project_overview_counts_open_and_total_changes_in_subtree() -> None:
    project = Project(id=1, workspace_id=1, code="app", title="App")
    open_change = Change(
        id=10,
        workspace_id=1,
        code="app-C1",
        title="Open",
        type=ChangeType.new_feature,
        status=WorkflowStatus.in_progress,
        project_id=1,
    )
    done_change = Change(
        id=11,
        workspace_id=1,
        code="app-C2",
        title="Done",
        type=ChangeType.new_feature,
        status=WorkflowStatus.done,
        project_id=1,
    )
    overview = project_overview(
        project,
        entities=[project, open_change, done_change],
        document_refs=[],
    )
    assert overview.changes.open == 1
    assert overview.changes.total == 2


@pytest.mark.unit
def test_project_overview_counts_active_facts_only() -> None:
    project = Project(id=1, workspace_id=1, code="app", title="App")
    active = Fact(
        id=20,
        workspace_id=1,
        code="app-F1",
        title="Active",
        status=LifecycleStatus.active,
        project_id=1,
    )
    superseded = Fact(
        id=21,
        workspace_id=1,
        code="app-F2",
        title="Old",
        status=LifecycleStatus.superseded,
        project_id=1,
    )
    overview = project_overview(
        project,
        entities=[project, active, superseded],
        document_refs=[],
    )
    assert overview.facts == 1


@pytest.mark.unit
def test_entity_detail_change_includes_goal_dependencies_and_required_by() -> None:
    change_a = Change(
        id=1,
        workspace_id=1,
        code="app-C1",
        title="A",
        type=ChangeType.new_feature,
        goal="ship it",
        project_id=1,
    )
    change_b = Change(
        id=2,
        workspace_id=1,
        code="app-C2",
        title="B",
        type=ChangeType.new_feature,
        project_id=1,
    )
    change_c = Change(
        id=3,
        workspace_id=1,
        code="app-C3",
        title="C",
        type=ChangeType.new_feature,
        project_id=1,
    )
    edges = [
        DependencyEdge(dependent_id=1, dependency_id=3),
        DependencyEdge(dependent_id=2, dependency_id=1),
    ]
    detail = entity_detail(
        change_a,
        entities=[change_a, change_b, change_c],
        edges=edges,
    )
    goal_labels = [section.label for section in detail.sections]
    assert "goal" in goal_labels
    assert len(detail.dependencies) == 1
    assert detail.dependencies[0].code == "app-C3"
    assert len(detail.required_by) == 1
    assert detail.required_by[0].code == "app-C2"


@pytest.mark.unit
def test_list_entities_parent_code_filters_changes_under_parent() -> None:
    parent = Project(id=1, workspace_id=1, code="app", title="App")
    other_parent = Project(id=2, workspace_id=1, code="other", title="Other")
    change_on_app = Change(
        id=10,
        workspace_id=1,
        code="app-C1",
        title="On app",
        type=ChangeType.new_feature,
        project_id=1,
    )
    change_on_other = Change(
        id=11,
        workspace_id=1,
        code="other-C1",
        title="On other",
        type=ChangeType.new_feature,
        project_id=2,
    )
    listed = list_entities(
        "changes",
        [parent, other_parent, change_on_app, change_on_other],
        parent_code="app",
    )
    assert len(listed.groups) == 1
    assert listed.groups[0].parent_code == "app"
    assert [item.code for item in listed.groups[0].items] == ["app-C1"]


@pytest.mark.unit
def test_order_changes_dependency_first_without_cycle() -> None:
    change_a = Change(
        id=1,
        workspace_id=1,
        code="app-C1",
        title="A",
        type=ChangeType.new_feature,
    )
    change_b = Change(
        id=2,
        workspace_id=1,
        code="app-C2",
        title="B",
        type=ChangeType.new_feature,
    )
    edges = [DependencyEdge(dependent_id=2, dependency_id=1)]
    result = order_changes([change_a, change_b], edges=edges)
    assert result.has_cycle is False
    assert [item.code for item in result.changes] == ["app-C1", "app-C2"]


@pytest.mark.unit
def test_order_changes_detects_cycle_and_preserves_input_order() -> None:
    change_a = Change(
        id=1,
        workspace_id=1,
        code="app-C1",
        title="A",
        type=ChangeType.new_feature,
    )
    change_b = Change(
        id=2,
        workspace_id=1,
        code="app-C2",
        title="B",
        type=ChangeType.new_feature,
    )
    edges = [
        DependencyEdge(dependent_id=1, dependency_id=2),
        DependencyEdge(dependent_id=2, dependency_id=1),
    ]
    result = order_changes([change_a, change_b], edges=edges)
    assert result.has_cycle is True
    assert [item.code for item in result.changes] == ["app-C1", "app-C2"]
