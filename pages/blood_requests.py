import streamlit as st

from src.database.connection import SessionLocal
from src.database.crud import (
    get_all_blood_requests,
    get_patient,
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

    /* =====================================================
       Main Application
       ===================================================== */

    .stApp {
        background-color: #f7f8fa;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 45px;
        padding-bottom: 60px;
    }


    /* =====================================================
       Sidebar
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #991b1b;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.18);
    }

    /* Sidebar navigation buttons */
    section[data-testid="stSidebar"] button {
        color: #991b1b !important;
    }


    /* =====================================================
       Main Titles
       ===================================================== */

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


    /* =====================================================
       Text
       ===================================================== */

    p {
        color: #5f6b7a;
        line-height: 1.7;
    }


    /* =====================================================
       Metrics
       ===================================================== */

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


    /* =====================================================
       Request Cards
       ===================================================== */

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


    /* =====================================================
       Buttons
       ===================================================== */

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


    /* =====================================================
       Select Boxes
       ===================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 9px;
        border: 1px solid #d1d5db;
    }


    /* =====================================================
       Divider
       ===================================================== */

    hr {
        border: none;
        border-top: 1px solid #e1e5ea;
        margin: 35px 0;
    }


    /* =====================================================
       Alerts
       ===================================================== */

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
# Load Requests
# =========================================================

session = SessionLocal()

try:

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
    # Page Header
    # =====================================================

    st.title("Blood Requests")

    st.caption(
        "Manage and monitor blood donation requests"
    )


    # =====================================================
    # Statistics
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

        # Newest requests first
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
                # Status / Units / ID
                # =================================================

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.markdown(
                        "**Status**"
                    )

                    st.write(
                        request.status
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