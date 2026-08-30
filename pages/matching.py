import streamlit as st

from src.database.connection import SessionLocal
from src.database.crud import get_blood_request
from src.database.models import BloodRequest
from src.services.matching_service import find_matches


st.title("🩸 Blood Donor Matching")
st.markdown(
    """
    <style>

    /* =========================
       Sidebar
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #991b1b;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.18);
    }

    section[data-testid="stSidebar"] button {
        color: #991b1b !important;
    }

    /* =========================
       Main Titles
       ========================= */

    h1 {
        color: #991b1b !important;
        font-weight: 800 !important;
        font-size: 44px !important;
    }

    h2 {
        color: #991b1b !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #1f2937 !important;
        font-weight: 700 !important;
    }

    /* =========================
       Metrics
       ========================= */

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #991b1b !important;
        font-weight: 800 !important;
    }

    /* =========================
       Buttons
       ========================= */

    div.stButton > button {
        background-color: #991b1b;
        color: white !important;
        border: none;
        border-radius: 9px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #7f1d1d;
        color: white !important;
    }

    /* =========================
       Divider
       ========================= */

    hr {
        border: none;
        border-top: 1px solid #e1e5ea;
        margin: 35px 0;
    }

    /* =========================
       Dataframe
       ========================= */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,)

with st.sidebar:
    st.title("Smart Blood Bank")
    st.caption("Blood Management System")

    st.divider()

    st.subheader("Navigation")

    st.write(
        "Use the navigation menu to access "
        "the different modules of the system."
    )

    st.divider()

    st.success(" System Operational")

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

            if st.button(" Find Matches", type="primary"):

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
