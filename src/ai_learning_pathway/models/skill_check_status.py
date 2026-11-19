from enum import Enum

class SkillCheckStatus(Enum):
    NEW = "New"
    DUPLICATE = "Duplicate"
    CONFLICT = "Conflict"
    