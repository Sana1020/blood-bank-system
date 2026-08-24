from src.database.connection import SessionLocal
from src.database.crud import (
    create_patient,
    get_all_patients,
    get_patient,
)


def add_patient(**data):
    with SessionLocal() as session:
        return create_patient(session, **data)


def get_patients():
    with SessionLocal() as session:
        return get_all_patients(session)


def get_patient_by_id(patient_id: int):
    with SessionLocal() as session:
        return get_patient(session, patient_id)