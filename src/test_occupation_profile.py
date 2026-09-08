from asyncio import tasks

from services.occupation_service import (
    get_dwas_by_code,
    get_essential_skills_by_code,
    get_occupation_by_code,
    get_tasks_by_code,
    get_transferable_skills_by_code,
)
from services.occupation_profile import get_occupation_profile


def get_occupation_profile(occupation_code):
    """
    Retrieve the complete occupation profile for a specific occupation code.

    Args:
        occupation_code: The O*NET-SOC code of the occupation to retrieve the profile for.

    Returns:
        A dictionary containing the complete occupation profile.
    """
    return {
        "occupation": get_occupation_by_code(occupation_code),
        "tasks": get_tasks_by_code(occupation_code),
        "dwas": get_dwas_by_code(occupation_code),
        "essential_skills": get_essential_skills_by_code(occupation_code),
        "transferable_skills": get_transferable_skills_by_code(occupation_code)
    }

profile = get_occupation_profile("15-1252.00")
print(profile.keys())





tasks = profile["tasks"][["Task", "Task Type"]]
print(tasks)

dwas = profile["dwas"]["DWA Element Name"].unique().tolist()
print(dwas)



essential_skills = profile["essential_skills"]
importance = essential_skills[essential_skills["Scale Name"] == "Importance"]
importance = importance.sort_values("Data Value", ascending=False)
print(importance[["Element Name", "Data Value"]])