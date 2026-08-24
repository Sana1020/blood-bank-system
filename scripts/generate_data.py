import random
from datetime import date, timedelta

from src.database.connection import SessionLocal
from src.database.models import (
    BloodInventory,
    BloodRequest,
    Donation,
    Donor,
    Patient,
)

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

NAMES = [
    "Ahmed Ali",
    "Mohamed Hassan",
    "Omar Mahmoud",
    "Youssef Ahmed",
    "Mariam Ali",
    "Sara Mohamed",
    "Nour Hassan",
    "Menna Mahmoud",
]

LOCATIONS = [
    "Mansoura",
    "Talkha",
    "Mit Ghamr",
    "Mahalla",
    "Zagazig",
]

HOSPITALS = [
    "Mansoura General Hospital",
    "Mansoura University Hospital",
    "Mansoura International Hospital",
]


def random_date(days_back=365):
    return date.today() - timedelta(
        days=random.randint(1, days_back)
    )


def generate_donors(session, count=200):
    donors = []

    for i in range(count):
        donor = Donor(
            name=f"{random.choice(NAMES)} {i + 1}",
            age=random.randint(18, 60),
            gender=random.choice(["Male", "Female"]),
            blood_type=random.choice(BLOOD_TYPES),
            phone=f"010{random.randint(10000000, 99999999)}",
            location=random.choice(LOCATIONS),
            latitude=random.uniform(30.9, 31.3),
            longitude=random.uniform(31.1, 31.6),
            is_available=random.choice([True, True, True, False]),
            last_donation_date=random_date(180),
        )

        donors.append(donor)

    session.add_all(donors)
    session.commit()

    return donors


def generate_patients(session, count=50):
    patients = []

    for i in range(count):
        patient = Patient(
            name=f"Patient {i + 1}",
            age=random.randint(1, 80),
            gender=random.choice(["Male", "Female"]),
            blood_type=random.choice(BLOOD_TYPES),
            hospital=random.choice(HOSPITALS),
            location=random.choice(LOCATIONS),
            latitude=random.uniform(30.9, 31.3),
            longitude=random.uniform(31.1, 31.6),
        )

        patients.append(patient)

    session.add_all(patients)
    session.commit()

    return patients


def generate_requests(session, patients):
    requests = []

    for patient in patients:
        if random.random() < 0.7:
            request = BloodRequest(
                patient_id=patient.id,
                blood_type=patient.blood_type,
                units_required=random.randint(1, 4),
                urgency=random.choice(
                    ["Normal", "Urgent", "Emergency"]
                ),
                hospital=patient.hospital,
                location=patient.location,
                latitude=patient.latitude,
                longitude=patient.longitude,
                status="Pending",
            )

            requests.append(request)

    session.add_all(requests)
    session.commit()

    return requests


def generate_donations(session, donors):
    donations = []

    for donor in donors:
        if random.random() < 0.6:
            donation = Donation(
                donor_id=donor.id,
                donation_date=donor.last_donation_date
                or random_date(180),
                blood_type=donor.blood_type,
                units_donated=1,
                location=donor.location,
                status="Completed",
            )

            donations.append(donation)

    session.add_all(donations)
    session.commit()

    return donations


def generate_inventory(session):
    inventory = []

    for blood_type in BLOOD_TYPES:
        item = BloodInventory(
            blood_type=blood_type,
            units_available=random.randint(3, 50),
            low_stock_threshold=10,
        )

        inventory.append(item)

    session.add_all(inventory)
    session.commit()

    return inventory


def main():
    session = SessionLocal()

    try:
        print("Generating dummy data...")

        donors = generate_donors(session, 200)
        print(f"Created {len(donors)} donors.")

        patients = generate_patients(session, 50)
        print(f"Created {len(patients)} patients.")

        requests = generate_requests(session, patients)
        print(f"Created {len(requests)} blood requests.")

        donations = generate_donations(session, donors)
        print(f"Created {len(donations)} donations.")

        inventory = generate_inventory(session)
        print(f"Created {len(inventory)} inventory records.")

        print("\nDummy data generated successfully!")

    finally:
        session.close()


if __name__ == "__main__":
    main()