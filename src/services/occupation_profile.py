
from data.transformations import (
    transform_essential_skills,
    transform_transferable_skills,
    transform_tasks
)

from services.occupation_service import (
    get_dwas_by_code,
    get_essential_skills_by_code,
    occupation_model_from_code,
    get_tasks_by_code,
    get_transferable_skills_by_code,
)

def get_occupation_profile(occupation_code):
    essential_skills = get_essential_skills_by_code(occupation_code)
    essential_skills = transform_essential_skills(essential_skills)
    transferable_skills = get_transferable_skills_by_code(occupation_code)
    transferable_skills = transform_transferable_skills(transferable_skills)

    return {
        "occupation": occupation_model_from_code(occupation_code),
        "tasks": transform_tasks (get_tasks_by_code(occupation_code)),
        "dwas": get_dwas_by_code(occupation_code),
        "essential_skills": essential_skills,
        "transferable_skills": transferable_skills,
    }


