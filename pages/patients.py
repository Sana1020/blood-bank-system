import streamlit as st
import pandas as pd

from src.database.connection import SessionLocal
from src.database.crud import (
    create_patient,
    get_all_patients,
)


st.title("🩺 Patients Management")
st.caption("Register and manage patient records")


# =========================
# Add Patient
# =========================

st.subheader("➕ Register New Patient")

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


# =========================
# Registered Patients
# =========================

st.subheader("📋 Registered Patients")

session = SessionLocal()

try:

    patients = get_all_patients(session)

    if not patients:

        st.info("No patient records found.")

    else:

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