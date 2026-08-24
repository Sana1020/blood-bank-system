from src.database.connection import SessionLocal
from src.database.crud import (
    create_blood_request,
    get_all_blood_requests,
    get_blood_request,
    update_blood_request,
)


def add_blood_request(**data):
    with SessionLocal() as session:
        return create_blood_request(session, **data)


def get_blood_requests():
    with SessionLocal() as session:
        return get_all_blood_requests(session)


def get_blood_request_by_id(request_id: int):
    with SessionLocal() as session:
        return get_blood_request(session, request_id)


def edit_blood_request(request_id: int, **data):
    with SessionLocal() as session:
        return update_blood_request(
            session,
            request_id,
            **data
        )