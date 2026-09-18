from data.transformations import transform_transferable_skills
from services.occupation_profile import get_occupation_profile
import pandas as pd


profile = get_occupation_profile("15-1252.00")
result = transform_transferable_skills(profile["transferable_skills"])

assert len(result) == 25, "Expected 25 transferable skills"
assert list(result.columns) == [
    "Rank", "Element Name", "Importance", "Level"
], "Expected columns in the transformed DataFrame"
assert result.iloc[0]["Element Name"] == "Programming", \
    "The first skill should be Programming."

empty_skills = pd.DataFrame()   
try:
    transform_transferable_skills(empty_skills)
except ValueError as e:
    assert str(e) == "The transferable skills DataFrame is empty."
else:
    assert False, "Expected ValueError for empty transferable skills DataFrame"
