from sqlalchemy.orm import Session

from ..algorithms.compatibility import is_compatible
from ..algorithms.distance import calculate_distance
from ..algorithms.eligibility import is_eligible
from ..algorithms.ranking import calculate_ranking_score
from ..database.crud import (
    get_blood_request,
    get_all_donors,
    create_match,
    delete_matches_by_request,
)


def find_matches(session: Session, request_id: int, max_matches_per_request: int = 5):
    """
    Find, rank, and save eligible donors for a blood request.
    """
    request = get_blood_request(session, request_id)
    if request is None:
        return []

    # 1. Remove previous matches for this request
    delete_matches_by_request(session, request_id)

    # 2. Retrieve all donors from database

    donors = get_all_donors(session)
    candidates = []

    for donor in donors:
        # Check donor eligibility (Age, availability, donation interval)
        if not is_eligible(
                donor.age,
                donor.is_available,
                donor.last_donation_date,
        ):
            continue

        # Check blood type compatibility
        if not is_compatible(
                donor.blood_type,
                request.blood_type,
        ):
            continue

        # Calculate distance between donor and request location
        distance_km = calculate_distance(
            donor.latitude,
            donor.longitude,
            request.latitude,
            request.longitude,
        )

        compatibility_score = 100.0

        # Calculate ranking score based on proximity, urgency, etc.
        ranking_score = calculate_ranking_score(
            compatibility_score=compatibility_score,
            distance_km=distance_km,
            urgency=request.urgency,
        )

        candidates.append({
            "donor": donor,
            "compatibility_score": compatibility_score,
            "distance_km": distance_km,
            "ranking_score": ranking_score,
        })

    # 3. Sort candidates: Best candidates first
    candidates.sort(
        key=lambda candidate: candidate["ranking_score"],
        reverse=True,
    )

    # 4. Select top N candidates
    selected_candidates = candidates[:max_matches_per_request]

    # 5. Create and save match records
    matches = []
    for candidate in selected_candidates:
        match = create_match(
            session,
            request_id=request.id,
            donor_id=candidate["donor"].id,
            compatibility_score=candidate["compatibility_score"],
            distance_km=candidate["distance_km"],
            ranking_score=candidate["ranking_score"],
            status="Suggested",
        )
        matches.append(match)

    return matches

