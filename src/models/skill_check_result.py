from dataclasses import dataclass
from models.skill import Skill
from skill_check_status import SkillCheckStatus

@dataclass
class SkillCheckResult:
    status: SkillCheckStatus
    proposed_skill: Skill
    existing_skill: Skill | None = None



