import pandas as pd


def transform_transferable_skills(transferable_skills):
    """
    Transform the transferable skills DataFrame to include rank and level.

    Args:
        transferable_skills: DataFrame containing raw transferable skills data.

    Returns:
        A transformed DataFrame with Rank, Element Name, Importance, and Level.
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

