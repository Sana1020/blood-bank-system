
import streamlit as st
import pandas as pd

from src.database.connection import SessionLocal
from src.database.crud import (
    create_patient,
    get_all_patients,
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Patients Management",
    page_icon="🩺",
    layout="wide",
)

# =========================================================
# Custom Theme - Sidebar
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

st.title("Patients Management")

st.caption(
    "Register and manage patient records"
)

# =========================================================
# Add Patient
# =========================================================

st.subheader("Register New Patient")

with st.form("patient_form"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Patient Full Name"
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=25,
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
        )

        blood_type = st.selectbox(
            "Blood Type",
            [
                "O-",
                "O+",
                "A-",
                "A+",
                "B-",
                "B+",
                "AB-",
                "AB+",
            ],
        )

    with col2:

        hospital = st.text_input(
            "Hospital / Clinic"
        )

        location = st.text_input(
            "Location"
        )

        latitude = st.number_input(
            "Latitude",
            format="%.6f",
        )

        longitude = st.number_input(
            "Longitude",
            format="%.6f",
        )

    submitted = st.form_submit_button(
        "Register Patient",
        type="primary",
    )

# =========================================================
# Save Patient
# =========================================================

if submitted:

    if not name or not hospital or not location:

        st.error(
            "Please fill in Name, Hospital and Location."
        )

    else:

        session = SessionLocal()

        try:

            create_patient(
                session,
                name=name,
                age=age,
                gender=gender,
                blood_type=blood_type,
                hospital=hospital,
                location=location,
                latitude=latitude,
                longitude=longitude,
            )

            st.success(
                f"Patient '{name}' registered successfully."
            )

            st.rerun()

        finally:

            session.close()

st.divider()

# =========================================================
# Registered Patients
# =========================================================

st.subheader("📋 Registered Patients")

session = SessionLocal()

try:

    patients = get_all_patients(session)

    if not patients:

        st.info(
            "No patient records found."
        )

    else:

        # Show the newest registered patient first
        patients = list(reversed(patients))

        data = []

        for patient in patients:

            data.append(
                {
                    "ID": patient.id,
                    "Name": patient.name,
                    "Age": patient.age,
                    "Gender": patient.gender,
                    "Blood Type": patient.blood_type,
                    "Hospital": patient.hospital,
                    "Location": patient.location,
                }
            )

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

finally:

    session.close()

