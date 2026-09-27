from collections.abc import Callable

import pytest

from psg_domain.entities import (
    Bug,
    BugSeverity,
    Change,
    ChangeType,
    Idea,
    Project,
    Task,
    TriageStatus,
)
from psg_domain.errors import InvalidCloseStatusError, InvalidConversionTargetError
from psg_domain.triage import close, convert, link_change

_WS = 1


@pytest.mark.unit
@pytest.mark.parametrize(
    "factory",
    [
        lambda: Task(workspace_id=_WS, code="app-T1"),
        lambda: Bug(workspace_id=_WS, code="app-B1"),
        lambda: Idea(workspace_id=_WS, code="app-I1"),
    ],
    ids=["task", "bug", "idea"],
)
@pytest.mark.parametrize(
    "status",
    [TriageStatus.done, TriageStatus.wontfix],
    ids=["done", "wontfix"],
)
def test_close_from_pending_legal(
    factory: Callable[[], Task | Bug | Idea], status: TriageStatus
) -> None:
    item = factory()
    result = close(item, status)
    assert result.status is status
    assert result is not item


@pytest.mark.unit
@pytest.mark.parametrize(
    "factory",
    [
        lambda: Task(workspace_id=_WS, code="app-T1"),
        lambda: Bug(workspace_id=_WS, code="app-B1"),
        lambda: Idea(workspace_id=_WS, code="app-I1"),
    ],
    ids=["task", "bug", "idea"],
)
@pytest.mark.parametrize(
    "status",
    [TriageStatus.converted, TriageStatus.in_progress],
    ids=["converted", "in_progress"],
)
def test_close_rejects_non_terminal_status(
    factory: Callable[[], Task | Bug | Idea], status: TriageStatus
) -> None:
    item = factory()
    with pytest.raises(InvalidCloseStatusError) as exc_info:
        close(item, status)
    assert exc_info.value.status == status.value


@pytest.mark.unit
@pytest.mark.parametrize(
    "factory",
    [
        lambda: Task(workspace_id=_WS, code="app-T1"),
        lambda: Bug(workspace_id=_WS, code="app-B1"),
        lambda: Idea(workspace_id=_WS, code="app-I1"),
    ],
    ids=["task", "bug", "idea"],
)
@pytest.mark.parametrize(
    "target_factory",
    [
        lambda: Change(
            workspace_id=_WS,
            code="app-C1",
            type=ChangeType.new_feature,
        ),
        lambda: Project(workspace_id=_WS, code="app"),
    ],
    ids=["change", "project"],
)
def test_convert_sets_converted_status_and_code(
    factory: Callable[[], Task | Bug | Idea],
    target_factory: Callable[[], Change | Project],
) -> None:
    item = factory()
    target = target_factory()
    result = convert(item, target)
    assert result.status is TriageStatus.converted
    assert result.converted_to_code == target.code


@pytest.mark.unit
@pytest.mark.parametrize(
    "factory",
    [
        lambda: Task(workspace_id=_WS, code="app-T1"),
        lambda: Bug(workspace_id=_WS, code="app-B1"),
        lambda: Idea(workspace_id=_WS, code="app-I1"),
    ],
    ids=["task", "bug", "idea"],
)
def test_convert_rejects_task_target(factory: Callable[[], Task | Bug | Idea]) -> None:
    item = factory()
    target = Task(workspace_id=_WS, code="app-T2")
    with pytest.raises(InvalidConversionTargetError):
        convert(item, target)
    assert item.status is TriageStatus.pending
    assert item.converted_to_code == ""


@pytest.mark.unit
@pytest.mark.parametrize(
    "factory",
    [
        lambda: Task(workspace_id=_WS, code="app-T1"),
        lambda: Bug(
            workspace_id=_WS,
            code="app-B1",
            severity=BugSeverity.high,
        ),
    ],
    ids=["task", "bug"],
)
def test_link_change_sets_change_id_from_pending(
    factory: Callable[[], Task | Bug],
) -> None:
    item = factory()
    change = Change(
        workspace_id=_WS,
        code="app-C1",
        type=ChangeType.new_feature,
        id=42,
    )
    result = link_change(item, change)
    assert result.change_id == 42
    assert result.status is TriageStatus.pending


@pytest.mark.unit
@pytest.mark.parametrize(
    "factory",
    [
        lambda: Task(workspace_id=_WS, code="app-T1", change_id=99),
        lambda: Bug(workspace_id=_WS, code="app-B1", change_id=99),
    ],
    ids=["task", "bug"],
)
def test_link_change_none_clears_change_id(factory: Callable[[], Task | Bug]) -> None:
    item = factory()
    result = link_change(item, None)
    assert result.change_id is None
    assert result.status is item.status
