import pytest
from ai_learning_pathway.models import skill
from ai_learning_pathway.models.review_status import ReviewStatus
from ai_learning_pathway.services.user_profile import classify_skill_submission, create_skill_review, add_new_skill, resolve_skill_review
from ai_learning_pathway.models.user_profile_model import UserProfile
from ai_learning_pathway.models.user_skill import UserSkill
from ai_learning_pathway.models.proficiency import ProficiencyLevel
from ai_learning_pathway.models.skill_check_status import SkillCheckStatus
from ai_learning_pathway.models.skill_review import SkillReview

def test_classify_skill_submission_new():
    profile_new = UserProfile()
    skill= UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )
    
    result = classify_skill_submission(profile_new, skill)
    assert result.status == SkillCheckStatus.NEW
    assert result.proposed_skill == skill
    assert result.existing_skill is None


def test_classify_skill_submission_duplicate():
    profile_duplicate = UserProfile(
        skills = [UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.BEGINNER,
            source="Self-assessment"
        )]
    )

    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )
    
    result = classify_skill_submission(profile_duplicate, proposed_skill)
    assert result.status == SkillCheckStatus.DUPLICATE
    assert result.proposed_skill == proposed_skill
    assert result.existing_skill == profile_duplicate.skills[0]

def test_classify_skill_submission_conflict():
    profile_conflict = UserProfile(
        skills = [UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.BEGINNER,
            source="Self-assessment"
        )]
    )
    
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )

    result = classify_skill_submission(profile_conflict, proposed_skill)
    assert result.status == SkillCheckStatus.CONFLICT
    assert result.proposed_skill == proposed_skill
    assert result.existing_skill == profile_conflict.skills[0]
    assert result.existing_skill.proficiency == ProficiencyLevel.BEGINNER
    assert profile_conflict.skills[0].proficiency == ProficiencyLevel.BEGINNER


def test_create_skill_review():
    profile_conflict = UserProfile(
        skills = [UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.BEGINNER,
            source="Self-assessment"
        )]
    )
    
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )

    skill_check_result = classify_skill_submission(profile_conflict, proposed_skill)
    
    review = create_skill_review(skill_check_result, category="Proficiency Conflict", reason="Submitted proficiency differs from the existing proficiency.")
    
    assert review.existing_skill == profile_conflict.skills[0]
    assert review.proposed_skill == proposed_skill
    assert review.category == "Proficiency Conflict"
    assert review.reason == "Submitted proficiency differs from the existing proficiency."
    assert review.review_status == ReviewStatus.PENDING
    assert profile_conflict.skills[0].proficiency == ProficiencyLevel.BEGINNER


def test_create_skill_review_rejects_new_skill():
    #create a profile with no existing skills
    profile_new = UserProfile(
        skills = []
    )
    #Create a proposed skill that is new such as Python with proficiency level BEGINNER
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )
    #Pass the resulting SkillChecckResult into the create_skill_review function and assert that it raises a ValueError
    skill_check_result = classify_skill_submission(profile_new, proposed_skill)
    
    assert skill_check_result.status == SkillCheckStatus.NEW
    
    with pytest.raises(ValueError):
        create_skill_review(skill_check_result, category="Proficiency Conflict", reason="Submitted proficiency differs from the existing proficiency.")


def test_create_skill_review_rejects_duplicate_skill():
    #create a profile with an existing skill of Intermediate Python
    profile_duplicate = UserProfile(
        skills = [UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.INTERMEDIATE,
            source="Self-assessment"
        )]
    )
    #Create a proposed skill that is a duplicate such as Python with proficiency level INTERMEDIATE
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )
    #Pass the resulting SkillChecckResult into the create_skill_review function and assert that it raises a ValueError
    skill_check_result = classify_skill_submission(profile_duplicate, proposed_skill)
    
    assert skill_check_result.status == SkillCheckStatus.DUPLICATE
    
    with pytest.raises(ValueError):
        create_skill_review(skill_check_result, category="Proficiency Conflict", reason="Submitted proficiency is the same as the existing proficiency.")


def test_add_new_skill():
    #create a profile
    profile_new_skill = UserProfile(
        skills = [UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.INTERMEDIATE,
            source="Self-assessment"
        )]
    )
    # Create a proposed skill
    proposed_skill = UserSkill(
        skill_id="SKL-002",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )
    # Add the classification result 
    skill_check_result = classify_skill_submission(profile_new_skill, proposed_skill)

    assert skill_check_result.status == SkillCheckStatus.NEW
    assert skill_check_result.proposed_skill == proposed_skill

    updated_profile = add_new_skill(profile_new_skill, skill_check_result)
    assert skill_check_result.proposed_skill in updated_profile.skills
    assert updated_profile is profile_new_skill

def test_add_new_skill_rejects_duplicate():
    #create a duplicate profile
    profile_duplicate = UserProfile(
        skills = [UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.INTERMEDIATE,
            source="Self-assessment"
        )]
    )
    # Create a proposed skill duplicate
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )
    # Add the classification result 
    skill_check_result = classify_skill_submission(profile_duplicate, proposed_skill)

    assert skill_check_result.status == SkillCheckStatus.DUPLICATE
    assert skill_check_result.proposed_skill == proposed_skill

    with pytest.raises(ValueError):
        add_new_skill(profile_duplicate, skill_check_result)
        assert len(profile_duplicate.skills) == 1
        assert profile_duplicate.skills[0].proficiency == ProficiencyLevel.INTERMEDIATE

def test_add_new_skill_rejects_conflict():
    #create a conflict profile
    profile_conflict = UserProfile(
        skills = [UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.BEGINNER,
            source="Self-assessment"
        )]
    )
    # Create a proposed skill conflict
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.INTERMEDIATE,
        source="Self-assessment"
    )
    # Add the classification result 
    skill_check_result = classify_skill_submission(profile_conflict, proposed_skill)
    assert skill_check_result.status == SkillCheckStatus.CONFLICT
    assert skill_check_result.proposed_skill == proposed_skill

    with pytest.raises(ValueError):
        add_new_skill(profile_conflict, skill_check_result)
    
    assert len(profile_conflict.skills) == 1
    assert profile_conflict.skills[0].proficiency == ProficiencyLevel.BEGINNER

def test_resolve_skill_review():
    #Create a profile with python of beginner
    existing_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )
    #Create a profile with python advanced
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.ADVANCED,
        source="Self-assessment"
    )

    user_profile = UserProfile(
        skills = [existing_skill]
    )

    skill_review = SkillReview (
      existing_skill = existing_skill,
      proposed_skill = proposed_skill,
      category = "Software Applications",
      reason = "User submitted a different proficiency level for an existing skill"
    )

    updated_profile = resolve_skill_review(
        user_profile,
        skill_review,
        decision=ReviewStatus.ACCEPTED
    )

    assert updated_profile.skills[0].proficiency == ProficiencyLevel.ADVANCED
    assert skill_review.review_status == ReviewStatus.ACCEPTED
    assert len(updated_profile.skills) == 1

def test_resolve_skill_review_declined():
    #Create a profile with python of beginner
    existing_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.BEGINNER,
        source="Self-assessment"
    )
    #Create a profile with python advanced
    proposed_skill = UserSkill(
        skill_id="SKL-001",
        proficiency=ProficiencyLevel.ADVANCED,
        source="Self-assessment"
    )

    user_profile = UserProfile(
        skills = [existing_skill]
    )

    skill_review = SkillReview (
      existing_skill = existing_skill,
      proposed_skill = proposed_skill,
      category = "Software Applications",
      reason = "User submitted a different proficiency level for an existing skill"
    )

    updated_profile = resolve_skill_review(
        user_profile,
        skill_review,
        decision=ReviewStatus.DECLINED
    )

    assert updated_profile.skills[0].proficiency == ProficiencyLevel.BEGINNER
    assert skill_review.review_status == ReviewStatus.DECLINED
    assert len(updated_profile.skills) == 1

def test_resolve_skill_review_rejects_non_pending():
        #Create a profile with python of beginner
        existing_skill = UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.BEGINNER,
            source="Self-assessment"
        )
        #Create a profile with python advanced
        proposed_skill = UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.ADVANCED,
            source="Self-assessment"
        )
    
        user_profile = UserProfile(
            skills = [existing_skill]
        )
    
        skill_review = SkillReview (
          existing_skill = existing_skill,
          proposed_skill = proposed_skill,
          category = "Software Applications",
          reason = "User submitted a different proficiency level for an existing skill"
        )

        #User accepts the review
        updated_profile = resolve_skill_review(
            user_profile,
            skill_review,
            decision=ReviewStatus.ACCEPTED
        )

        #Reject an already-resolved review
        with pytest.raises(ValueError):
            resolve_skill_review(updated_profile, skill_review, ReviewStatus.ACCEPTED)

def test_resolve_skill_review_rejects_invalid_decision():
    #Create a profile with python of beginner
        existing_skill = UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.BEGINNER,
            source="Self-assessment"
        )
        #Create a profile with python advanced
        proposed_skill = UserSkill(
            skill_id="SKL-001",
            proficiency=ProficiencyLevel.ADVANCED,
            source="Self-assessment"
        )
    
        user_profile = UserProfile(
            skills = [existing_skill]
        )
    
        skill_review = SkillReview (
          existing_skill = existing_skill,
          proposed_skill = proposed_skill,
          category = "Software Applications",
          reason = "User submitted a different proficiency level for an existing skill"
        )

        with pytest.raises(ValueError):
            resolve_skill_review(
            user_profile,
            skill_review,
            decision=ReviewStatus.PENDING
        )

        #assert that the skill proficiency has not changed
        assert user_profile.skills[0].proficiency == ProficiencyLevel.BEGINNER
        assert  skill_review.review_status == ReviewStatus.PENDING
