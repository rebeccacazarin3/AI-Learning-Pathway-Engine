from models.user_skill import UserSkill
from models.skill_check_result import SkillCheckResult
from models.user_profile_model import UserProfile
from models.skill_check_status import SkillCheckStatus
from models.skill_review import SkillReview
from models.review_status import ReviewStatus

def normalize_skill_name(skill_name: str) -> str:
    """
    Normalize the skill name by removing leading/trailing whitespace and converting to lowercase.
    
    Args:
    skill_name (str): The skill name to normalize.

    Returns:
    str: The normalized skill name.
    """
    return skill_name.strip().casefold()

def classify_skill_submission(profile : UserProfile, proposed_skill : UserSkill) -> SkillCheckResult:
    for existing_skill in profile.skills:
        if normalize_skill_name(existing_skill.skill_id) == normalize_skill_name(proposed_skill.skill_id):
            if existing_skill.proficiency == proposed_skill.proficiency:
                return SkillCheckResult(
                    status=SkillCheckStatus.DUPLICATE,
                    proposed_skill=proposed_skill,
                    existing_skill=existing_skill
                )
            else:
                return SkillCheckResult(
                    status=SkillCheckStatus.CONFLICT,
                    proposed_skill=proposed_skill,
                    existing_skill=existing_skill
                )
    return SkillCheckResult(
        status=SkillCheckStatus.NEW,
        proposed_skill=proposed_skill
    )

def create_skill_review(
        skill_check_result: SkillCheckResult,
        category: str,
        reason: str
    ) -> SkillReview:

    if skill_check_result.status != SkillCheckStatus.CONFLICT:
        raise ValueError("A skill review can only be created for a conflict.")

    review = SkillReview(
        existing_skill=skill_check_result.existing_skill,
        proposed_skill=skill_check_result.proposed_skill,
        category=category,
        reason=reason
    )

    return review

def add_new_skill(
        profile: UserProfile,
        skill_check_result: SkillCheckResult
    ) -> UserProfile:
    
    if skill_check_result.status == SkillCheckStatus.NEW:
        profile.skills.append(skill_check_result.proposed_skill)
    else:
        raise ValueError("Only new skills can be added.")
    return profile

def add_new_skill(
        profile: UserProfile,
        skill_check_result: SkillCheckResult
    ) -> UserProfile:
    
    if skill_check_result.status == SkillCheckStatus.NEW:
        profile.skills.append(skill_check_result.proposed_skill)
    else:
        raise ValueError("Only new skills can be added.")
    return profile

def generate_conflict_message(skill_check_result) -> str:
    #Verify that the status is CONFLICT, if not raise an error
    if skill_check_result.status != SkillCheckStatus.CONFLICT:
        raise ValueError("A conflict message can only be created for a conflict.")
    
    #Retrive the skill name and the both proficiency levels from the SkillCheckResult
    
    skill_name = skill_check_result.existing_skill.skill_id
    existing_proficiency = skill_check_result.existing_skill.proficiency.value
    proposed_proficiency = skill_check_result.proposed_skill.proficiency.value

    #Generate a message that states the conflict that includes the skill name, existing proficiency, and proposed proficiency.
    message = (
        f"You already have {skill_name} recorded as {existing_proficiency}, "
        f"but your new submission indicates {proposed_proficiency}. "
        "Please review this discrepancy before updating your profile."
    )
    return message

def resolve_skill_review(profile, skill_review, decision):

    if skill_review.review_status != ReviewStatus.PENDING:
        raise ValueError("Only pending reviews can be resolved.")

    if decision not in (ReviewStatus.ACCEPTED, ReviewStatus.DECLINED):
        raise ValueError("Decision must be ACCEPTED or DECLINED.")

    if decision == ReviewStatus.ACCEPTED:
        # Update the existing skill's proficiency here
        skill_review.existing_skill.proficiency = skill_review.proposed_skill.proficiency

    # Update the review status here
    skill_review.review_status = decision

    return profile