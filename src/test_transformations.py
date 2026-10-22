from data.transformations import (transform_transferable_skills, transform_dwas, transform_software_skills)
import pandas as pd
from services import occupation_profile

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

raw_dwas = occupation_profile.get_dwas_by_code("15-1252.00")
result = transform_dwas(raw_dwas)

assert len(result) == 18 
assert len(result) == len(set(result))

empty_dwas = pd.DataFrame()
try :
    transform_dwas(empty_dwas)
except ValueError as e:
    assert str(e) == "The DWA DataFrame is empty."
else :
    assert False, "Expected ValueError for empty dwas DataFrame"

raw_software_skills = occupation_profile.get_software_skills_by_code("15-1252.00")

grouped = raw_software_skills.groupby("Element Name")[
    ["Workplace Example", "Hot Technology", "In Demand"]
]

result = grouped.apply(lambda x: x.to_dict(orient="records")).rename("Workplace Examples").reset_index()

print(result.iloc[0]["Element Name"])
print(result.iloc[0]["Workplace Examples"])