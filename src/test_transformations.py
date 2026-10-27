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
result = transform_software_skills(raw_software_skills)


assert not result.empty, "Expected a non-empty transformed DataFrame"

assert list(result.columns) == [
    "Element Name", "Workplace Examples"
], "Expected columns in the transformed DataFrame"

assert len(set(result["Element Name"])) == len(result), \
    "Expected unique Element Names in the transformed DataFrame"

assert set(result.iloc[0]["Workplace Examples"][0].keys()) == set([
    "Workplace Example",
    "Hot Technology",
    "In Demand"
]), "Expected each workplace example to contain all three fields"

assert result.iloc[0]["Workplace Examples"][0]["Hot Technology"] in ["Y", "N"], "Expected Hot Technology to be either Y or N"


for index, row in result.iterrows():
    assert isinstance(row["Workplace Examples"], list), "Expected Workplace Examples to be a list"

    for example in row["Workplace Examples"]:
        assert example["Hot Technology"] in ["Y", "N"], "Expected Hot Technology to be either Y or N"
        assert example["In Demand"] in ["Y", "N"], "Expected In Demand to be either Y or N"
        assert set(example.keys()) == {
            "Workplace Example",
         "Hot Technology",
          "In Demand"
        }, "Expected each workplace example to contain all three fields"

empty_software_skills = pd.DataFrame()
try:
    transform_software_skills(empty_software_skills)
except ValueError as e:
    assert str(e) == "The software skills DataFrame is empty."
else:
    assert False, "Expected ValueError for empty software skills DataFrame"

print(f"Software categories tested: {len(result)}")

total_examples = sum(
    len(examples)
    for examples in result["Workplace Examples"]
)

print(f"Workplace examples tested: {total_examples}")
print("All software skills transformation tests passed.")