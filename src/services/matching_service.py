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


def find_matches(session: Session, request_id: int):
    """
    Find, rank, and save eligible donors for a blood request.
    """

    request = get_blood_request(session, request_id)

    if request is None:
        return []

    # Remove previous matches for this request
    delete_matches_by_request(session, request_id)

    donors = get_all_donors(session)

    candidates = []

    for donor in donors:

        # 1. Check donor eligibility
        if not is_eligible(
            donor.age,
            donor.is_available,
            donor.last_donation_date,
        ):
            continue

        # 2. Check blood compatibility
        if not is_compatible(
            donor.blood_type,
            request.blood_type,
        ):
            continue

        # 3. Calculate distance
        distance_km = calculate_distance(
            donor.latitude,
            donor.longitude,
            request.latitude,
            request.longitude,
        )

        # 4. Compatible donors receive 100%
        compatibility_score = 100.0

        # 5. Calculate ranking score
        ranking_score = calculate_ranking_score(
            compatibility_score=compatibility_score,
            distance_km=distance_km,
            urgency=request.urgency,
        )

        candidates.append(
            {
                "donor": donor,
                "compatibility_score": compatibility_score,
                "distance_km": distance_km,
                "ranking_score": ranking_score,
            }
        )

    # Best candidates first
    candidates.sort(
        key=lambda candidate: candidate["ranking_score"],
        reverse=True,
    )

    # Limit matches according to requested units
    selected_candidates = candidates[:request.units_required]

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