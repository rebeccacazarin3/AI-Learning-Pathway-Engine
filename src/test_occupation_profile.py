from services.occupation_profile import (
    get_occupation_profile,
    transform_transferable_skills,
)

profile = get_occupation_profile("15-1252.00")

print(profile.keys())

print("\n--- Tasks ---")
tasks = profile["tasks"][["Task", "Task Type"]]
print(tasks)

print("\n--- DWAs ---")
dwas = profile["dwas"]["DWA Element Name"].unique().tolist()
print(dwas)

print("\n--- Essential Skills ---")
print(profile["essential_skills"])

print("\n--- Transferable Skills ---")
print(profile["transferable_skills"].columns.tolist())
print(profile["transferable_skills"].head(20).to_string())

print("\n--- Transferable Skill Summary ---")

transferable = profile["transferable_skills"]

print("Unique skills:",
      transferable["Element Name"].nunique())

print("\nUnique skill names:")
print(transferable["Element Name"].unique().tolist())

print("\n--- Ranked Transferable Skills ---")

transferable_skills = transform_transferable_skills(
    profile["transferable_skills"]
)

print(transferable_skills.to_string(index=False))

print("\n--- Transferable Skill Levels ---")
transferable = profile["transferable_skills"]

levels = transferable[
    transferable["Scale Name"] == "Level"
]

print(levels[["Element Name", "Data Value"]].to_string(index=False))




