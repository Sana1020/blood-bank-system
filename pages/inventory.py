
import streamlit as st
import pandas as pd

from src.database.connection import SessionLocal
from src.database.crud import (
    get_inventory,
    get_inventory_by_type,
    update_inventory,
)


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Blood Inventory",
    page_icon=None,
    layout="wide",
)


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
# Page Header
# =========================================================

st.title("🩸 Blood Inventory")

st.caption(
    "Monitor available blood units and stock levels"
)


# =========================================================
# Database
# =========================================================

session = SessionLocal()

try:

    inventory = get_inventory(session)


    # =====================================================
    # Summary
    # =====================================================

    total_units = sum(
        item.units_available
        for item in inventory
    )

    low_stock = sum(
        1
        for item in inventory
        if item.units_available
        <= item.low_stock_threshold
    )

    blood_types = len(inventory)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Units",
            total_units,
        )

    with col2:
        st.metric(
            "Low Stock Types",
            low_stock,
        )

    with col3:
        st.metric(
            "Blood Types",
            blood_types,
        )


    st.divider()


    # =====================================================
    # Inventory Table
    # =====================================================

    st.subheader("Current Inventory")

    if not inventory:

        st.info(
            "No inventory records found."
        )

    else:

        data = []

        for item in inventory:

            status = (
                "Low Stock"
                if item.units_available
                <= item.low_stock_threshold
                else "Good"
            )

            data.append(
                {
                    "Blood Type": item.blood_type,
                    "Available Units": item.units_available,
                    "Low Stock Threshold": item.low_stock_threshold,
                    "Status": status,
                }
            )

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


    st.divider()


    # =====================================================
    # Update Inventory
    # =====================================================

    st.subheader("Update Blood Stock")

    blood_types_options = [
        item.blood_type
        for item in inventory
    ]


    if blood_types_options:

        selected_type = st.selectbox(
            "Blood Type",
            blood_types_options,
        )

        selected_inventory = get_inventory_by_type(
            session,
            selected_type,
        )


        if selected_inventory:

            st.write(
                f"Current stock: "
                f"**{selected_inventory.units_available} units**"
            )


            new_units = st.number_input(
                "New Available Units",
                min_value=0,
                value=selected_inventory.units_available,
                step=1,
            )


            if st.button(
                "Update Inventory",
                type="primary",
            ):

                updated_inventory = update_inventory(
                    session,
                    selected_type,
                    new_units,
                )

                if updated_inventory:

                    st.success(
                        f"✅ {selected_type} inventory updated "
                        f"successfully to "
                        f"{updated_inventory.units_available} units."
                    )

                    # Update displayed value immediately
                    st.write(
                        f"Updated stock: "
                        f"**{updated_inventory.units_available} units**"
                    )

                else:

                    st.error(
                        f"❌ No inventory record found for "
                        f"{selected_type}."
                    )

finally:

    session.close()


