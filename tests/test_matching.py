from datetime import date, timedelta

from src.database.connection import SessionLocal
from src.database.models import Donor, Patient, BloodRequest
from src.services.matching_service import find_matches


def test_matching_returns_compatible_donors():
    session = SessionLocal()

    try:
        patient = Patient(
            name="Test Patient",
            age=30,
            gender="Male",
            blood_type="A+",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
        )

        session.add(patient)
        session.commit()
        session.refresh(patient)

        compatible_donor = Donor(
            name="Compatible Donor",
            age=25,
            gender="Male",
            blood_type="A+",
            phone="01000000000",
            location="Mansoura",
            latitude=31.0410,
            longitude=31.3810,
            is_available=True,
            last_donation_date=date.today() - timedelta(days=100),
        )

        incompatible_donor = Donor(
            name="Incompatible Donor",
            age=25,
            gender="Male",
            blood_type="B+",
            phone="01000000001",
            location="Mansoura",
            latitude=31.0410,
            longitude=31.3810,
            is_available=True,
            last_donation_date=date.today() - timedelta(days=100),
        )

        session.add_all([
            compatible_donor,
            incompatible_donor,
        ])
        session.commit()

        request = BloodRequest(
            patient_id=patient.id,
            blood_type="A+",
            units_required=1000,
            urgency="Emergency",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
            status="Pending",
        )

        session.add(request)
        session.commit()
        session.refresh(request)

        matches = find_matches(session, request.id)

        donor_ids = [match.donor_id for match in matches]

        assert compatible_donor.id in donor_ids
        assert incompatible_donor.id not in donor_ids

    finally:
        session.close()
def test_unavailable_donor_is_not_matched():
    session = SessionLocal()

    try:
        patient = Patient(
            name="Test Patient 2",
            age=30,
            gender="Male",
            blood_type="A+",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
        )
        session.add(patient)
        session.commit()
        session.refresh(patient)

        donor = Donor(
            name="Unavailable Donor",
            age=25,
            gender="Male",
            blood_type="A+",
            phone="01000000002",
            location="Mansoura",
            latitude=31.0410,
            longitude=31.3810,
            is_available=False,
            last_donation_date=date.today() - timedelta(days=100),
        )
        session.add(donor)
        session.commit()

        request = BloodRequest(
            patient_id=patient.id,
            blood_type="A+",
            units_required=1,
            urgency="Emergency",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
            status="Pending",
        )
        session.add(request)
        session.commit()
        session.refresh(request)

        matches = find_matches(session, request.id)

        donor_ids = [match.donor_id for match in matches]

        assert donor.id not in donor_ids

    finally:
        session.close()


def test_recent_donor_is_not_matched():
    session = SessionLocal()

    try:
        patient = Patient(
            name="Test Patient 3",
            age=30,
            gender="Male",
            blood_type="A+",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
        )
        session.add(patient)
        session.commit()
        session.refresh(patient)

        donor = Donor(
            name="Recent Donor",
            age=25,
            gender="Male",
            blood_type="A+",
            phone="01000000003",
            location="Mansoura",
            latitude=31.0410,
            longitude=31.3810,
            is_available=True,
            last_donation_date=date.today() - timedelta(days=20),
        )
        session.add(donor)
        session.commit()

        request = BloodRequest(
            patient_id=patient.id,
            blood_type="A+",
            units_required=1,
            urgency="Emergency",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
            status="Pending",
        )
        session.add(request)
        session.commit()
        session.refresh(request)

        matches = find_matches(session, request.id)

        donor_ids = [match.donor_id for match in matches]

        assert donor.id not in donor_ids

    finally:
        session.close()


def test_matches_are_sorted_by_ranking_score():
    session = SessionLocal()

    try:
        patient = Patient(
            name="Test Patient 4",
            age=30,
            gender="Male",
            blood_type="A+",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
        )
        session.add(patient)
        session.commit()
        session.refresh(patient)

        donor_near = Donor(
            name="Near Donor",
            age=25,
            gender="Male",
            blood_type="A+",
            phone="01000000004",
            location="Mansoura",
            latitude=31.0410,
            longitude=31.3810,
            is_available=True,
            last_donation_date=date.today() - timedelta(days=100),
        )

        donor_far = Donor(
            name="Far Donor",
            age=25,
            gender="Male",
            blood_type="A+",
            phone="01000000005",
            location="Mansoura",
            latitude=31.1000,
            longitude=31.4500,
            is_available=True,
            last_donation_date=date.today() - timedelta(days=100),
        )

        session.add_all([donor_near, donor_far])
        session.commit()

        request = BloodRequest(
            patient_id=patient.id,
            blood_type="A+",
            units_required=1,
            urgency="Emergency",
            hospital="Test Hospital",
            location="Mansoura",
            latitude=31.0400,
            longitude=31.3800,
            status="Pending",
        )
        session.add(request)
        session.commit()
        session.refresh(request)

        matches = find_matches(session, request.id)

        scores = [match.ranking_score for match in matches]

        assert scores == sorted(scores, reverse=True)

    finally:
        session.close()