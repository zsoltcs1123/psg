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
    title: str = ""
    status: ProjectStatus = ProjectStatus.pending
    description: str = ""
    parent_id: int | None = None


class Milestone(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: MilestoneCode
    title: str = ""
    status: WorkflowStatus = WorkflowStatus.pending
    project_id: int | None = None
    goal: str = ""
    success_criteria: list[str] = []


class Change(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ChangeCode
    title: str = ""
    type: ChangeType
    status: WorkflowStatus = WorkflowStatus.pending
    project_id: int | None = None
    goal: str = ""
    deliverables: list[str] = []
    notes: list[str] = []
    milestone_id: int | None = None


class Fact(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: FactCode
    title: str = ""
    status: LifecycleStatus = LifecycleStatus.active
    superseded_by: int | None = None
    project_id: int | None = None
    body: str = ""


class Validation(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: ValidationCode
    title: str = ""
    status: LifecycleStatus = LifecycleStatus.active
    scenarios: list[str] = []
    coverage: list[str] = []
    change_id: int | None = None
    superseded_by: int | None = None
    project_id: int | None = None


class Task(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: TaskCode
    title: str = ""
    status: TriageStatus = TriageStatus.pending
    change_id: int | None = None
    milestone_id: int | None = None
    converted_to_code: str = ""
    project_id: int | None = None
    body: str = ""


class Bug(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: BugCode
    title: str = ""
    status: TriageStatus = TriageStatus.pending
    severity: BugSeverity = BugSeverity.medium
    change_id: int | None = None
    milestone_id: int | None = None
    converted_to_code: str = ""
    project_id: int | None = None
    description: str = ""
    repro_notes: list[str] = []
    notes: list[str] = []


class Idea(Struct, kw_only=True):
    id: int = 0
    workspace_id: int
    code: IdeaCode
    title: str = ""
    status: TriageStatus = TriageStatus.pending
    milestone_id: int | None = None
    converted_to_code: str = ""
    project_id: int | None = None
    body: str = ""


class DocumentRef(Struct, kw_only=True):
    doc_type: str
    path: str
    project_id: int | None = None
    change_id: int | None = None


Entity = Project | Milestone | Change | Fact | Validation | Task | Bug | Idea
DependencyTarget = Entity
