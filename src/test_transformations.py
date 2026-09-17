from data.transformations import transform_transferable_skills
from services.occupation_profile import get_occupation_profile

profile = get_occupation_profile("15-1252.00")
result = transform_transferable_skills(profile["transferable_skills"])

print(type(result))

assert not result.empty, "The transformed transferable skills DataFrame is empty."
assert len(result) == 25, "Expected 25 transferable skills"
assert list(result.columns) == [
    "Rank", "Element Name", "Importance", "Level"
], "Expected columns in the transformed DataFrame"
assert result.iloc[0]["Element Name"] == "Programming", \
    "The first skill should be Programming."

print(result.to_string(index=False))