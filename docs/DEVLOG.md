# Development Log

## Project: AI Learning Pathway Engine

---
Proposed Phases
Phase 0 - Occupational Data Pipeline Structuring ← completed
Phase 1 — Data Discovery & Validation          ← completed
Phase 2 — Backend Architecture & Data Models   ← completed
Phase 3 — Occupation Profiling Engine          ← in progress
Phase 4 — User Skill Modeling
Phase 5 — Gap Analysis Engine
Phase 6 — Recommendation / Prioritization Logic
Phase 7 — API / Application Layer
Phase 8 — Professional UI & Visualization
Phase 9 — Testing, Evaluation & Deployment

# Phase names and number may change depending on what is needed to complete the engine. 
---
# Phase 1 — O*NET Data Discovery and Evidence Validation

### Objective

Evaluate whether O*NET occupational data can support an automated learning-pathway engine capable of identifying occupational requirements and eventually comparing them against a user's existing skills.

---

## Initial Data Exploration

The first stage focused on understanding the structure and relationships within the O*NET datasets.

### Occupation Dataset

The occupation dataset contains:

- 1,016 occupations
- O*NET-SOC Code
- Occupation Title
- Description

The O*NET-SOC Code was selected as the primary identifier for connecting occupational datasets.

---

## Task Dataset

The task dataset contains:

- 18,838 task records
- Task IDs
- Task descriptions
- Task types
- Occupation identifiers

Relationship validation showed:

- 1,016 unique occupations in the occupation dataset
- 923 occupations with associated tasks
- 0 task occupation codes missing from the occupation dataset

This confirmed that all task records could be linked to a valid occupation.

---

## Software Developers Test Case

The occupation:

- Software Developers
- O*NET-SOC Code: 15-1252.00

was selected as the initial test case.

The occupation contained:

- 17 tasks

---

## Task to Detailed Work Activity Mapping

Task-to-DWA data was added to investigate whether occupational tasks could be connected to more granular work activities.

For Software Developers:

- 17 total tasks
- 17 tasks with at least one DWA mapping
- 0 tasks without a DWA mapping
- 18 unique Detailed Work Activities

This provided complete task-to-DWA coverage for the Software Developers test case.

Several DWAs were connected to multiple tasks, indicating convergence between different occupational responsibilities.

---

## Skills Evidence

### Essential Skills

For Software Developers:

- 20 skill measurement records
- 10 unique skills

Each skill contains two measurements:

- Importance
- Level

An important modeling decision was identified:

**Importance and Level should not be directly compared because they represent different measurements.**

For example:

- Critical Thinking had the highest Importance score.
- Reading Comprehension had the highest Level score.

Future scoring logic will need to preserve this distinction.

---

### Transferable Skills

For Software Developers:

- 50 measurement records
- 25 unique skills

The highest Importance scores included:

1. Programming — 4.00
2. Judgment and Decision Making — 3.62
3. Systems Analysis — 3.50

This reinforced that the Software Developers occupation involves more than programming alone and includes decision-making and systems-level analysis.

---

## Technology Evidence

The Software Skills dataset was examined as a source of occupation-associated technologies.

For Software Developers:

- 430 technology records
- 67 software categories
- 430 unique workplace examples

The dataset includes:

- Broad technology categories
- Specific workplace examples
- Hot Technology signals
- In Demand signals

Initial inspection revealed that raw technology associations are too broad to directly generate learning recommendations.

For example, an occupation may be associated with hundreds of technologies, including technologies that are outdated, specialized, or only relevant to particular career paths.

---

# Key Engineering Decision

Raw occupational data will not be used directly as a learning curriculum.

The future engine will require additional transformation layers:

O*NET Evidence
↓
Occupation Profile
↓
Skill / Technology Normalization
↓
Specialization or Career Direction
↓
User Gap Analysis
↓
Prioritization
↓
Personalized Learning Pathway

---

# Current Status

Completed:

- Raw dataset ingestion
- Dataset inspection
- Occupation-to-task validation
- Task-to-DWA validation
- Essential skill inspection
- Transferable skill inspection
- Technology dataset inspection

Next:

Design backend data models. 

### Phase 2
Date: August 31 - September 8, 2026

Milestone: Building the Occupation Profile Service

I continued building the service layer for the AI Learning Pathway Engine.
The goal of this stage is to take the separate O*NET datasets and make it possible to retrieve a complete profile for a single occupation.

What I worked on:

1. Occupation Service
I built service functions that retrieve O*NET data by occupation code:

- get_occupation_by_code()
- get_tasks_by_code()
- get_dwas_by_code()
- get_essential_skills_by_code()
- get_transferable_skills_by_code()

I tested these functions using Software Developers (15-1252.00).
The functions successfully retrieve the corresponding records from the different O*NET datasets.

2. Occupation Profile
I created get_occupation_profile(), which combines the individual service functions into a single dictionary.
The resulting structure is:

{
    "occupation": DataFrame,
    "tasks": DataFrame,
    "dwas": DataFrame,
    "essential_skills": DataFrame,
    "transferable_skills": DataFrame
}

This helped clarify an important distinction for me: the overall profile is a Python dictionary, while the values inside the dictionary are still Pandas DataFrames.

3. Understanding O*NET Relationships
While working with the DWA data, I discovered that a task does not necessarily map to only one Detailed Work Activity (DWA).
A single task can be associated with multiple DWAs.
This means the tasks-to-DWAs dataset functions as a relationship/bridge table rather than a simple one-to-one mapping.
I need to preserve this relationship when designing the application's data model.

4. Beginning the Presentation Layer
I started thinking about how the raw O*NET data should be transformed before eventually being presented to users.
For example:
Tasks:
- Show the Task description
- Show the Task Type
- Hide unnecessary O*NET metadata from the user

DWAs:
- Extract unique DWA Element Names
- Convert them into a standard Python list

Essential Skills:
- Filter the dataset to Importance records
- Sort skills by Importance Data Value in descending order
- Eventually combine each skill's Importance and Level measurements

Transferable Skills:
- Eventually present the skill names as a simple alphabetical list

One important lesson from this process is that the raw dataset and the user-facing representation do not need to be identical.
The service layer can retrieve the raw data, while another layer can transform that data into a cleaner structure for the application.
What I learned:

- Python dictionaries can contain Pandas DataFrames as values.
- Pandas filtering works by comparing a DataFrame column to a value.
- Filtering and sorting are separate operations.
- O*NET task-to-DWA relationships are one-to-many rather than one-to-one.
- O*NET Essential Skills contain separate Importance and Level measurements, so I should not flatten or discard either one prematurely.
- Data retrieval and data presentation should be treated as separate concerns.

Current status:
The occupation profile retrieval is working successfully.
DWA transformation is working and now produces a standard Python list of unique DWA names.
Essential Skills transformation has been started. I successfully filtered the data to Importance records and identified that the next step is sorting those records by Data Value in descending order.

Next session:
- Finish Essential Skills transformation
- Match Importance and Level values for each skill
- Transform Transferable Skills into an alphabetical list
- Decide on the final structure of the user-facing occupation profile
- Add tests for the occupation profile transformations

## 2026-09-17 — Transferable Skills Transformation & Testing

### Goal
Separate O*NET transferable-skill transformation logic from the occupation profile service and establish automated checks for the transformed output.

### Work Completed
- Created `src/data/transformations.py` to hold data transformation logic.
- Moved `transform_transferable_skills()` out of `services/occupation_profile.py`.
- Transformation now:
  - Separates O*NET Importance and Level records.
  - Renames `Data Value` to `Importance` and `Level`.
  - Merges Importance and Level by `Element Name`.
  - Sorts skills by Importance in descending order.
  - Adds a sequential Rank from 1 onward.
  - Returns `Rank`, `Element Name`, `Importance`, and `Level`.
- Added validation for empty transferable-skill input using `ValueError`.
- Created `src/test_transformations.py`.
- Added assertions verifying:
  - The transformed DataFrame is not empty.
  - 25 transferable skills are returned for Software Developers.
  - The expected columns are present in the expected order.
  - Programming is ranked first.
  - Empty transferable-skill input raises the expected `ValueError`.

### Validation
Tested with O*NET occupation code `15-1252.00` (Software Developers).

Expected result:
- 25 transferable skills
- Programming ranked #1
- Repairing ranked #25
- All transformation assertions passed.
- Empty-input error test passed.

### Debugging Lesson
Encountered a `NoneType` error because the transformation function had accidentally been duplicated inside `test_transformations.py`. The duplicate function shadowed the imported implementation and omitted its return statement.

Lesson: keep implementation logic in the module being tested; test files should import and exercise that logic rather than redefine it.

### Architectural Note
The current separation is:

O*NET raw data
→ data loader
→ occupation service
→ occupation profile
→ data transformations
→ tests

This keeps retrieval, profile assembly, transformation, and testing responsibilities separate.

Phase 3 — Software Skills Transformation 
**Focus:** O*NET software skills data retrieval, transformation, and validation  
**Status:** In progress

### Accomplished

**1. Validated software skills retrieval**
- Retrieved software skills for Software Developers using O*NET-SOC code `15-1252.00`.
- Confirmed that the raw dataset contains 430 records and includes the columns `O*NET-SOC Code`, `Element Name`, `Workplace Example`, `Hot Technology`, and `In Demand`.
- Verified that filtering by occupation code returns the expected records.

**2. Implemented the initial transformation**
- Created `transform_software_skills()` in `src/data/transformations.py`.
- Initially grouped records by `Element Name` and combined workplace examples into comma-separated strings.
- Tested the output and confirmed that the transformation produced a non-empty DataFrame with unique categories.

**3. Identified a data-integrity concern**
- Determined that `Hot Technology` and `In Demand` are associated with individual workplace examples.
- Recognized that combining examples into a single string would discard the relationship between each example and its flags.
- Decided to retain one row per software category while preserving the full information for each example.

**4. Developed an improved transformation approach**
- Grouped the data by `Element Name` while retaining `Workplace Example`, `Hot Technology`, and `In Demand`.
- Used `to_dict(orient="records")` to convert each category's rows into a list of dictionaries.
- Named the resulting column `Workplace Examples`.
- Used `reset_index()` to convert the category index into a regular DataFrame column.
- Confirmed that the intermediate result is a DataFrame with the intended columns: `Element Name` and `Workplace Examples`.

### Testing and validation

- Ran `python src/test_transformations.py` successfully with no assertion errors before beginning the revised transformation inspection.
- Verified that the revised approach produces a DataFrame rather than a Series.
- Currently inspecting the contents of an individual category to confirm that every example retains all three fields: `Workplace Example`, `Hot Technology`, and `In Demand`.

### Current state

The improved transformation logic has been explored and tested interactively, but it still needs to be incorporated into `transform_software_skills()` and covered by automated assertions.
The current automated tests should be rerun after integration.

### Next steps

1. Inspect one category's complete list of example dictionaries.
2. Update `transform_software_skills()` to use the improved grouping and conversion logic.
3. Update automated tests to verify the output columns, unique categories, expected dictionary keys, and preserved flag values.
4. Consider how the transformed software skills should be incorporated into the occupation profile service.
5. Revisit how the user interface should display technology and demand flags without overwhelming users with raw data.

### Key learning
The transformation layer should preserve meaningful source relationships instead of discarding information simply to make the output easier to display. 
The application can simplify presentation later while retaining the underlying data needed for filtering, analysis, and future features.

## Milestone
Software-skills transformation is integrated into the occupation profile, validated by tests, committed, and pushed to GitHub

## 2026-11-13 Development Progress

### User Skill Modeling: Skill Conflict Review and Resolution

**Status: Core review-resolution logic implemented and tested.**

Continued development of the user skill modeling service in `src/services/user_profile.py`.

#### Implemented
- Skill name normalization using `strip()` and `casefold()` to support consistent comparisons.
- Skill submission classification into `NEW`, `DUPLICATE`, and `CONFLICT`.
- Conflict review creation for skills submitted with a different proficiency level.
- New skill addition to the user's profile.
- Human-readable conflict messages displaying existing and proposed proficiency levels.
- Conflict review resolution with three possible statuses:
  - `PENDING`
  - `ACCEPTED`
  - `DECLINED`

#### Review Resolution Behavior
- **Accepted:** Updates the existing skill's proficiency to the proposed proficiency.
- **Declined:** Preserves the existing skill's proficiency.
- **Already resolved:** Rejects attempts to resolve a review more than once.
- **Invalid decision:** Rejects `PENDING` as a resolution decision and prevents unintended changes to the profile or review.

#### Testing
Successfully tested the review-resolution scenarios:
- Accepted review
- Declined review
- Attempt to resolve an already-resolved review
- Attempt to resolve using an invalid decision

All tests passed.

#### Engineering Considerations
- Prevents duplicate skill entries when proficiency conflicts occur.
- Preserves the existing skill until a conflict is explicitly resolved.
- Uses Enum values to represent skill proficiency and review status.
- Uses exception handling to reject invalid operations.

#### Next Steps
- Review the complete skill-submission workflow.
- Verify that classification, conflict detection, review creation, and resolution work together correctly.
- Continue toward the skill-gap analysis component.

# Sub-Phase: Skill Model Separation and Canonical ID Refactor

**Date:** November 18, 2026  
**Milestone:** Separation of Canonical Skills and User Skills

## 1. Objective

- Refactor the skill data models to distinguish canonical skill definitions from individual users' proficiency records.
- The previous design used one `Skill` model for both purposes. This created potential ambiguity between a skill's identity and a user's relationship to that skill.
- The objective was to establish a canonical skill identity that could be referenced consistently across multiple user profiles.

## 2. Architectural Changes

### Canonical Skill Model

Redefined `models/skill.py` to represent skills independently of individual users.

Fields:
- `skill_id`: Unique, stable identifier assigned by the Skill Registry.
- `name`: Official skill name.
- `aliases`: Alternative names and common spellings.
- `description`: Definition of the skill.
- `category`: Skill classification.

The registry will eventually generate IDs when proposed skills receive approval and are registered.

### UserSkill Model

Created `models/user_skill.py` by separating the original user-specific `Skill` model and renaming it to `UserSkill`.

Updated fields:
- `skill_id`: Reference to the canonical skill.
- `proficiency`: User's proficiency level.
- `source`: Origin of the proficiency information.

Removed `name` because the canonical Skill Registry will serve as the single source of truth for skill names.

### Dependent Model Updates

Updated the following models to reference `UserSkill`:

- `UserProfile`
- `SkillCheckResult`
- `SkillReview`

Updated corresponding service imports, type annotations, and test fixtures.

## 3. User Profile Service Refactor

Updated `classify_skill_submission()` to compare canonical `skill_id` values rather than normalized skill names.
The classification logic retains three possible outcomes:

| Status | Condition |
|---|---|
| NEW | No matching canonical skill ID exists in the profile. |
| DUPLICATE | Matching skill ID and proficiency already exist. |
| CONFLICT | Matching skill ID exists, but the submitted proficiency differs. |

Removed `normalize_skill_name()` and its associated usage because name resolution will become the responsibility of the Skill Registry.
This establishes a clearer separation of concerns:

- Skill Registry: Skill identity, name resolution, and aliases.
- User Profile Service: User-specific skill records and proficiency management.

## 4. Testing and Validation

- Updated existing test fixtures to construct `UserSkill` objects using `skill_id`.
- Updated model and service references.
- Removed obsolete name-normalization dependencies.
- Executed the full test suite using `python -m pytest -v`.

**Result: All tests passing.**

The existing user-profile classification and conflict-review workflows remain functional following the refactor.

## 5. Architectural Decisions

The following decisions were established:

1. Canonical skills and user-specific skill records remain separate models.
2. The Skill Registry owns canonical skill ID generation.
3. Canonical IDs are stable and independent of skill names.
4. User profiles reference canonical skills through `skill_id`.
5. Name normalization and alias resolution belong to the Skill Registry, not the User Profile Service.
6. The application continues to follow a modular monolith architecture.

## 6. Outstanding Work

The following functionality has not yet been implemented:

- Skill Registry service.
- Canonical skill lookup by name and alias.
- Canonical skill ID generation.
- Registry integration with user skill submissions.
- Skill proposal and approval workflows.
- Governance controls for registering new canonical skills.

## 7. Next Development Milestone

**Build the Skill Registry Service.**

The next implementation phase will establish how submitted skill names are resolved to canonical skill records before being passed to the User Profile Service.
The intended workflow:

1. Receive a submitted skill name.
2. Search canonical skill names and aliases.
3. Resolve the matching canonical skill.
4. Retrieve its `skill_id`.
5. Create or classify the corresponding `UserSkill`.

Unknown skills will eventually enter the AI-assisted proposal and governance workflow rather than being automatically registered.
---
**Milestone Status:** Completed — Model separation and ID-based classification validated by the existing test suite.

## 26-11-20 — Project Organization and Package Configuration

### Objective
Reorganize the application into a structured Python package while preserving existing functionality and test coverage.

### Changes Made

**1. Reorganized the project structure**
- Created `src/ai_learning_pathway/` as the main application package.
- Organized application code into `data/`, `models/`, and `services/` subpackages.
- Added `__init__.py` files to establish Python packages.
- Moved exploratory scripts into the root-level `exploratory/` directory.
- Kept raw and processed datasets outside the application source directory.
- Kept the test suite in the root-level `tests/` directory.

**2. Configured Python packaging**
- Created `pyproject.toml`.
- Configured `setuptools` as the build backend.
- Defined project metadata, version `0.1.0`, and minimum Python version `3.13`.
- Configured package discovery to locate `ai_learning_pathway` under `src/`.
- Installed the project in editable mode using `python -m pip install -e .`.

**3. Corrected data path resolution**
- Updated `PROJECT_ROOT` in `src/ai_learning_pathway/data/loader.py`.
- Changed the parent directory reference from `parents[2]` to `parents[3]` to correctly resolve the repository root.
- Verified that `RAW_DATA_DIR` points to the root-level `data/raw/` directory.

### Verification

- Confirmed Python can import `ai_learning_pathway` from the correct source directory.
- Confirmed the raw data directory exists and resolves correctly.
- Ran the full test suite using `python -m pytest -v`.
- **Result: All 25 tests passed.**

### Key Concepts Learned
- Python package structure and the `src/` layout.
- TOML syntax and the purpose of `pyproject.toml`.
- Build systems, build backends, and package discovery.
- Editable package installation.
- Absolute filesystem paths and `pathlib.Path`.
- Regression testing after structural refactoring.

### Outcome
The project now has a structured, installable Python package. Existing functionality remains intact, and all 25 tests pass following the reorganization.