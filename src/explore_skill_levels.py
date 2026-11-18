import pandas as pd

from data.loader import load_essential_skills
from data.loader import load_transferable_skills

essential_skills = load_essential_skills()
transferable_skills = load_transferable_skills()

essential_skills = essential_skills[
    essential_skills["O*NET-SOC Code"] == "15-1252.00"
]

transferable_skills = transferable_skills[
    transferable_skills["O*NET-SOC Code"] == "15-1252.00"
]


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

merged = transform_transferable_skills(transferable_skills)
print(merged)


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

    return merged[["Element Name", "Rank", "Importance", "Level"]]
    
merged = transform_essential_skills(essential_skills)
print(merged)
