from src.database.connection import SessionLocal
from src.database.crud import (
    create_donor,
    get_all_donors,
    get_donor,
    update_donor,
    delete_donor,
)


def add_donor(**data):
    with SessionLocal() as session:
        return create_donor(session, **data)


def get_donors():
    with SessionLocal() as session:
        return get_all_donors(session)


def get_donor_by_id(donor_id: int):
    with SessionLocal() as session:
        return get_donor(session, donor_id)


def edit_donor(donor_id: int, **data):
    with SessionLocal() as session:
        return update_donor(session, donor_id, **data)


def remove_donor(donor_id: int):
    with SessionLocal() as session:
        return delete_donor(session, donor_id)