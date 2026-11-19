from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV file from the project's raw data directory.

    Args:
        filename: Name of the CSV file to load.

    Returns:
        A pandas DataFrame containing the CSV data.
    """

    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Could not find data file: {file_path}"
        )

    return pd.read_csv(file_path)


def load_occupations() -> pd.DataFrame:
    return load_csv("occupation_data.csv")


def load_task_statements() -> pd.DataFrame:
    return load_csv("task_statements.csv")


def load_tasks_to_dwas() -> pd.DataFrame:
    return load_csv("tasks_to_dwas.csv")


def load_essential_skills() -> pd.DataFrame:
    return load_csv("essential_skills.csv")


def load_transferable_skills() -> pd.DataFrame:
    return load_csv("transferable_skills.csv")


def load_software_skills() -> pd.DataFrame:
    return load_csv("software_skills.csv")