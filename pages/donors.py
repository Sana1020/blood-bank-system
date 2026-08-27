import streamlit as st
from datetime import date

from src.database.connection import SessionLocal
from src.database.crud import create_donor, get_all_donors


st.title("🩸 Donors")

st.subheader("Add New Donor")

with st.form("donor_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female"])

    blood_type = st.selectbox(
        "Blood Type",
        ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    )

    phone = st.text_input("Phone")
    location = st.text_input("Location")
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")

    is_available = st.checkbox("Available for donation", value=True)

    last_donation_date = st.date_input(
        "Last Donation Date",
        value=None,
    )

    submitted = st.form_submit_button("Add Donor")

if submitted:
    if not name or not phone or not location:
        st.error("Please fill in all required fields.")
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

            st.success("Donor added successfully.")

        finally:
            session.close()


st.divider()

st.subheader("Registered Donors")

session = SessionLocal()

try:
    donors = get_all_donors(session)

    if not donors:
        st.info("No donors found.")
    else:
        for donor in donors:
            with st.container():
                st.write(f"### {donor.name}")

                col1, col2, col3, col4 = st.columns(4)

                col1.write(f"**Blood Type:** {donor.blood_type}")
                col2.write(f"**Age:** {donor.age}")
                col3.write(f"**Location:** {donor.location}")
                col4.write(
                    f"**Available:** {'Yes' if donor.is_available else 'No'}"
                )

                st.divider()

finally:
    session.close()