import pandas as pd



def transform_transferable_skills(transferable_skills):
    """
    Transform the transferable skills DataFrame to include rank and level.

    Args:
        transferable_skills: DataFrame containing raw transferable skills data.

    Returns:
        A transformed DataFrame with Rank, Element Name, Importance, and Level.
    """

    if transferable_skills.empty:
        raise ValueError(
            "The transferable skills DataFrame is empty."
        )
    
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

def transform_tasks(tasks):
    """
    Transform the tasks DataFrame to include description of each task and type.

    Args:
        tasks: DataFrame containing raw tasks data.

    Returns:
        A transformed DataFrame with description and type for each task.
    """

    if tasks.empty:
        raise ValueError(
            "The tasks DataFrame is empty."
        )

    tasks = tasks[["Task", "Task Type"]]

    tasks_order = {
        "Core": 0,
        "Supplemental": 1
    }

    fallback_value = 2

    tasks["Task Order"] = tasks["Task Type"].map(
        tasks_order
    ).fillna(fallback_value)

    tasks = tasks.sort_values(
        by=["Task Order", "Task"]
    )

    tasks = tasks[["Task", "Task Type"]]

    return tasks