from asyncio import tasks
import pandas as pd

from services.occupation_service import (
    get_dwas_by_code,
    get_essential_skills_by_code,
    get_occupation_by_code,
    get_tasks_by_code,
    get_transferable_skills_by_code,
)

profile = get_occupation_profile("15-1252.00")
print(profile.keys())


tasks = profile["tasks"][["Task", "Task Type"]]
print(tasks)

dwas = profile["dwas"]["DWA Element Name"].unique().tolist()
print(dwas)




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




















