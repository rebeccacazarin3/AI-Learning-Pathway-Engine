from enum import Enum


class ReviewStatus(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    SUPERSEDED = "Superseded"

#Superseded would keep historical records but replace the review for a newer review