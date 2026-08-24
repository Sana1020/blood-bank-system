def calculate_ranking_score(
    compatibility_score: float,
    distance_km: float,
    urgency: str,
) -> float:
    """
    Calculate a priority score for a potential donor.

    Higher score = better donor candidate.
    """

    compatibility_score = max(
        0,
        min(100, compatibility_score)
    )

    
    distance_score = max(
        0,
        100 - (distance_km * 5)
    )

    
    urgency_scores = {
        "Emergency": 100,
        "Urgent": 70,
        "Normal": 40,
    }

    urgency_score = urgency_scores.get(
        urgency,
        40
    )

    
    final_score = (
        compatibility_score * 0.5
        + distance_score * 0.3
        + urgency_score * 0.2
    )

    return round(final_score, 2)