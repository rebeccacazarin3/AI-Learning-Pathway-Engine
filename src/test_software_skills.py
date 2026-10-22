from services.occupation_service import get_software_skills_by_code

software_skills = get_software_skills_by_code("15-1252.00")

print(software_skills)
print(software_skills.empty)

assert not software_skills.empty, "Software skills DataFrame is empty"
assert (software_skills["O*NET-SOC Code"] == "15-1252.00").all(), "O*NET-SOC Code column does not match the expected value"
assert "Element Name" in software_skills.columns, "'Element Name' column is missing"
assert "Hot Technology" in software_skills.columns, "'Hot Technology' column is missing"
assert "In Demand" in software_skills.columns, "'In Demand' column is missing"