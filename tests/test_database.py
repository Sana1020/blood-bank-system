from src.database.connection import SessionLocal
from src.database.crud import (
    get_all_donors,
    get_all_patients,
    get_all_blood_requests,
    get_inventory,
)


def test_database_data():
    session = SessionLocal()

    try:
        donors = get_all_donors(session)
        patients = get_all_patients(session)
        requests = get_all_blood_requests(session)
        inventory = get_inventory(session)

        print(f"Donors: {len(donors)}")
        print(f"Patients: {len(patients)}")
        print(f"Blood Requests: {len(requests)}")
        print(f"Inventory Records: {len(inventory)}")

    finally:
        session.close()


if __name__ == "__main__":
    test_database_data()