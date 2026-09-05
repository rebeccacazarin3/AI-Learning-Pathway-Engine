from data.loader import (
    load_essential_skills,
    load_occupations,
    load_task_statements,
    load_tasks_to_dwas,
    load_transferable_skills,
)

def get_occupation_by_code(occupation_code):
    """
    Retrieve occupation data by occupation code.

    Args:
        occupation_code: The O*NET-SOC code of the occupation to retrieve.

    Returns:
        A pandas DataFrame containing the occupation data
        for the specified code.
    """
    occupations_df = load_occupations()

    occupation_data = occupations_df[
        occupations_df["O*NET-SOC Code"] == occupation_code
    ]

    if occupation_data.empty:
        raise ValueError(
            f"No occupation found with code: {occupation_code}"
        )

    return occupation_data

def get_tasks_by_code(occupation_code):
    """
    Retrieve task statements associated with a specific occupation code.

    Args:
        occupation_code: The O*NET-SOC code of the occupation to retrieve tasks for.

    Returns:
        A pandas DataFrame containing the task statements
        for the specified occupation code.
    """
    tasks_df = load_task_statements()

    tasks_data = tasks_df[
        tasks_df["O*NET-SOC Code"] == occupation_code
    ]

    if tasks_data.empty:
        raise ValueError(
            f"No tasks found for occupation code: {occupation_code}"
        )

    return tasks_data


def get_dwas_by_code(occupation_code):
    """
    Retrieve DWAs (Detailed Work Activities) associated with a specific occupation code.

    Args:
        occupation_code: The O*NET-SOC code of the occupation to retrieve DWAs for.

    Returns:
        A pandas DataFrame containing the DWAs
        for the specified occupation code.
    """
    dwas_df = load_tasks_to_dwas()

    dwas_data = dwas_df[
        dwas_df["O*NET-SOC Code"] == occupation_code
    ]

    if dwas_data.empty:
        raise ValueError(
            f"No DWAs found for occupation code: {occupation_code}"
        )

    return dwas_data

def get_essential_skills_by_code(occupation_code):
    """
    Retrieve essential skills associated with a specific occupation code.

    Args:
        occupation_code: The O*NET-SOC code of the occupation to retrieve essential skills for.

    Returns:
        A pandas DataFrame containing the essential skills
        for the specified occupation code.
    """
    essential_skills_df = load_essential_skills()

    essential_skills_data = essential_skills_df[
        essential_skills_df["O*NET-SOC Code"] == occupation_code
    ]

    if essential_skills_data.empty:
        raise ValueError(
            f"No essential skills found for occupation code: {occupation_code}"
        )

    return essential_skills_data

def get_transferable_skills_by_code(occupation_code):
    """
    Retrieve transferable skills associated with a specific occupation code.

    Args:
        occupation_code: The O*NET-SOC code of the occupation to retrieve transferable skills for.

    Returns:
        A pandas DataFrame containing the transferable skills
        for the specified occupation code.
    """
    transferable_skills_df = load_transferable_skills()

    transferable_skills_data = transferable_skills_df[
        transferable_skills_df["O*NET-SOC Code"] == occupation_code
    ]

    if transferable_skills_data.empty:
        raise ValueError(
            f"No transferable skills found for occupation code: {occupation_code}"
        )

    return transferable_skills_data
















essential_skills = get_essential_skills_by_code("15-1252.00")
occupation = get_occupation_by_code("15-1252.00")
tasks = get_tasks_by_code("15-1252.00")
dwas = get_dwas_by_code("15-1252.00")
transferable_skills = get_transferable_skills_by_code("15-1252.00")

print(get_occupation_by_code("15-1256.00"))
print(get_tasks_by_code("15-1256.00"))
print(get_dwas_by_code("15-1256.00"))
print(get_essential_skills_by_code("15-1256.00"))
print(get_transferable_skills_by_code("15-1256.00"))