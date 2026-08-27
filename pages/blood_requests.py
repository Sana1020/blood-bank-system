import streamlit as st

from src.database.connection import SessionLocal
from src.database.crud import (
    get_all_blood_requests,
    get_patient,
)


st.title("🩸 Blood Requests")
st.caption("Manage and monitor blood donation requests")


# =========================
# Load Requests
# =========================

session = SessionLocal()

try:
    requests = get_all_blood_requests(session)

    # =========================
    # Statistics
    # =========================

    total_requests = len(requests)

    emergency_requests = sum(
        1 for r in requests
        if r.urgency == "Emergency"
    )

    pending_requests = sum(
        1 for r in requests
        if r.status == "Pending"
    )

    fulfilled_requests = sum(
        1 for r in requests
        if r.status == "Fulfilled"
    )

    # =========================
    # Top Statistics
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Requests",
        total_requests,
    )

    col2.metric(
        "🚨 Emergency",
        emergency_requests,
    )

    col3.metric(
        "⏳ Pending",
        pending_requests,
    )

    col4.metric(
        "✅ Fulfilled",
        fulfilled_requests,
    )

    st.divider()

    # =========================
    # Filters
    # =========================

    st.subheader("🔎 Find a Request")

    col1, col2, col3 = st.columns(3)

    with col1:
        urgency_filter = st.selectbox(
            "Urgency",
            [
                "All",
                "Emergency",
                "Urgent",
                "Normal",
            ],
        )

    with col2:
        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Pending",
                "Matching",
                "Fulfilled",
                "Cancelled",
            ],
        )

    with col3:
        blood_filter = st.selectbox(
            "Blood Type",
            [
                "All",
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

    # =========================
    # Apply Filters
    # =========================

    filtered_requests = requests

    if urgency_filter != "All":
        filtered_requests = [
            r for r in filtered_requests
            if r.urgency == urgency_filter
        ]

    if status_filter != "All":
        filtered_requests = [
            r for r in filtered_requests
            if r.status == status_filter
        ]

    if blood_filter != "All":
        filtered_requests = [
            r for r in filtered_requests
            if r.blood_type == blood_filter
        ]

    st.divider()

    # =========================
    # Requests
    # =========================

    st.subheader(
        f"📋 Requests ({len(filtered_requests)})"
    )

    if not filtered_requests:
        st.info("No blood requests match the selected filters.")

    else:

        # Newest first
        filtered_requests = sorted(
            filtered_requests,
            key=lambda r: r.created_at,
            reverse=True,
        )

        for request in filtered_requests:

            # Get patient
            patient = get_patient(
                session,
                request.patient_id,
            )

            patient_name = (
                patient.name
                if patient
                else "Unknown Patient"
            )

            # =========================
            # Urgency Indicator
            # =========================

            if request.urgency == "Emergency":
                urgency_icon = "🚨"
                urgency_text = "EMERGENCY"

            elif request.urgency == "Urgent":
                urgency_icon = "🟠"
                urgency_text = "URGENT"

            else:
                urgency_icon = "🟢"
                urgency_text = "NORMAL"

            # =========================
            # Status Indicator
            # =========================

            if request.status == "Pending":
                status_icon = "⏳"

            elif request.status == "Matching":
                status_icon = "🔎"

            elif request.status == "Fulfilled":
                status_icon = "✅"

            elif request.status == "Cancelled":
                status_icon = "❌"

            else:
                status_icon = "⚪"

            # =========================
            # Request Card
            # =========================

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.markdown(
                        f"### 🩸 Request #{request.id}"
                    )

                    st.markdown(
                        f"**{urgency_icon} {urgency_text}**"
                    )

                with col2:

                    st.markdown(
                        f"### {request.blood_type}"
                    )

                    st.caption(
                        f"{request.units_required} "
                        f"unit(s)"
                    )

                st.divider()

                col1, col2, col3 = st.columns(3)

                col1.markdown(
                    f"**Patient**  \n"
                    f"{patient_name}"
                )

                col2.markdown(
                    f"**Hospital**  \n"
                    f"{request.hospital}"
                )

                col3.markdown(
                    f"**Location**  \n"
                    f"📍 {request.location}"
                )

                st.write("")

                col1, col2, col3 = st.columns(3)

                col1.markdown(
                    f"**Status:** "
                    f"{status_icon} {request.status}"
                )

                col2.markdown(
                    f"**Units Required:** "
                    f"{request.units_required}"
                )

                col3.markdown(
                    f"**Request ID:** #{request.id}"
                )

                st.write("")

                # =========================
                # Action
                # =========================

                if request.status not in [
                    "Fulfilled",
                    "Cancelled",
                ]:

                    if st.button(
                        "🔎 Find Compatible Donors",
                        key=f"match_{request.id}",
                        use_container_width=True,
                    ):
                        st.session_state[
                            "selected_request_id"
                        ] = request.id

                        st.success(
                            f"Request #{request.id} selected."
                        )

                        st.info(
                            "Go to the Matching page "
                            "to find the best donors."
                        )

                else:

                    st.caption(
                        "This request is no longer active."
                    )

                st.write("")

finally:
    session.close()