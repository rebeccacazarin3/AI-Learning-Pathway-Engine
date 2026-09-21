from data.transformations import transform_transferable_skills
from data.loader import load_transferable_skills
import pandas as pd
from services import occupation_profile

transferable_skills = load_transferable_skills()
result = transform_transferable_skills(transferable_skills)

raw_skills = occupation_profile.get_transferable_skills_by_code("15-1252.00")
result = transform_transferable_skills(raw_skills)

assert not result.empty, "Expected a non-empty transformed DataFrame"
assert len(result) == 25, "Expected 25 transferable skills"
assert list(result.columns) == [
    "Rank", "Element Name", "Importance", "Level"
], "Expected columns in the transformed DataFrame"
assert result.iloc[0]["Element Name"] == "Programming", "The first skill should be Programming."

empty_skills = pd.DataFrame()
try:
    transform_transferable_skills(empty_skills)
except ValueError as e:
    assert str(e) == "The transferable skills DataFrame is empty."
else:
    assert False, "Expected ValueError for empty transferable skills DataFrame"
