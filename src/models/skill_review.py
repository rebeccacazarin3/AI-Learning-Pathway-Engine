
from dataclasses import dataclass
from models.review_status import ReviewStatus
from models.skill import Skill

@dataclass
class SkillReview:
    existing_skill: Skill
    proposed_skill: Skill
    category: str
    reason: str
    review_status: ReviewStatus = ReviewStatus.PENDING

