from ai_learning_pathway.models.user_skill import UserSkill
from ai_learning_pathway.models.proficiency import ProficiencyLevel


skill = UserSkill(
    skill_id="SKL-001",
    proficiency=ProficiencyLevel.INTERMEDIATE,
    source="user"
)

print(skill)
print(skill.skill_id)
print(skill.proficiency)
print(skill.proficiency.value)
print(skill.source)