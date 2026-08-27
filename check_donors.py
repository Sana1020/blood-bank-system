from src.database.connection import SessionLocal
from src.database.models import Donor


session = SessionLocal()

try:
    donors = (
        session.query(Donor)
        .order_by(Donor.id)
        .all()
    )

    print("\nCurrent Donors:")
    print("-" * 60)

    for donor in donors:
        print(
            f"ID: {donor.id} | "
            f"Name: {donor.name} | "
            f"Blood Type: {donor.blood_type} | "
            f"Location: {donor.location}"
        )

    print("-" * 60)
    print(f"Total donors: {len(donors)}")

finally:
    session.close()