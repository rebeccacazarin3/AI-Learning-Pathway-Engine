from dataclasses import dataclass, field
from models.skill import Skill


@dataclass
class UserProfile:
    skills: list[Skill] = field(default_factory=list)