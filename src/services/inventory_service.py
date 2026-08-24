from src.database.connection import SessionLocal
from src.database.crud import (
    get_inventory,
    get_inventory_by_type,
    update_inventory,
)


def get_all_inventory():
    with SessionLocal() as session:
        return get_inventory(session)


def get_blood_type_inventory(blood_type: str):
    with SessionLocal() as session:
        return get_inventory_by_type(
            session,
            blood_type
        )


def set_inventory_units(
    blood_type: str,
    units_available: int,
):
    with SessionLocal() as session:
        return update_inventory(
            session,
            blood_type,
            units_available
        )