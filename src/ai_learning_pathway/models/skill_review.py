from dataclasses import dataclass
from ai_learning_pathway.models.review_status import ReviewStatus
from ai_learning_pathway.models.user_skill import UserSkill

@dataclass
class SkillReview:
    existing_skill: UserSkill
    proposed_skill: UserSkill
    category: str
    reason: str
    review_status: ReviewStatus = ReviewStatus.PENDING

