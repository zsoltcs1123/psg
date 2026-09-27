import msgspec.structs

from psg_domain.entities import Bug, Change, Idea, Project, Task, TriageStatus
from psg_domain.errors import InvalidCloseStatusError, InvalidConversionTargetError
from psg_domain.workflow import transition

TriageItem = Task | Bug | Idea

_LEGAL_CLOSE_STATUSES = frozenset({TriageStatus.done, TriageStatus.wontfix})


def close(item: TriageItem, status: TriageStatus) -> TriageItem:
    if status not in _LEGAL_CLOSE_STATUSES:
        raise InvalidCloseStatusError(status.value)
    return transition(item, status)


def convert(
    item: TriageItem,
    target: Change | Project | Task | Bug | Idea,
) -> TriageItem:
    if not isinstance(target, (Change, Project)):
        raise InvalidConversionTargetError()
    converted = transition(item, TriageStatus.converted)
    return msgspec.structs.replace(converted, converted_to_code=target.code)


def link_change(item: Task | Bug, change: Change | None) -> Task | Bug:
    change_id = None if change is None else change.id
    return msgspec.structs.replace(item, change_id=change_id)
