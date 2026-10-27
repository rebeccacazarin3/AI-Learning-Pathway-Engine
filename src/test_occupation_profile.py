from services.occupation_profile import (
    get_occupation_profile,
)

from services.occupation_service import (
    occupation_model_from_code,
)

from models.occupation import Occupation

profile = get_occupation_profile("15-1252.00")

assert isinstance(profile["occupation"], Occupation)

print(tasks := profile["tasks"])

print("\n--- DWAs ---")
assert len(profile["dwas"]) == 18
assert len(profile["dwas"]) == len(set(profile["dwas"]))
print(profile["dwas"])

print("\n--- Essential Skills ---")

print(profile["essential_skills"])

print("\n--- Transferable Skills ---")

print(profile["transferable_skills"])

occupation = occupation_model_from_code("15-1252.00")

print(occupation)
print(type(occupation))

print("\n--- Software Skills ---")
assert "software_skills" in profile
assert not profile["software_skills"].empty
assert len(profile["software_skills"]) == 67
total_examples = sum(
    len(examples)
    for examples in profile["software_skills"]["Workplace Examples"]
)

assert total_examples == 430, (
    f"Expected 430 workplace examples, got {total_examples}"
)

for index, row in profile["software_skills"].iterrows():
    assert isinstance(row["Workplace Examples"], list)

    for example in row["Workplace Examples"]:
        assert example["Hot Technology"] in ["Y", "N"]
        assert example["In Demand"] in ["Y", "N"]
        assert set(example.keys()) == {
            "Workplace Example",
            "Hot Technology",
            "In Demand"
        }, "Expected each workplace example to contain all three fields"

print(f"Software categories: {len(profile['software_skills'])}")

total_examples = sum(
    len(examples)
    for examples in profile["software_skills"]["Workplace Examples"]
)

print(f"Workplace examples: {total_examples}")
print("Occupation profile integration tests passed.")