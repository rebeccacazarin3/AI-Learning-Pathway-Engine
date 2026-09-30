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