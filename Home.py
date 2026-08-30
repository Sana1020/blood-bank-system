import streamlit as st

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Smart Blood Bank",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# Database
# =========================================================

try:
    from src.database.connection import SessionLocal
    from src.database.models import (
        Donor,
        Patient,
        BloodRequest,
        BloodInventory,
    )

    DB_AVAILABLE = True

except Exception:
    DB_AVAILABLE = False


def get_count(model):
    if not DB_AVAILABLE:
        return 0

    session = None

    try:
        session = SessionLocal()
        return session.query(model).count()

    except Exception:
        return 0

    finally:
        if session:
            session.close()


# =========================================================
# Get Database Statistics
# =========================================================

total_donors = get_count(Donor)
total_patients = get_count(Patient)
total_requests = get_count(BloodRequest)
total_inventory = get_count(BloodInventory)


# =========================================================
# Custom Theme
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       Main Application
       ========================= */

    .stApp {
        background-color: #f7f8fa;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 45px;
        padding-bottom: 60px;
    }


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
        font-size: 46px !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #1f2937 !important;
        font-weight: 750 !important;
        margin-top: 30px !important;
    }

    h3 {
        color: #1f2937 !important;
        font-weight: 700 !important;
    }


    /* =========================
       Text
       ========================= */

    p {
        color: #5f6b7a;
        line-height: 1.7;
    }


    /* =========================
       Metric Cards
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
        font-weight: 800;
    }


    /* =========================
       Containers / Cards
       ========================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 14px;
        border: 1px solid #e1e5ea;
        transition: all 0.2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #c62828;
        box-shadow: 0 6px 20px rgba(153,27,27,0.10);
        transform: translateY(-2px);
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
       Success Message
       ========================= */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
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
# Main Header
# =========================================================

st.title("Smart Blood Bank")

st.subheader(
    "Intelligent donor matching and blood bank management system."
)

st.write(
    "A centralized platform for managing donors, patients, "
    "blood requests and inventory."
)


# =========================================================
# Overview
# =========================================================

st.divider()

st.header("System Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Donors",
        total_donors
    )


with col2:
    st.metric(
        "Patients",
        total_patients
    )


with col3:
    st.metric(
        "Blood Requests",
        total_requests
    )


with col4:
    st.metric(
        "Available Stock",
        total_inventory
    )


# =========================================================
# System Modules
# =========================================================

st.header("System Modules")

st.write(
    "Access the main components of the Smart Blood Bank system."
)

st.write("")


# First row
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Donor Management")
        st.write(
            "Register and manage donors, blood types, "
            "availability, locations and donation history."
        )

with col2:
    with st.container(border=True):
        st.subheader("Blood Requests")
        st.write(
            "Create and manage blood requests based on "
            "blood type, required units and urgency."
        )

with col3:
    with st.container(border=True):
        st.subheader("Donor Matching")
        st.write(
            "Find suitable donors using blood compatibility, "
            "eligibility and geographical distance."
        )


st.write("")


# Second row
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Blood Inventory")
        st.write(
            "Monitor blood stock and track available units "
            "for different blood types."
        )

with col2:
    with st.container(border=True):
        st.subheader("Patient Management")
        st.write(
            "Manage patient records and connect their "
            "requirements with appropriate blood requests."
        )

with col3:
    with st.container(border=True):
        st.subheader("Statistics")
        st.write(
            "Review important statistics and insights "
            "related to donors, requests and inventory."
        )


# =========================================================
# About
# =========================================================

st.write("")

st.divider()

st.header("About Smart Blood Bank")

st.write(
    "Smart Blood Bank is designed to improve the management "
    "of blood bank operations and support faster donor identification."
)

st.write(
    "The system considers blood compatibility, donor eligibility, "
    "geographical distance and request urgency when identifying "
    "suitable donors."
)


# =========================================================
# Footer
# =========================================================

st.write("")

st.divider()

st.caption(
    "Smart Blood Bank Management System"
)