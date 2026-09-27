from enum import StrEnum
from typing import Annotated

from msgspec import Meta, Struct

ProjectCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+$")]
MilestoneCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-MS\d+$")]
ChangeCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-C\d+$")]
FactCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-F\d+$")]
ValidationCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-V\d+$")]
TaskCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-T\d+$")]
BugCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-B\d+$")]
IdeaCode = Annotated[str, Meta(pattern=r"^[A-Za-z0-9_-]+-I\d+$")]


class WorkflowStatus(StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class ProjectStatus(StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    obsolete = "obsolete"


class LifecycleStatus(StrEnum):
    active = "active"
    superseded = "superseded"


class TriageStatus(StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"
    wontfix = "wontfix"
    converted = "converted"


class ChangeType(StrEnum):
    new_feature = "new_feature"
    feature_update = "feature_update"
    cross_cutting = "cross_cutting"
    refactor = "refactor"


class BugSeverity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Project(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ProjectCode
    status: ProjectStatus = ProjectStatus.pending


class Milestone(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: MilestoneCode
    status: WorkflowStatus = WorkflowStatus.pending


class Change(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ChangeCode
    type: ChangeType
    status: WorkflowStatus = WorkflowStatus.pending


class Fact(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: FactCode
    status: LifecycleStatus = LifecycleStatus.active
    superseded_by: int | None = None


class Validation(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ValidationCode
    status: LifecycleStatus = LifecycleStatus.active
    scenarios: list[str] = []
    coverage: list[str] = []
    change_id: int | None = None
    superseded_by: int | None = None


class Task(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: TaskCode
    status: TriageStatus = TriageStatus.pending
    change_id: int | None = None
    milestone_id: int | None = None
    converted_to_code: str = ""


class Bug(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: BugCode
    status: TriageStatus = TriageStatus.pending
    severity: BugSeverity = BugSeverity.medium
    change_id: int | None = None
    milestone_id: int | None = None
    converted_to_code: str = ""


class Idea(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: IdeaCode
    status: TriageStatus = TriageStatus.pending
    milestone_id: int | None = None
    converted_to_code: str = ""


class DocumentRef(Struct, kw_only=True):
    doc_type: str
    path: str
    project_id: int | None = None
    change_id: int | None = None


Entity = Project | Milestone | Change | Fact | Validation | Task | Bug | Idea
DependencyTarget = Entity
