from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "raw"

OCCUPATIONS_FILE = DATA_DIR / "occupation_data.csv"
TASKS_FILE = DATA_DIR / "task_statements.csv"
TASKS_TO_DWAS_FILE = DATA_DIR / "tasks_to_dwas.csv"
ESSENTIAL_SKILLS_FILE = DATA_DIR / "essential_skills.csv"
SOFTWARE_SKILLS_FILE = DATA_DIR / "software_skills.csv"
TRANSFERABLE_SKILLS_FILE = DATA_DIR / "transferable_skills.csv"

# --------------------------------------------------
# Load data
# --------------------------------------------------

occupations = pd.read_csv(OCCUPATIONS_FILE)
tasks = pd.read_csv(TASKS_FILE)
tasks_to_dwas = pd.read_csv(TASKS_TO_DWAS_FILE)
essential_skills = pd.read_csv(ESSENTIAL_SKILLS_FILE)
software_skills = pd.read_csv(SOFTWARE_SKILLS_FILE)
transferable_skills = pd.read_csv(TRANSFERABLE_SKILLS_FILE)

# --------------------------------------------------
# Inspect Occupation Data
# --------------------------------------------------

print("\n" + "=" * 60)
print("OCCUPATION DATA")
print("=" * 60)

print("\nColumns:")
print(occupations.columns.tolist())

print("\nFirst 5 rows:")
print(occupations.head())


# --------------------------------------------------
# Inspect Task Statements
# --------------------------------------------------

print("\n" + "=" * 60)
print("TASK STATEMENTS")
print("=" * 60)

print("\nColumns:")
print(tasks.columns.tolist())

print("\nFirst 5 rows:")
print(tasks.head())


# --------------------------------------------------
# Basic dataset information
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATASET SHAPES")
print("=" * 60)

print(f"\nOccupation rows: {len(occupations):,}")
print(f"Task rows: {len(tasks):,}")

# --------------------------------------------------
# Validate Occupation → Task relationship
# --------------------------------------------------

print("\n" + "=" * 60)
print("RELATIONSHIP VALIDATION")
print("=" * 60)


# Get unique occupation codes from each dataset
occupation_codes = set(occupations["O*NET-SOC Code"])
task_occupation_codes = set(tasks["O*NET-SOC Code"])


# Find task occupation codes that do not exist
# in the occupation dataset
missing_occupations = (
    task_occupation_codes - occupation_codes
)


print(
    f"\nUnique occupations in occupation data: "
    f"{len(occupation_codes):,}"
)

print(
    f"Unique occupations with tasks: "
    f"{len(task_occupation_codes):,}"
)

print(
    f"Task occupation codes missing from "
    f"occupation data: {len(missing_occupations):,}"
)


if missing_occupations:
    print("\nMissing occupation codes:")
    print(missing_occupations)
else:
    print(
        "\n✓ All task occupation codes exist "
        "in occupation data."
    )

    # --------------------------------------------------
# Find Software Developers
# --------------------------------------------------

print("\n" + "=" * 60)
print("OCCUPATION SEARCH")
print("=" * 60)


search_term = "Software Developers"


matching_occupations = occupations[
    occupations["Title"].str.contains(
        search_term,
        case=False,
        na=False
    )
]


print(f"\nSearch term: {search_term}")

print("\nMatching occupations:")

print(
    matching_occupations[
        [
            "O*NET-SOC Code",
            "Title",
            "Description"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# Retrieve Tasks for Selected Occupation
# --------------------------------------------------

print("\n" + "=" * 60)
print("TASK RETRIEVAL")
print("=" * 60)


# Extract the O*NET-SOC code from the first match
occupation_code = matching_occupations.iloc[0]["O*NET-SOC Code"]


# Retrieve all tasks associated with this occupation
occupation_tasks = tasks[
    tasks["O*NET-SOC Code"] == occupation_code
]


print(f"\nOccupation: {matching_occupations.iloc[0]['Title']}")
print(f"O*NET-SOC Code: {occupation_code}")

print(f"\nTasks found: {len(occupation_tasks)}")


print("\nTasks:\n")

for _, row in occupation_tasks.iterrows():
    print(
        f"Task ID {row['Task ID']}: "
        f"{row['Task']}"
    )

# --------------------------------------------------
# Inspect Tasks to Detailed Work Activities Mapping
# --------------------------------------------------

print("\n" + "=" * 60)
print("TASKS TO DWAS")
print("=" * 60)

print("\nColumns:")
print(tasks_to_dwas.columns.tolist())

print("\nFirst 10 rows:")
print(tasks_to_dwas.head(10))

print("\nDataset shape:")
print(tasks_to_dwas.shape)

# --------------------------------------------------
# Retrieve DWAs for Selected Occupation
# --------------------------------------------------

print("\n" + "=" * 60)
print("DETAILED WORK ACTIVITY RETRIEVAL")
print("=" * 60)


# Retrieve Task → DWA mappings for the selected occupation
occupation_dwas = tasks_to_dwas[
    tasks_to_dwas["O*NET-SOC Code"] == occupation_code
]


print(f"\nOccupation: {matching_occupations.iloc[0]['Title']}")
print(f"O*NET-SOC Code: {occupation_code}")

print(
    f"\nTask → DWA relationships found: "
    f"{len(occupation_dwas)}"
)


# Count unique DWAs
unique_dwas = occupation_dwas[
    [
        "DWA Element ID",
        "DWA Element Name"
    ]
].drop_duplicates()


print(f"Unique Detailed Work Activities: {len(unique_dwas)}")


print("\nDetailed Work Activities:\n")

for _, row in unique_dwas.iterrows():
    print(
        f"{row['DWA Element ID']}: "
        f"{row['DWA Element Name']}"
    )

# --------------------------------------------------
# Analyze Task → DWA Relationship Coverage
# --------------------------------------------------

print("\n" + "=" * 60)
print("TASK → DWA RELATIONSHIP ANALYSIS")
print("=" * 60)


# Get the Task IDs for the selected occupation
occupation_task_ids = set(
    occupation_tasks["Task ID"]
)


# Get the Task IDs that have DWA mappings
mapped_task_ids = set(
    occupation_dwas["Task ID"]
)


# Identify tasks without a DWA mapping
tasks_without_dwas = (
    occupation_task_ids - mapped_task_ids
)


print(
    f"\nTotal occupation tasks: "
    f"{len(occupation_task_ids)}"
)

print(
    f"Tasks with at least one DWA: "
    f"{len(mapped_task_ids)}"
)

print(
    f"Tasks without a DWA mapping: "
    f"{len(tasks_without_dwas)}"
)

# --------------------------------------------------
# Find DWAs Connected to Multiple Tasks
# --------------------------------------------------

print("\n" + "=" * 60)
print("DWA CONVERGENCE ANALYSIS")
print("=" * 60)


# Count how many unique tasks map to each DWA
dwa_task_counts = (
    occupation_dwas
    .groupby(
        [
            "DWA Element ID",
            "DWA Element Name"
        ]
    )["Task ID"]
    .nunique()
    .reset_index(
        name="Connected Task Count"
    )
)


# Keep only DWAs connected to more than one task
shared_dwas = dwa_task_counts[
    dwa_task_counts["Connected Task Count"] > 1
]


if shared_dwas.empty:

    print(
        "\nNo DWAs are connected "
        "to more than one task."
    )

else:

    print(
        "\nDWAs connected to multiple tasks:\n"
    )

    print(
        shared_dwas.to_string(
            index=False
        )
    )

# --------------------------------------------------
# Skill Dataset Inventory
# --------------------------------------------------

print("\n" + "=" * 60)
print("SKILL DATASET INVENTORY")
print("=" * 60)


# --------------------------------------------------
# Essential Skills
# --------------------------------------------------

print("\n" + "-" * 60)
print("ESSENTIAL SKILLS")
print("-" * 60)

print("\nColumns:")
print(essential_skills.columns.tolist())

print("\nFirst 10 rows:")
print(essential_skills.head(10))

print("\nDataset shape:")
print(essential_skills.shape)


# --------------------------------------------------
# Soft Skills
# --------------------------------------------------

print("\n" + "-" * 60)
print("SOFTWARE SKILLS")
print("-" * 60)

print("\nColumns:")
print(software_skills.columns.tolist())

print("\nFirst 10 rows:")
print(software_skills.head(10))

print("\nDataset shape:")
print(software_skills.shape)


# --------------------------------------------------
# Transferable Skills
# --------------------------------------------------

print("\n" + "-" * 60)
print("TRANSFERABLE SKILLS")
print("-" * 60)

print("\nColumns:")
print(transferable_skills.columns.tolist())

print("\nFirst 10 rows:")
print(transferable_skills.head(10))

print("\nDataset shape:")
print(transferable_skills.shape)

# --------------------------------------------------
# Retrieve Essential Skills for Selected Occupation
# --------------------------------------------------

print("\n" + "=" * 60)
print("ESSENTIAL SKILLS RETRIEVAL")
print("=" * 60)


# Filter essential skills for the selected occupation
occupation_essential_skills = essential_skills[
    essential_skills["O*NET-SOC Code"] == occupation_code
]


print(f"\nOccupation: {matching_occupations.iloc[0]['Title']}")
print(f"O*NET-SOC Code: {occupation_code}")


print(
    f"\nSkill measurement records found: "
    f"{len(occupation_essential_skills)}"
)


print(
    f"Unique essential skills: "
    f"{occupation_essential_skills['Element ID'].nunique()}"
)


print("\nEssential Skills:\n")

print(
    occupation_essential_skills[
        [
            "Element ID",
            "Element Name",
            "Scale Name",
            "Data Value"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# Retrieve Transferable Skills for Selected Occupation
# --------------------------------------------------

print("\n" + "=" * 60)
print("TRANSFERABLE SKILLS RETRIEVAL")
print("=" * 60)


# Filter transferable skills for the selected occupation
occupation_transferable_skills = transferable_skills[
    transferable_skills["O*NET-SOC Code"] == occupation_code
]


print(f"\nOccupation: {matching_occupations.iloc[0]['Title']}")
print(f"O*NET-SOC Code: {occupation_code}")


print(
    f"\nSkill measurement records found: "
    f"{len(occupation_transferable_skills)}"
)


print(
    f"Unique transferable skills: "
    f"{occupation_transferable_skills['Element ID'].nunique()}"
)


print("\nTransferable Skills:\n")

print(
    occupation_transferable_skills[
        [
            "Element ID",
            "Element Name",
            "Scale Name",
            "Data Value"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# Retrieve Software Skills for Selected Occupation
# --------------------------------------------------

print("\n" + "=" * 60)
print("SOFTWARE SKILLS RETRIEVAL")
print("=" * 60)


# Filter software skills for the selected occupation
occupation_software_skills = software_skills[
    software_skills["O*NET-SOC Code"] == occupation_code
]


print(f"\nOccupation: {matching_occupations.iloc[0]['Title']}")
print(f"O*NET-SOC Code: {occupation_code}")


print(
    f"\nSoftware skill records found: "
    f"{len(occupation_software_skills)}"
)


print(
    f"Unique software categories: "
    f"{occupation_software_skills['Element ID'].nunique()}"
)


print(
    f"Unique workplace examples: "
    f"{occupation_software_skills['Workplace Example'].nunique()}"
)


print("\nSoftware Skills / Technologies:\n")

print(
    occupation_software_skills[
        [
            "Element ID",
            "Element Name",
            "Workplace Example",
            "Hot Technology",
            "In Demand"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# Software Technology Signal Analysis
# --------------------------------------------------

print("\n" + "=" * 60)
print("SOFTWARE TECHNOLOGY SIGNAL ANALYSIS")
print("=" * 60)


print("\nHot Technology counts:")
print(
    occupation_software_skills["Hot Technology"]
    .value_counts(dropna=False)
)


print("\nIn Demand counts:")
print(
    occupation_software_skills["In Demand"]
    .value_counts(dropna=False)
)


print("\nTechnologies marked as Hot Technology:\n")

hot_technologies = occupation_software_skills[
    occupation_software_skills["Hot Technology"] == "Y"
]

print(
    hot_technologies[
        [
            "Element Name",
            "Workplace Example",
            "In Demand"
        ]
    ].to_string(index=False)
)


print("\nTechnologies marked as In Demand:\n")

in_demand_technologies = occupation_software_skills[
    occupation_software_skills["In Demand"] == "Y"
]

print(
    in_demand_technologies[
        [
            "Element Name",
            "Workplace Example",
            "Hot Technology"
        ]
    ].to_string(index=False)
)