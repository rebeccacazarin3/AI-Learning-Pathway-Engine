from dataclasses import dataclass
from ai_learning_pathway.models.proficiency import ProficiencyLevel

@dataclass
class UserSkill:
    skill_id: str
    proficiency: ProficiencyLevel
    source: str

