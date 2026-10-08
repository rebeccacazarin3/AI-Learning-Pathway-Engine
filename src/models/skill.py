from dataclasses import dataclass
from models.proficiency import ProficiencyLevel

@dataclass
class Skill:
    name: str
    proficiency: ProficiencyLevel
    source: str

