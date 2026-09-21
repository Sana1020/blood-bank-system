from sqlalchemy.orm import Session

from .models import (
    BloodInventory,
    BloodRequest,
    Donation,
    Donor,
    Match,
    Patient,
)


# =========================================================
# DONORS
# =========================================================

def create_donor(session: Session, **data):
    donor = Donor(**data)

    session.add(donor)
    session.commit()
    session.refresh(donor)

    return donor


def get_donor(session: Session, donor_id: int):
    return session.get(Donor, donor_id)


def get_all_donors(session: Session):
    return (
        session.query(Donor)
        .order_by(Donor.id.desc())
        .all()
    )


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


# =========================================================
# PATIENTS
# =========================================================

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


# =========================================================
# BLOOD REQUESTS
# =========================================================

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


def fulfill_blood_request(session: Session, request_id: int):
    request = session.get(BloodRequest, request_id)

    if request is None:
        raise ValueError("Blood request not found.")

    # Prevent deducting inventory more than once
    if request.status == "Fulfilled":
        return request

    inventory = get_inventory_by_type(
        session,
        request.blood_type
    )

    if inventory is None:
        raise ValueError(
            f"No inventory found for blood type "
            f"{request.blood_type}."
        )

    # Check available stock
    if inventory.units_available < request.units_required:
        raise ValueError(
            f"Not enough {request.blood_type} blood units "
            f"in inventory. "
            f"Available: {inventory.units_available}, "
            f"Required: {request.units_required}."
        )

    try:
        # Deduct requested units
        inventory.units_available -= request.units_required

        # Mark request as fulfilled
        request.status = "Fulfilled"

        session.commit()

        session.refresh(request)
        session.refresh(inventory)

        return request

    except Exception:
        session.rollback()
        raise


# =========================================================
# DONATIONS
# =========================================================

def create_donation(session: Session, **data):
    donation = Donation(**data)

    session.add(donation)
    session.commit()
    session.refresh(donation)

    return donation


def create_completed_donation(
    session: Session,
    donor_id: int,
    donation_date,
    units_donated: int,
    location: str,
):
    """
    Record a completed donation and automatically update:

    1. Donations table
    2. Blood inventory
    3. Donor's last donation date
    """

    # Validate units
    if units_donated <= 0:
        raise ValueError("Units donated must be greater than 0.")

    # Get donor
    donor = session.get(Donor, donor_id)

    if donor is None:
        raise ValueError("Donor not found.")

    # Get inventory for donor blood type
    inventory = get_inventory_by_type(
        session,
        donor.blood_type
    )

    # If inventory record doesn't exist, create it
    if inventory is None:
        inventory = BloodInventory(
            blood_type=donor.blood_type,
            units_available=0,
        )

        session.add(inventory)
        session.flush()

    try:
        # Create donation record
        donation = Donation(
            donor_id=donor.id,
            donation_date=donation_date,
            blood_type=donor.blood_type,
            units_donated=units_donated,
            location=location,
            status="Completed",
        )

        session.add(donation)

        # Add donated units to inventory
        inventory.units_available += units_donated

        # Update donor's last donation date
        donor.last_donation_date = donation_date

        # Save everything together
        session.commit()
        session.refresh(donation)

        return donation

    except Exception:
        session.rollback()
        raise


def get_donations_by_donor(session: Session, donor_id: int):
    return (
        session.query(Donation)
        .filter(Donation.donor_id == donor_id)
        .order_by(Donation.donation_date.desc())
        .all()
    )


# =========================================================
# INVENTORY
# =========================================================

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


# =========================================================
# MATCHES
# =========================================================

def create_match(session: Session, **data):
    match = Match(**data)

    session.add(match)
    session.commit()
    session.refresh(match)

    return match


def get_matches_by_request(session: Session, request_id: int):
    return (
        session.query(Match)
        .filter(Match.request_id == request_id)
        .order_by(Match.ranking_score.desc())
        .all()
    )


def delete_matches_by_request(session: Session, request_id: int):
    matches = (
        session.query(Match)
        .filter(Match.request_id == request_id)
        .all()
    )

    for match in matches:
        session.delete(match)

    session.commit()