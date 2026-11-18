from dataclasses import dataclass, field
from models.user_skill import UserSkill


@dataclass
class UserProfile:
    skills: list[UserSkill] = field(default_factory=list)