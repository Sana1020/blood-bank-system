
import streamlit as st

from src.database.connection import SessionLocal
from src.database.crud import (
    get_all_blood_requests,
    get_all_patients,
    get_patient,
    create_blood_request,
    get_inventory_by_type,
)


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Blood Requests",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# Custom Theme
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f8fa;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 45px;
        padding-bottom: 60px;
    }

    section[data-testid="stSidebar"] {
        background-color: #991b1b;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.18);
    }

    section[data-testid="stSidebar"] button {
        color: #991b1b !important;
    }

    h1 {
        color: #991b1b !important;
        font-weight: 800 !important;
        font-size: 44px !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #991b1b !important;
        font-weight: 750 !important;
        margin-top: 30px !important;
    }

    h3 {
        color: #1f2937 !important;
        font-weight: 700 !important;
    }

    p {
        color: #5f6b7a;
        line-height: 1.7;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    div[data-testid="stMetricValue"] {
        color: #991b1b !important;
        font-weight: 800 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 14px;
        border: 1px solid #e1e5ea;
        transition: all 0.2s ease;
        padding: 4px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #991b1b;
        box-shadow: 0 6px 20px rgba(153, 27, 27, 0.10);
        transform: translateY(-2px);
    }

    div.stButton > button {
        background-color: #991b1b;
        color: white !important;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #7f1d1d;
        color: white !important;
        border: none;
    }

    div[data-baseweb="select"] > div {
        border-radius: 9px;
        border: 1px solid #d1d5db;
    }

    hr {
        border: none;
        border-top: 1px solid #e1e5ea;
        margin: 35px 0;
    }

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
# Page Header
# =========================================================

st.title("Blood Requests")

st.caption(
    "Manage and monitor blood donation requests"
)


# =========================================================
# Database Session
# =========================================================

session = SessionLocal()

try:

    # =====================================================
    # Load Patients
    # =====================================================

    patients = get_all_patients(session)


    # =====================================================
    # Create New Blood Request
    # =====================================================

    st.subheader("Create New Blood Request")

    if not patients:

        st.info(
            "No patients found. "
            "Please register a patient first."
        )

    else:

        with st.form("blood_request_form"):

            patient_options = {
                f"{patient.name} (ID: {patient.id})": patient
                for patient in patients
            }

            selected_patient_name = st.selectbox(
                "Patient",
                list(patient_options.keys())
            )

            selected_patient = patient_options[
                selected_patient_name
            ]

            col1, col2 = st.columns(2)

            with col1:

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
                    ]
                )

                units_required = st.number_input(
                    "Units Required",
                    min_value=1,
                    value=1,
                    step=1
                )

                urgency = st.selectbox(
                    "Urgency",
                    [
                        "Normal",
                        "Urgent",
                        "Emergency",
                    ]
                )

            with col2:

                hospital = st.text_input(
                    "Hospital"
                )

                location = st.text_input(
                    "Location"
                )

                latitude = st.number_input(
                    "Latitude",
                    format="%.6f"
                )

                longitude = st.number_input(
                    "Longitude",
                    format="%.6f"
                )

            submitted = st.form_submit_button(
                "Create Blood Request",
                type="primary"
            )

        if submitted:

            if not hospital or not location:

                st.error(
                    "Please fill in Hospital and Location."
                )

            else:

                try:

                    create_blood_request(
                        session,
                        patient_id=selected_patient.id,
                        blood_type=blood_type,
                        units_required=units_required,
                        urgency=urgency,
                        hospital=hospital,
                        location=location,
                        latitude=latitude,
                        longitude=longitude,
                    )

                    st.success(
                        f"Blood request created successfully "
                        f"for {selected_patient.name}."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Failed to create blood request: {e}"
                    )


    st.divider()


    # =====================================================
    # Load Requests
    # =====================================================

    requests = get_all_blood_requests(session)


    # =====================================================
    # Statistics
    # =====================================================

    total_requests = len(requests)

    emergency_requests = sum(
        1
        for r in requests
        if r.urgency == "Emergency"
    )

    pending_requests = sum(
        1
        for r in requests
        if r.status == "Pending"
    )

    fulfilled_requests = sum(
        1
        for r in requests
        if r.status == "Fulfilled"
    )


    # =====================================================
    # Statistics Cards
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Requests",
            total_requests
        )

    with col2:

        st.metric(
            "Emergency",
            emergency_requests
        )

    with col3:

        st.metric(
            "Pending",
            pending_requests
        )

    with col4:

        st.metric(
            "Fulfilled",
            fulfilled_requests
        )


    st.divider()


    # =====================================================
    # Filters
    # =====================================================

    st.header("Find a Request")

    col1, col2, col3 = st.columns(3)

    with col1:

        urgency_filter = st.selectbox(
            "Urgency",
            [
                "All",
                "Emergency",
                "Urgent",
                "Normal",
            ]
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
            ]
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
            ]
        )


    # =====================================================
    # Apply Filters
    # =====================================================

    filtered_requests = requests

    if urgency_filter != "All":

        filtered_requests = [
            r
            for r in filtered_requests
            if r.urgency == urgency_filter
        ]

    if status_filter != "All":

        filtered_requests = [
            r
            for r in filtered_requests
            if r.status == status_filter
        ]

    if blood_filter != "All":

        filtered_requests = [
            r
            for r in filtered_requests
            if r.blood_type == blood_filter
        ]


    st.divider()


    # =====================================================
    # Requests
    # =====================================================

    st.header(
        f"Requests ({len(filtered_requests)})"
    )


    if not filtered_requests:

        st.info(
            "No blood requests match the selected filters."
        )

    else:

        filtered_requests = sorted(
            filtered_requests,
            key=lambda r: r.created_at,
            reverse=True
        )


        for request in filtered_requests:

            # =================================================
            # Get Patient
            # =================================================

            patient = get_patient(
                session,
                request.patient_id
            )

            patient_name = (
                patient.name
                if patient
                else "Unknown Patient"
            )


            # =================================================
            # Request Card
            # =================================================

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.subheader(
                        f"Request #{request.id}"
                    )

                    if request.urgency == "Emergency":

                        st.markdown(
                            """
                            <div style="
                                color:#991b1b;
                                font-weight:800;
                                font-size:14px;
                                letter-spacing:0.5px;
                            ">
                                EMERGENCY
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    elif request.urgency == "Urgent":

                        st.markdown(
                            """
                            <div style="
                                color:#b45309;
                                font-weight:800;
                                font-size:14px;
                                letter-spacing:0.5px;
                            ">
                                URGENT
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            """
                            <div style="
                                color:#15803d;
                                font-weight:800;
                                font-size:14px;
                                letter-spacing:0.5px;
                            ">
                                NORMAL
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                with col2:

                    st.markdown(
                        f"""
                        <div style="
                            text-align:right;
                            font-size:26px;
                            font-weight:800;
                            color:#991b1b;
                            padding-top:8px;
                        ">
                            {request.blood_type}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption(
                        f"{request.units_required} unit(s)"
                    )


                st.divider()


                # =================================================
                # Patient / Hospital / Location
                # =================================================

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.markdown(
                        "**Patient**"
                    )

                    st.write(
                        patient_name
                    )

                with col2:

                    st.markdown(
                        "**Hospital**"
                    )

                    st.write(
                        request.hospital
                    )

                with col3:

                    st.markdown(
                        "**Location**"
                    )

                    st.write(
                        request.location
                    )


                st.write("")


                # =================================================
                # Status / Units / Request ID
                # =================================================

                col1, col2, col3 = st.columns(3)

                status_options = [
                    "Pending",
                    "Matching",
                    "Fulfilled",
                    "Cancelled",
                ]

                current_index = (
                    status_options.index(request.status)
                    if request.status in status_options
                    else 0
                )

                with col1:

                    new_status = st.selectbox(
                        "Update Status",
                        options=status_options,
                        index=current_index,
                        key=f"status_select_{request.id}"
                    )

                with col2:

                    st.markdown(
                        "**Units Required**"
                    )

                    st.write(
                        request.units_required
                    )

                with col3:

                    st.markdown(
                        "**Request ID**"
                    )

                    st.write(
                        f"#{request.id}"
                    )


                st.write("")


                # =================================================
                # Action
                # =================================================

                col_btn1, col_btn2 = st.columns(2)

                with col_btn1:

                    if new_status != request.status:

                        if st.button(
                            "Save Status Change",
                            key=f"save_status_{request.id}",
                            use_container_width=True
                        ):

                            try:

                                # =================================
                                # Fulfill Request
                                # =================================

                                if (
                                    new_status == "Fulfilled"
                                    and request.status != "Fulfilled"
                                ):

                                    inventory = get_inventory_by_type(
                                        session,
                                        request.blood_type
                                    )

                                    if inventory is None:

                                        st.error(
                                            f"No inventory found for "
                                            f"{request.blood_type}."
                                        )

                                    elif (
                                        inventory.units_available
                                        < request.units_required
                                    ):

                                        st.error(
                                            f"Not enough "
                                            f"{request.blood_type} "
                                            f"blood in inventory. "
                                            f"Available: "
                                            f"{inventory.units_available} "
                                            f"unit(s), Required: "
                                            f"{request.units_required} "
                                            f"unit(s)."
                                        )

                                    else:

                                        # Deduct blood units
                                        inventory.units_available -= (
                                            request.units_required
                                        )

                                        # Update request status
                                        request.status = "Fulfilled"

                                        session.commit()

                                        st.success(
                                            f"Request #{request.id} "
                                            f"fulfilled successfully. "
                                            f"{request.units_required} "
                                            f"unit(s) of "
                                            f"{request.blood_type} "
                                            f"deducted from inventory."
                                        )

                                        st.rerun()

                                else:

                                    # Normal status update
                                    request.status = new_status

                                    session.commit()

                                    st.success(
                                        f"Updated Request "
                                        f"#{request.id} "
                                        f"to {new_status}!"
                                    )

                                    st.rerun()

                            except Exception as e:

                                session.rollback()

                                st.error(
                                    f"Failed to update request: {e}"
                                )


                with col_btn2:

                    if request.status not in [
                        "Fulfilled",
                        "Cancelled"
                    ]:

                        if st.button(
                            "Find Compatible Donors",
                            key=f"match_{request.id}",
                            use_container_width=True
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

