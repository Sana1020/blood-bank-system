import streamlit as st

from src.database.connection import SessionLocal
from src.database.crud import get_blood_request
from src.database.models import BloodRequest
from src.services.matching_service import find_matches


st.title("🩸 Blood Donor Matching")

session = SessionLocal()

try:
    # Get all blood requests
    requests = (
        session.query(BloodRequest)
        .order_by(BloodRequest.created_at.desc())
        .all()
    )

    if not requests:
        st.warning("No blood requests found.")

    else:
        # Request selection
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

            st.divider()

            if st.button("🔎 Find Matches", type="primary"):

                # Matching logic is handled by the service layer
                matches = find_matches(
                    session,
                    request.id,
                )

                if not matches:
                    st.error(
                        "❌ No eligible compatible donors found."
                    )

                else:
                    st.success(
                        f"✅ Found {len(matches)} "
                        f"recommended donor(s)."
                    )

                    st.caption(
                        f"Showing the best matches for "
                        f"{request.units_required} required unit(s)."
                    )

                    st.divider()

                    # =========================
                    # Best Match
                    # =========================

                    best = matches[0]
                    donor = best.donor

                    st.subheader("🥇 Best Match")

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
                        f"{best.distance_km:.2f} km",
                    )

                    col4.metric(
                        "Ranking Score",
                        f"{best.ranking_score:.1f}",
                    )

                    st.success(
                        f"Recommended donor: **{donor.name}**"
                    )

                    st.divider()

                    # =========================
                    # Other Recommended Donors
                    # =========================

                    if len(matches) > 1:

                        st.subheader("👥 Other Recommended Donors")

                        for index, match in enumerate(
                            matches[1:],
                            start=2,
                        ):

                            donor = match.donor

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
                                    f"{match.distance_km:.2f} km",
                                )

                                col3.metric(
                                    "Compatibility",
                                    f"{match.compatibility_score:.0f}%",
                                )

                                col4.metric(
                                    "Ranking Score",
                                    f"{match.ranking_score:.1f}",
                                )

                                st.divider()

finally:
    session.close()