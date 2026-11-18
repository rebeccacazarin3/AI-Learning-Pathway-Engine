from models.skill_check_result import SkillCheckResult
from models.user_skill import UserSkill
from models.proficiency import ProficiencyLevel
from models.skill_check_status import SkillCheckStatus
from services.user_profile import generate_conflict_message
import pytest


def test_skill_check_result_new():
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )

    result = SkillCheckResult(
        status=SkillCheckStatus.NEW,
        proposed_skill=proposed_skill
    )

    assert result.status == SkillCheckStatus.NEW
    assert result.proposed_skill == proposed_skill
    assert result.existing_skill is None


def test_skill_check_result_duplicate():
    existing_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )

    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )

    result = SkillCheckResult(
        status=SkillCheckStatus.DUPLICATE,
        proposed_skill=proposed_skill,
        existing_skill=existing_skill
    )

    assert result.status == SkillCheckStatus.DUPLICATE
    assert result.proposed_skill == proposed_skill
    assert result.existing_skill == existing_skill


def test_skill_check_result_conflict():
    existing_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )

    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.ADVANCED,
        source="Self-assessment"
    )

    result = SkillCheckResult(
        status=SkillCheckStatus.CONFLICT,
        proposed_skill=proposed_skill,
        existing_skill=existing_skill
    )

    assert result.status == SkillCheckStatus.CONFLICT
    assert result.proposed_skill == proposed_skill
    assert result.existing_skill == existing_skill


def test_generate_conflict_message():
    existing_profile = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )

    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )

    #Use SkillCheckResult to isolate the fuction that is being tested.
    result_message_check = SkillCheckResult(
        status=SkillCheckStatus.CONFLICT,
        proposed_skill=proposed_skill,
        existing_skill=existing_profile
    )

    # Call generate_conflict_message() and pass the SkillCheckResult object.
    # Store the returned message in the message variable.
    message = generate_conflict_message(result_message_check)

    # Verify that the message contains the skill name and both proficiency levels.
    assert "SKL-001" in message
    assert "Beginner" in message
    assert "Intermediate" in message

def test_generate_conflict_message_rejects_new_skill():
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )

    new_skill = SkillCheckResult(
        status=SkillCheckStatus.NEW,
        proposed_skill=proposed_skill
    )

    with pytest.raises(ValueError):
        generate_conflict_message(new_skill)

def test_generate_conflict_message_rejects_duplicate_skill():
    duplicate_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )
    result_duplicate = SkillCheckResult(
        status=SkillCheckStatus.DUPLICATE,
        proposed_skill=duplicate_skill,
    )

    with pytest.raises(ValueError):
        generate_conflict_message(result_duplicate)

