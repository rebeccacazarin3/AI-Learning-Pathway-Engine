from dataclasses import dataclass
from models.review_status import ReviewStatus
from models.user_skill import UserSkill

@dataclass
class SkillReview:
    existing_skill: UserSkill
    proposed_skill: UserSkill
    category: str
    reason: str
    review_status: ReviewStatus = ReviewStatus.PENDING

