
import streamlit as st
import pandas as pd

from src.database.connection import SessionLocal
from src.database.models import (
    Donor,
    Patient,
    BloodRequest,
    BloodInventory,
    Match,
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Statistics & Analytics",
    page_icon="📊",
    layout="wide",
)

# =========================================================
# Custom Theme
# =========================================================

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
    unsafe_allow_html=True,
)

# =========================================================
# Sidebar
# =========================================================

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

    st.success("System Operational")

# =========================================================
# Page Header
# =========================================================

st.title("📊 Statistics & Analytics")

st.caption(
    "Analyze blood bank activity and system performance"
)

# =========================================================
# Database
# =========================================================

session = SessionLocal()

try:

    # =====================================================
    # Load Data
    # =====================================================

    donors = session.query(Donor).all()
    patients = session.query(Patient).all()
    requests = session.query(BloodRequest).all()
    inventory = session.query(BloodInventory).all()
    matches = session.query(Match).all()

    # =====================================================
    # Summary
    # =====================================================

    total_donors = len(donors)

    available_donors = sum(
        1 for donor in donors
        if donor.is_available
    )

    total_patients = len(patients)
    total_requests = len(requests)
    total_matches = len(matches)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Donors",
        total_donors,
    )

    col2.metric(
        "Available",
        available_donors,
    )

    col3.metric(
        "Patients",
        total_patients,
    )

    col4.metric(
        "Requests",
        total_requests,
    )

    col5.metric(
        "Matches",
        total_matches,
    )

    st.divider()

    # =====================================================
    # Donor Statistics
    # =====================================================

    st.subheader("Donor Statistics")

    donor_col1, donor_col2 = st.columns(2)

    # -------------------------
    # Blood Types
    # -------------------------

    donor_blood_counts = {}

    for donor in donors:

        blood_type = donor.blood_type

        donor_blood_counts[blood_type] = (
            donor_blood_counts.get(blood_type, 0) + 1
        )

    if donor_blood_counts:

        donor_df = pd.DataFrame(
            {
                "Blood Type": list(
                    donor_blood_counts.keys()
                ),
                "Donors": list(
                    donor_blood_counts.values()
                ),
            }
        )

        with donor_col1:

            st.write("**Donors by Blood Type**")

            st.bar_chart(
                donor_df.set_index("Blood Type")
            )

    else:

        with donor_col1:
            st.info("No donor data available.")

    # -------------------------
    # Availability
    # -------------------------

    availability_data = pd.DataFrame(
        {
            "Status": [
                "Available",
                "Unavailable",
            ],
            "Donors": [
                available_donors,
                total_donors - available_donors,
            ],
        }
    )

    with donor_col2:

        st.write("**Donor Availability**")

        st.bar_chart(
            availability_data.set_index("Status")
        )

    st.divider()

    # =====================================================
    # Patient Statistics
    # =====================================================

    st.subheader("Patient Statistics")

    patient_blood_counts = {}

    for patient in patients:

        blood_type = patient.blood_type

        patient_blood_counts[blood_type] = (
            patient_blood_counts.get(blood_type, 0) + 1
        )

    if patient_blood_counts:

        patient_df = pd.DataFrame(
            {
                "Blood Type": list(
                    patient_blood_counts.keys()
                ),
                "Patients": list(
                    patient_blood_counts.values()
                ),
            }
        )

        st.bar_chart(
            patient_df.set_index("Blood Type")
        )

    else:

        st.info(
            "No patient data available."
        )

    st.divider()

    # =====================================================
    # Request Statistics
    # =====================================================

    st.subheader("Blood Request Statistics")

    request_col1, request_col2 = st.columns(2)

    # -------------------------
    # Request Status
    # -------------------------

    status_counts = {}

    for request in requests:

        status = request.status

        status_counts[status] = (
            status_counts.get(status, 0) + 1
        )

    if status_counts:

        status_df = pd.DataFrame(
            {
                "Status": list(
                    status_counts.keys()
                ),
                "Requests": list(
                    status_counts.values()
                ),
            }
        )

        with request_col1:

            st.write("**Requests by Status**")

            st.bar_chart(
                status_df.set_index("Status")
            )

    else:

        with request_col1:
            st.info("No request status data.")

    # -------------------------
    # Urgency
    # -------------------------

    urgency_counts = {}

    for request in requests:

        urgency = request.urgency

        urgency_counts[urgency] = (
            urgency_counts.get(urgency, 0) + 1
        )

    if urgency_counts:

        urgency_df = pd.DataFrame(
            {
                "Urgency": list(
                    urgency_counts.keys()
                ),
                "Requests": list(
                    urgency_counts.values()
                ),
            }
        )

        with request_col2:

            st.write("**Requests by Urgency**")

            st.bar_chart(
                urgency_df.set_index("Urgency")
            )

    else:

        with request_col2:
            st.info("No urgency data.")

    st.divider()

    # =====================================================
    # Blood Type Demand
    # =====================================================

    st.subheader("Blood Type Demand")

    blood_demand = {}

    for request in requests:

        blood_type = request.blood_type
        units = request.units_required

        blood_demand[blood_type] = (
            blood_demand.get(blood_type, 0) + units
        )

    if blood_demand:

        demand_df = pd.DataFrame(
            {
                "Blood Type": list(
                    blood_demand.keys()
                ),
                "Units Required": list(
                    blood_demand.values()
                ),
            }
        )

        st.bar_chart(
            demand_df.set_index("Blood Type")
        )

    else:

        st.info(
            "No blood request data available."
        )

    st.divider()

    # =====================================================
    # Inventory Statistics
    # =====================================================

    st.subheader("Inventory Statistics")

    if inventory:

        inventory_df = pd.DataFrame(
            [
                {
                    "Blood Type": item.blood_type,
                    "Available Units": item.units_available,
                    "Low Stock Threshold": item.low_stock_threshold,
                    "Status": (
                        "Low Stock"
                        if item.units_available
                        <= item.low_stock_threshold
                        else "OK"
                    ),
                }
                for item in inventory
            ]
        )

        st.dataframe(
            inventory_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No inventory records found."
        )

    st.divider()

    # =====================================================
    # Matching Statistics
    # =====================================================

    st.subheader("Matching Statistics")

    if matches:

        average_distance = (
            sum(
                match.distance_km
                for match in matches
            )
            / len(matches)
        )

        average_score = (
            sum(
                match.ranking_score
                for match in matches
            )
            / len(matches)
        )

        compatibility_average = (
            sum(
                match.compatibility_score
                for match in matches
            )
            / len(matches)
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Distance",
            f"{average_distance:.2f} km",
        )

        col2.metric(
            "Average Ranking Score",
            f"{average_score:.2f}",
        )

        col3.metric(
            "Average Compatibility",
            f"{compatibility_average:.1f}%",
        )

    else:

        st.info(
            "No matching data available."
        )

finally:

    session.close()

