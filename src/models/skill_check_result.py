from dataclasses import dataclass
from models.user_skill import UserSkill
from models.skill_check_status import SkillCheckStatus

@dataclass
class SkillCheckResult:
    status: SkillCheckStatus
    proposed_skill: UserSkill
    existing_skill: UserSkill | None = None



