import streamlit as st

from src.database.connection import SessionLocal
from src.database.models import (
    Donor,
    Patient,
    BloodRequest,
    BloodInventory,
    Donation,
    Match,
)


st.title("🩸 Smart Blood Bank Dashboard")
st.caption("Overview of the blood bank system")


session = SessionLocal()

try:
    # =========================
    # Database Data
    # =========================

    donors = session.query(Donor).all()
    patients = session.query(Patient).all()
    requests = (
        session.query(BloodRequest)
        .order_by(BloodRequest.created_at.desc())
        .all()
    )
    inventory = session.query(BloodInventory).all()
    donations = session.query(Donation).all()
    matches = session.query(Match).all()

    # =========================
    # Statistics
    # =========================

    total_donors = len(donors)

    available_donors = sum(
        1 for donor in donors
        if donor.is_available
    )

    total_patients = len(patients)

    total_requests = len(requests)

    pending_requests = sum(
        1 for request in requests
        if request.status == "Pending"
    )

    emergency_requests = sum(
        1 for request in requests
        if request.urgency == "Emergency"
    )

    fulfilled_requests = sum(
        1 for request in requests
        if request.status == "Fulfilled"
    )

    total_units = sum(
        item.units_available
        for item in inventory
    )

    low_stock_items = [
        item
        for item in inventory
        if item.units_available <= item.low_stock_threshold
    ]

    total_donations = len(donations)
    total_matches = len(matches)

    # =========================
    # Main Metrics
    # =========================

    st.subheader("📊 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🧑‍⚕️ Total Donors",
        total_donors,
    )

    col2.metric(
        "🟢 Available Donors",
        available_donors,
    )

    col3.metric(
        "🩺 Patients",
        total_patients,
    )

    col4.metric(
        "🩸 Blood Requests",
        total_requests,
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "⏳ Pending Requests",
        pending_requests,
    )

    col2.metric(
        "🚨 Emergency Requests",
        emergency_requests,
    )

    col3.metric(
        "✅ Fulfilled Requests",
        fulfilled_requests,
    )

    col4.metric(
        "🩸 Available Units",
        total_units,
    )

    st.divider()

    # =========================
    # Blood Inventory
    # =========================

    st.subheader("🩸 Blood Inventory")

    if not inventory:
        st.info("No inventory records found.")

    else:
        inventory_columns = st.columns(4)

        for index, item in enumerate(inventory):
            col = inventory_columns[index % 4]

            with col:
                st.metric(
                    item.blood_type,
                    f"{item.units_available} units",
                )

                if item.units_available <= item.low_stock_threshold:
                    st.warning(
                        f"⚠️ Low stock "
                        f"(threshold: {item.low_stock_threshold})"
                    )
                else:
                    st.success("Stock level OK")

    st.divider()

    # =========================
    # Alerts
    # =========================

    st.subheader("🚨 Alerts")

    alert_col1, alert_col2 = st.columns(2)

    with alert_col1:

        if emergency_requests > 0:
            st.error(
                f"🚨 {emergency_requests} emergency "
                f"request(s) require attention."
            )
        else:
            st.success("No emergency requests.")

    with alert_col2:

        if low_stock_items:
            st.warning(
                f"⚠️ {len(low_stock_items)} blood type(s) "
                f"are low in stock."
            )
        else:
            st.success("All blood types have sufficient stock.")

    st.divider()

    # =========================
    # Recent Requests
    # =========================

    st.subheader("📋 Recent Blood Requests")

    if not requests:
        st.info("No blood requests found.")

    else:

        recent_requests = requests[:5]

        for request in recent_requests:

            patient = session.get(
                Patient,
                request.patient_id,
            )

            patient_name = (
                patient.name
                if patient
                else "Unknown Patient"
            )

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(4)

                col1.write(
                    f"**Request #{request.id}**"
                )

                col2.write(
                    f"**Patient:** {patient_name}"
                )

                col3.write(
                    f"**Blood:** {request.blood_type}"
                )

                col4.write(
                    f"**Status:** {request.status}"
                )

                if request.urgency == "Emergency":
                    st.error("🚨 EMERGENCY REQUEST")

                elif request.urgency == "Urgent":
                    st.warning("🟠 URGENT REQUEST")

    st.divider()

    # =========================
    # System Activity
    # =========================

    st.subheader("📈 System Activity")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💉 Total Donations",
        total_donations,
    )

    col2.metric(
        "🔎 Total Matches",
        total_matches,
    )

    col3.metric(
        "📦 Blood Types",
        len(inventory),
    )

finally:
    session.close()