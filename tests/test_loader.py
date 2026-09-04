from data.loader import (
    load_occupations,
    load_task_statements,
    load_essential_skills,
)


occupations = load_occupations()
tasks = load_task_statements()
essential_skills = load_essential_skills()

print(f"Occupation rows: {len(occupations)}")
print(f"Task rows: {len(tasks)}")
print(f"Essential skill records: {len(essential_skills)}")