import streamlit as st
import pandas as pd

from src.database.connection import SessionLocal
from src.database.crud import (
    get_inventory,
    get_inventory_by_type,
    update_inventory,
)


st.title("🩸 Blood Inventory")
st.caption("Monitor available blood units and stock levels")


session = SessionLocal()

try:

    inventory = get_inventory(session)

    # =========================
    # Summary
    # =========================

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

    col1.metric(
        "🩸 Total Units",
        total_units,
    )

    col2.metric(
        "⚠️ Low Stock Types",
        low_stock,
    )

    col3.metric(
        "Blood Types",
        blood_types,
    )

    st.divider()

    # =========================
    # Inventory Table
    # =========================

    st.subheader("📦 Current Inventory")

    if not inventory:

        st.info(
            "No inventory records found."
        )

    else:

        data = []

        for item in inventory:

            status = (
                "⚠️ Low Stock"
                if item.units_available
                <= item.low_stock_threshold
                else "✅ Good"
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

    # =========================
    # Update Inventory
    # =========================

    st.subheader("✏️ Update Blood Stock")

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

                update_inventory(
                    session,
                    selected_type,
                    new_units,
                )

                st.success(
                    f"{selected_type} inventory updated."
                )

                st.rerun()

finally:
    session.close()