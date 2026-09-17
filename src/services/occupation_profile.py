import pandas as pd
from services.occupation_service import (
    get_dwas_by_code,
    get_essential_skills_by_code,
    get_occupation_by_code,
    get_tasks_by_code,
    get_transferable_skills_by_code,
)


def get_occupation_profile(occupation_code):
    essential_skills = get_essential_skills_by_code(occupation_code)
    essential_skills = transform_essential_skills(essential_skills)

    return {
        "occupation": get_occupation_by_code(occupation_code),
        "tasks": get_tasks_by_code(occupation_code),
        "dwas": get_dwas_by_code(occupation_code),
        "essential_skills": essential_skills,
        "transferable_skills": get_transferable_skills_by_code(occupation_code)
    }


def transform_essential_skills(essential_skills):
    """
    Transform the essential skills DataFrame to include rank and level.

    Args:
        essential_skills: DataFrame containing raw essential skills data.

    Returns:
        A transformed DataFrame with rank and level.
    """

    importance = essential_skills[
        essential_skills["Scale Name"] == "Importance"
    ]

    importance = importance.rename(
      columns={"Data Value": "Importance"}
    ) 

    importance = importance[["Element Name", "Importance"]]

    importance = importance.sort_values(
      by="Importance",
      ascending=False
    )

    level = essential_skills[
        essential_skills["Scale Name"] == "Level" 
    ]

    level = level.rename(
        columns={"Data Value": "Level"}
    )

    level = level[["Element Name", "Level"]]

    merged = pd.merge(
        importance,
        level,
        on="Element Name",
        how="left"
    )

    merged["Rank"] = range(1, len(merged) + 1)

    return merged[["Element Name", "Rank", "Level"]]

def transform_transferable_skills(transferable_skills):
    """
    Transform the transferable skills DataFrame to include rank and level.

    Args:
        transferable_skills: DataFrame containing raw transferable skills data.

    Returns:
        A transformed DataFrame with rank and level.
    """

    importance = transferable_skills[
        transferable_skills["Scale Name"] == "Importance"
    ]

    importance = importance.rename(
      columns={"Data Value": "Importance"}
    ) 

    importance = importance[["Element Name", "Importance"]]

    importance = importance.sort_values(
      by="Importance",
      ascending=False
    )

    level = transferable_skills[
        transferable_skills["Scale Name"] == "Level" 
    ]

    level = level.rename(
        columns={"Data Value": "Level"}
    )

    level = level[["Element Name", "Level"]]

    merged = pd.merge(
        importance,
        level,
        on="Element Name",
        how="left"
    )

    merged["Rank"] = range(1, len(merged) + 1)

    return merged[[ "Rank", "Element Name", "Importance", "Level"]]