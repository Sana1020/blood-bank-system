import streamlit as st
import pandas as pd

from src.database.connection import SessionLocal
from src.database.models import (
    Donor,
    Patient,
    BloodRequest,
    BloodInventory,
    Donation,
    Match,
)


st.title("📊 Statistics & Analytics")
st.caption("Analyze blood bank activity and system performance")


session = SessionLocal()

try:
    # =========================
    # Load Data
    # =========================

    donors = session.query(Donor).all()
    patients = session.query(Patient).all()
    requests = session.query(BloodRequest).all()
    inventory = session.query(BloodInventory).all()
    donations = session.query(Donation).all()
    matches = session.query(Match).all()

    # =========================
    # Summary
    # =========================

    total_donors = len(donors)
    available_donors = sum(
        donor.is_available
        for donor in donors
    )

    total_patients = len(patients)
    total_requests = len(requests)

    total_donations = len(donations)
    total_matches = len(matches)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

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
        "Donations",
        total_donations,
    )

    col6.metric(
        "Matches",
        total_matches,
    )

    st.divider()

    # =========================
    # Donor Statistics
    # =========================

    st.subheader("🧑‍⚕️ Donor Statistics")

    donor_col1, donor_col2 = st.columns(2)

    # Blood types
    donor_blood_counts = {}

    for donor in donors:
        donor_blood_counts[donor.blood_type] = (
            donor_blood_counts.get(donor.blood_type, 0) + 1
        )

    if donor_blood_counts:

        donor_df = pd.DataFrame(
            {
                "Blood Type": list(donor_blood_counts.keys()),
                "Donors": list(donor_blood_counts.values()),
            }
        )

        with donor_col1:
            st.write("**Donors by Blood Type**")
            st.bar_chart(
                donor_df.set_index("Blood Type")
            )

    # Availability
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

    # =========================
    # Patient Statistics
    # =========================

    st.subheader("🩺 Patient Statistics")

    patient_blood_counts = {}

    for patient in patients:
        patient_blood_counts[patient.blood_type] = (
            patient_blood_counts.get(patient.blood_type, 0) + 1
        )

    if patient_blood_counts:

        patient_df = pd.DataFrame(
            {
                "Blood Type": list(patient_blood_counts.keys()),
                "Patients": list(patient_blood_counts.values()),
            }
        )

        st.bar_chart(
            patient_df.set_index("Blood Type")
        )

    else:
        st.info("No patient data available.")

    st.divider()

    # =========================
    # Request Statistics
    # =========================

    st.subheader("📋 Blood Request Statistics")

    request_col1, request_col2 = st.columns(2)

    # Status
    status_counts = {}

    for request in requests:
        status_counts[request.status] = (
            status_counts.get(request.status, 0) + 1
        )

    if status_counts:

        status_df = pd.DataFrame(
            {
                "Status": list(status_counts.keys()),
                "Requests": list(status_counts.values()),
            }
        )

        with request_col1:
            st.write("**Requests by Status**")

            st.bar_chart(
                status_df.set_index("Status")
            )

    # Urgency
    urgency_counts = {}

    for request in requests:
        urgency_counts[request.urgency] = (
            urgency_counts.get(request.urgency, 0) + 1
        )

    if urgency_counts:

        urgency_df = pd.DataFrame(
            {
                "Urgency": list(urgency_counts.keys()),
                "Requests": list(urgency_counts.values()),
            }
        )

        with request_col2:
            st.write("**Requests by Urgency**")

            st.bar_chart(
                urgency_df.set_index("Urgency")
            )

    st.divider()

    # =========================
    # Blood Type Demand
    # =========================

    st.subheader("🩸 Blood Type Demand")

    blood_demand = {}

    for request in requests:
        blood_demand[request.blood_type] = (
            blood_demand.get(request.blood_type, 0)
            + request.units_required
        )

    if blood_demand:

        demand_df = pd.DataFrame(
            {
                "Blood Type": list(blood_demand.keys()),
                "Units Required": list(blood_demand.values()),
            }
        )

        st.bar_chart(
            demand_df.set_index("Blood Type")
        )

    else:
        st.info("No blood request data available.")

    st.divider()

    # =========================
    # Inventory Statistics
    # =========================

    st.subheader("📦 Inventory Statistics")

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
        st.info("No inventory records found.")

    st.divider()

    # =========================
    # Matching Statistics
    # =========================

    st.subheader("🔎 Matching Statistics")

    if matches:

        average_distance = (
            sum(match.distance_km for match in matches)
            / len(matches)
        )

        average_score = (
            sum(match.ranking_score for match in matches)
            / len(matches)
        )

        compatibility_average = (
            sum(match.compatibility_score for match in matches)
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

        st.write("**Matches by Status**")

        match_status_counts = {}

        for match in matches:
            match_status_counts[match.status] = (
                match_status_counts.get(match.status, 0) + 1
            )

        match_df = pd.DataFrame(
            {
                "Status": list(match_status_counts.keys()),
                "Matches": list(match_status_counts.values()),
            }
        )

        st.bar_chart(
            match_df.set_index("Status")
        )

    else:
        st.info("No matching data available.")

finally:
    session.close()