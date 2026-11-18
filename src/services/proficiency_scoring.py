from models.proficiency import ProficiencyLevel


# TODO: Define and validate the numerical representation
# of each proficiency level before implementing scoring.
PROFICIENCY_SCORES = {}


def proficiency_to_score(proficiency: ProficiencyLevel) -> int:
    """
    Convert a user's proficiency level into a numerical representation.

    The scoring scale is currently under development.

    Args:
        proficiency: The user's self-assessed proficiency level.

    Returns:
        An integer representing the proficiency level.

    Raises:
        NotImplementedError: Until the scoring scale is established.
    """
    raise NotImplementedError(
        "Proficiency scoring has not been implemented yet."
    )