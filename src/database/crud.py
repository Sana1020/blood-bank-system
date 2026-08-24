from sqlalchemy.orm import Session

from .models import (
    BloodInventory,
    BloodRequest,
    Donation,
    Donor,
    Match,
    Patient,
)




def create_donor(session: Session, **data):
    donor = Donor(**data)
    session.add(donor)
    session.commit()
    session.refresh(donor)
    return donor


def get_donor(session: Session, donor_id: int):
    return session.get(Donor, donor_id)


def get_all_donors(session: Session):
    return session.query(Donor).all()


def update_donor(session: Session, donor_id: int, **data):
    donor = session.get(Donor, donor_id)

    if donor is None:
        return None

    for key, value in data.items():
        if hasattr(donor, key):
            setattr(donor, key, value)

    session.commit()
    session.refresh(donor)

    return donor


def delete_donor(session: Session, donor_id: int):
    donor = session.get(Donor, donor_id)

    if donor is None:
        return False

    session.delete(donor)
    session.commit()

    return True




def create_patient(session: Session, **data):
    patient = Patient(**data)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


def get_patient(session: Session, patient_id: int):
    return session.get(Patient, patient_id)


def get_all_patients(session: Session):
    return session.query(Patient).all()




def create_blood_request(session: Session, **data):
    request = BloodRequest(**data)
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


def get_blood_request(session: Session, request_id: int):
    return session.get(BloodRequest, request_id)


def get_all_blood_requests(session: Session):
    return session.query(BloodRequest).all()


def update_blood_request(session: Session, request_id: int, **data):
    request = session.get(BloodRequest, request_id)

    if request is None:
        return None

    for key, value in data.items():
        if hasattr(request, key):
            setattr(request, key, value)

    session.commit()
    session.refresh(request)

    return request




def create_donation(session: Session, **data):
    donation = Donation(**data)
    session.add(donation)
    session.commit()
    session.refresh(donation)
    return donation


def get_donations_by_donor(session: Session, donor_id: int):
    return (
        session.query(Donation)
        .filter(Donation.donor_id == donor_id)
        .all()
    )




def get_inventory(session: Session):
    return session.query(BloodInventory).all()


def get_inventory_by_type(session: Session, blood_type: str):
    return (
        session.query(BloodInventory)
        .filter(BloodInventory.blood_type == blood_type)
        .first()
    )


def update_inventory(
    session: Session,
    blood_type: str,
    units_available: int,
):
    inventory = get_inventory_by_type(session, blood_type)

    if inventory is None:
        return None

    inventory.units_available = units_available

    session.commit()
    session.refresh(inventory)

    return inventory


# =========================
# Match CRUD
# =========================

def create_match(session: Session, **data):
    match = Match(**data)
    session.add(match)
    session.commit()
    session.refresh(match)
    return match


def get_matches_by_request(
    session: Session,
    request_id: int,
):
    return (
        session.query(Match)
        .filter(Match.request_id == request_id)
        .order_by(Match.ranking_score.desc())
        .all()
    )