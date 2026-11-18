from dataclasses import dataclass
from models.proficiency import ProficiencyLevel

@dataclass
class UserSkill:
    skill_id: str
    proficiency: ProficiencyLevel
    source: str

