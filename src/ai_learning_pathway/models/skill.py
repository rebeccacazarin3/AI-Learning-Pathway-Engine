from dataclasses import dataclass


@dataclass
class Skill:
    skill_id: str
    name: str
    aliases: list[str]
    description: str
    category: str