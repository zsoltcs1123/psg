class InvalidTransitionError(Exception):
    def __init__(self, current: str, requested: str, allowed: list[str]) -> None:
        self.current = current
        self.requested = requested
        self.allowed = allowed
        super().__init__(f"invalid transition from {current} to {requested}")


class BlockedByDependencyError(Exception):
    def __init__(self, blocking_codes: list[str]) -> None:
        self.blocking_codes = blocking_codes
        super().__init__(f"blocked by dependencies: {', '.join(blocking_codes)}")


class MilestoneIncompleteError(Exception):
    def __init__(self, milestone_code: str, blocking_codes: list[str]) -> None:
        self.milestone_code = milestone_code
        self.blocking_codes = blocking_codes
        super().__init__(f"milestone {milestone_code} incomplete: {', '.join(blocking_codes)}")


class InvalidCloseStatusError(Exception):
    def __init__(self, status: str) -> None:
        self.status = status
        super().__init__(f"invalid close status: {status}")


class InvalidConversionTargetError(Exception):
    def __init__(self) -> None:
        super().__init__("invalid conversion target")
