import streamlit as st

from src.database.connection import SessionLocal
from src.database.crud import get_blood_request, get_all_donors
from src.algorithms.compatibility import is_compatible
from src.algorithms.eligibility import is_eligible
from src.algorithms.distance import calculate_distance
from src.algorithms.ranking import calculate_ranking_score


st.title("🩸 Blood Donor Matching")

session = SessionLocal()

try:
    requests = (
        session.query(
            __import__(
                "src.database.models",
                fromlist=["BloodRequest"]
            ).BloodRequest
        )
        .order_by(
            __import__(
                "src.database.models",
                fromlist=["BloodRequest"]
            ).BloodRequest.created_at.desc()
        )
        .all()
    )

    if not requests:
        st.warning("No blood requests found.")

    else:
        request_options = {
            f"Request #{request.id} | "
            f"{request.blood_type} | "
            f"{request.urgency} | "
            f"{request.units_required} unit(s)": request.id
            for request in requests
        }

        selected_request = st.selectbox(
            "Select Blood Request",
            list(request_options.keys()),
        )

        request_id = request_options[selected_request]

        request = get_blood_request(session, request_id)

        if request:

            st.info(
                f"**Blood Type:** {request.blood_type}  |  "
                f"**Urgency:** {request.urgency}  |  "
                f"**Units Required:** {request.units_required}"
            )

            if st.button(" Find Matches", type="primary"):

                donors = get_all_donors(session)

                candidates = []

                for donor in donors:

                    # 1. Eligibility
                    if not is_eligible(
                        donor.age,
                        donor.is_available,
                        donor.last_donation_date,
                    ):
                        continue

                    # 2. Blood compatibility
                    if not is_compatible(
                        donor.blood_type,
                        request.blood_type,
                    ):
                        continue

                    # 3. Distance
                    distance_km = calculate_distance(
                        donor.latitude,
                        donor.longitude,
                        request.latitude,
                        request.longitude,
                    )

                    # 4. Compatibility score
                    compatibility_score = 100.0

                    # 5. Ranking
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

                # Sort best → worst
                candidates.sort(
                    key=lambda x: x["ranking_score"],
                    reverse=True,
                )

                if not candidates:
                    st.error(
                        "❌ No eligible compatible donors found."
                    )

                else:
                    st.success(
                        f" Found {len(candidates)} "
                        f"eligible compatible donor(s)."
                    )

                    st.caption(
                        f"Showing the best matches for "
                        f"{request.units_required} required unit(s)."
                    )

                    st.divider()

                    # =========================
                    # Best Match
                    # =========================

                    best = candidates[0]
                    donor = best["donor"]

                    st.subheader(" Best Match")

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric(
                        "Donor",
                        donor.name,
                    )

                    col2.metric(
                        "Blood Type",
                        donor.blood_type,
                    )

                    col3.metric(
                        "Distance",
                        f"{best['distance_km']:.2f} km",
                    )

                    col4.metric(
                        "Ranking Score",
                        f"{best['ranking_score']:.1f}",
                    )

                    st.success(
                        f"Recommended donor: **{donor.name}**"
                    )

                    st.divider()

                    # =========================
                    # Other Recommended Donors
                    # =========================

                    if len(candidates) > 1:

                        st.subheader("👥 Other Recommended Donors")

                        for index, candidate in enumerate(
                            candidates[1:],
                            start=2,
                        ):

                            donor = candidate["donor"]

                            with st.container():

                                st.write(
                                    f"### #{index} — {donor.name}"
                                )

                                col1, col2, col3, col4 = st.columns(4)

                                col1.metric(
                                    "Blood Type",
                                    donor.blood_type,
                                )

                                col2.metric(
                                    "Distance",
                                    f"{candidate['distance_km']:.2f} km",
                                )

                                col3.metric(
                                    "Compatibility",
                                    f"{candidate['compatibility_score']:.0f}%",
                                )

                                col4.metric(
                                    "Ranking Score",
                                    f"{candidate['ranking_score']:.1f}",
                                )

                                st.divider()

finally:
    session.close()