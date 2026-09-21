### `donors.py`


import streamlit as st
from datetime import date

from src.database.connection import SessionLocal
from src.database.crud import (
    create_donor,
    get_all_donors,
    get_donor,
    create_completed_donation,
    get_donations_by_donor,
)


# =========================================================
# Validation Rules
# =========================================================

MIN_DONOR_AGE = 18
MAX_DONOR_AGE = 65


# =========================================================
# Custom Theme
# =========================================================

st.markdown(
    """
    <style>

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

    hr {
        border: none;
        border-top: 1px solid #e1e5ea;
        margin: 35px 0;
    }

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
# Page Title
# =========================================================

st.title("Donors")


# =========================================================
# Add New Donor
# =========================================================

st.subheader("Add New Donor")

with st.form("donor_form"):

    name = st.text_input(
        "Full Name",
        placeholder="Enter donor's full name"
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=25,
        step=1
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

    phone = st.text_input(
        "Phone Number",
        placeholder="Enter phone number"
    )

    location = st.text_input(
        "Location",
        placeholder="Enter donor location"
    )

    latitude = st.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        format="%.6f"
    )

    longitude = st.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        format="%.6f"
    )

    is_available = st.checkbox(
        "Available for donation",
        value=True
    )

    last_donation_date = st.date_input(
        "Last Donation Date",
        value=None
    )

    submitted = st.form_submit_button(
        "Add Donor",
        type="primary"
    )


# =========================================================
# Validate and Add Donor
# =========================================================

if submitted:

    errors = []

    if not name.strip():
        errors.append(
            "Please enter the donor's full name."
        )

    elif len(name.strip()) < 2:
        errors.append(
            "The donor's name must contain at least 2 characters."
        )

    if age < MIN_DONOR_AGE or age > MAX_DONOR_AGE:
        errors.append(
            f"Invalid donor age. "
            f"Donor age must be between "
            f"{MIN_DONOR_AGE} and {MAX_DONOR_AGE} years."
        )

    cleaned_phone = phone.strip().replace(" ", "")

    if not cleaned_phone:
        errors.append(
            "Please enter a phone number."
        )

    elif not cleaned_phone.isdigit():
        errors.append(
            "Invalid phone number. "
            "Please enter numbers only."
        )

    elif len(cleaned_phone) < 10:
        errors.append(
            "Invalid phone number. "
            "Please enter a valid phone number."
        )

    if not location.strip():
        errors.append(
            "Please enter the donor's location."
        )

    if not (-90 <= latitude <= 90):
        errors.append(
            "Invalid latitude. "
            "Latitude must be between -90 and 90."
        )

    if not (-180 <= longitude <= 180):
        errors.append(
            "Invalid longitude. "
            "Longitude must be between -180 and 180."
        )

    if last_donation_date is not None:

        if last_donation_date > date.today():
            errors.append(
                "Invalid last donation date. "
                "The date cannot be in the future."
            )

    if errors:

        st.error(
            "Please correct the following issues before submitting:"
        )

        for error in errors:
            st.warning(error)

    else:

        session = SessionLocal()

        try:

            create_donor(
                session,
                name=name.strip(),
                age=age,
                gender=gender,
                blood_type=blood_type,
                phone=cleaned_phone,
                location=location.strip(),
                latitude=latitude,
                longitude=longitude,
                is_available=is_available,
                last_donation_date=last_donation_date,
            )

            st.success(
                "✅ Donor registration completed successfully."
            )

        except Exception as e:

            session.rollback()

            st.error(
                f"Error registering donor: {e}"
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
            "No donors have been registered yet."
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

                if donor.last_donation_date:

                    st.caption(
                        f"Last Donation Date: "
                        f"{donor.last_donation_date}"
                    )

                st.divider()

finally:

    session.close()


# =========================================================
# Record Donation
# =========================================================

st.subheader("Record Donation")

session = SessionLocal()

try:

    donors = get_all_donors(session)

    if not donors:

        st.info(
            "Please register a donor before recording a donation."
        )

    else:

        donor_options = {
            f"{donor.name} (ID: {donor.id}) - {donor.blood_type}":
            donor.id
            for donor in donors
        }

        selected_donor_name = st.selectbox(
            "Select Donor",
            list(donor_options.keys()),
            key="record_donation_donor",
        )

        selected_donor_id = donor_options[
            selected_donor_name
        ]

        selected_donor = get_donor(
            session,
            selected_donor_id
        )

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                f"**Donor:** {selected_donor.name}\n\n"
                f"**Blood Type:** {selected_donor.blood_type}"
            )

        with col2:

            if selected_donor.last_donation_date:

                st.info(
                    f"**Last Donation:** "
                    f"{selected_donor.last_donation_date}"
                )

            else:

                st.info(
                    "**Last Donation:** No previous donation"
                )

        donation_date = st.date_input(
            "Donation Date",
            value=date.today(),
            key="donation_date",
        )

        units_donated = st.number_input(
            "Units Donated",
            min_value=1,
            value=1,
            step=1,
            key="units_donated",
        )

        donation_location = st.text_input(
            "Donation Location",
            value=selected_donor.location,
            placeholder="Enter donation location",
            key="donation_location",
        )

        record_donation = st.button(
            "Record Donation",
            type="primary",
        )

        if record_donation:

            errors = []

            if donation_date > date.today():

                errors.append(
                    "Donation date cannot be in the future."
                )

            if units_donated <= 0:

                errors.append(
                    "Units donated must be greater than 0."
                )

            if not donation_location.strip():

                errors.append(
                    "Please enter the donation location."
                )

            if errors:

                st.error(
                    "Please correct the following issues:"
                )

                for error in errors:
                    st.warning(error)

            else:

                try:

                    donation = create_completed_donation(
                        session,
                        donor_id=selected_donor_id,
                        donation_date=donation_date,
                        units_donated=int(units_donated),
                        location=donation_location.strip(),
                    )

                    st.success(
                        f"✅ Donation recorded successfully. "
                        f"{int(units_donated)} unit(s) of "
                        f"{selected_donor.blood_type} "
                        f"added to inventory."
                    )

                except Exception as e:

                    session.rollback()

                    st.error(
                        f"Error recording donation: {e}"
                    )

finally:

    session.close()


# =========================================================
# Donation History
# =========================================================

st.divider()

st.subheader("Donation History")

session = SessionLocal()

try:

    donors = get_all_donors(session)

    if donors:

        history_options = {
            f"{donor.name} (ID: {donor.id})":
            donor.id
            for donor in donors
        }

        selected_history_name = st.selectbox(
            "Select Donor",
            list(history_options.keys()),
            key="donation_history_donor",
        )

        selected_history_id = history_options[
            selected_history_name
        ]

        donations = get_donations_by_donor(
            session,
            selected_history_id
        )

        if donations:

            for donation in donations:

                col1, col2, col3, col4 = st.columns(4)

                col1.write(
                    f"**Date:** {donation.donation_date}"
                )

                col2.write(
                    f"**Blood Type:** {donation.blood_type}"
                )

                col3.write(
                    f"**Units:** {donation.units_donated}"
                )

                col4.write(
                    f"**Status:** {donation.status}"
                )

                st.caption(
                    f"Location: {donation.location}"
                )

                st.divider()

        else:

            st.info(
                "No donations recorded for this donor."
            )

    else:

        st.info(
            "No donors available."
        )

finally:

    session.close()
