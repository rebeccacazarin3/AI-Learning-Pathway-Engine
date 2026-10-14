from models.user_profile import UserProfile
from models.skill import Skill
from models.proficiency import ProficiencyLevel


profile1 = UserProfile()
profile2 = UserProfile()

python_skill = Skill(
    name="Python",
    proficiency=ProficiencyLevel.INTERMEDIATE,
    source="user"
)

profile1.skills.append(python_skill)

print("Profile 1:", profile1.skills)
print("Profile 2:", profile2.skills)

assert len(profile1.skills) == 1
assert len(profile2.skills) == 0

print("PASS: Profiles maintain independent skill collections.")