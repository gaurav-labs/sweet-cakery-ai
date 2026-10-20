from dataclasses import dataclass

@dataclass
class WorkflowError:
    code: str
    message: str