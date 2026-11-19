from dataclasses import dataclass
from ai_learning_pathway.models.user_skill import UserSkill
from ai_learning_pathway.models.skill_check_status import SkillCheckStatus

@dataclass
class SkillCheckResult:
    status: SkillCheckStatus
    proposed_skill: UserSkill
    existing_skill: UserSkill | None = None



