from models.skill import Skill
from models.proficiency import ProficiencyLevel


skill = Skill(
    name="Python",
    proficiency=ProficiencyLevel.INTERMEDIATE,
    source="user"
)

print(skill)
print(skill.name)
print(skill.proficiency)
print(skill.proficiency.value)
print(skill.source)