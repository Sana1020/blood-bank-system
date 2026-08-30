import streamlit as st
from datetime import date

from src.database.connection import SessionLocal
from src.database.crud import create_donor, get_all_donors


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

    st.success("System Operational")


# =========================================================
# Page Title
# =========================================================

st.title("🩸 Donors")


# =========================================================
# Add New Donor
# =========================================================

st.subheader("Add New Donor")

with st.form("donor_form"):

    name = st.text_input("Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=25
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
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
            "AB+"
        ],
    )

    phone = st.text_input("Phone")

    location = st.text_input("Location")

    latitude = st.number_input(
        "Latitude",
        format="%.6f"
    )

    longitude = st.number_input(
        "Longitude",
        format="%.6f"
    )

    is_available = st.checkbox(
        "Available for donation",
        value=True
    )

    last_donation_date = st.date_input(
        "Last Donation Date",
        value=None,
    )

    submitted = st.form_submit_button(
        "Add Donor"
    )


# =========================================================
# Add Donor to Database
# =========================================================

if submitted:

    if not name or not phone or not location:

        st.error(
            "Please fill in all required fields."
        )

    else:

        session = SessionLocal()

        try:

            create_donor(
                session,
                name=name,
                age=age,
                gender=gender,
                blood_type=blood_type,
                phone=phone,
                location=location,
                latitude=latitude,
                longitude=longitude,
                is_available=is_available,
                last_donation_date=last_donation_date,
            )

            st.success(
                "Donor added successfully."
            )

        finally:

            session.close()


# =========================================================
# Registered Donors
# =========================================================

st.divider()

st.subheader("Registered Donors")

session = SessionLocal()

try:

    donors = get_all_donors(session)

    if not donors:

        st.info(
            "No donors found."
        )

    else:

        for donor in donors:

            with st.container():

                st.write(
                    f"### {donor.name}"
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.write(
                    f"**Blood Type:** {donor.blood_type}"
                )

                col2.write(
                    f"**Age:** {donor.age}"
                )

                col3.write(
                    f"**Location:** {donor.location}"
                )

                col4.write(
                    f"**Available:** "
                    f"{'Yes' if donor.is_available else 'No'}"
                )

                st.divider()

finally:

    session.close()