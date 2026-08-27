from src.database.connection import SessionLocal
from src.database.crud import get_blood_request, get_all_donors
from src.algorithms.compatibility import is_compatible
from src.algorithms.eligibility import is_eligible

session = SessionLocal()

try:
    request = get_blood_request(session, 12)

    print("REQUEST")
    print("-" * 50)
    print("ID:", request.id)
    print("Blood Type:", request.blood_type)
    print("Units Required:", request.units_required)
    print("Urgency:", request.urgency)

    print("\nCOMPATIBLE + ELIGIBLE DONORS")
    print("-" * 50)

    count = 0

    for donor in get_all_donors(session):

        eligible = is_eligible(
            donor.age,
            donor.is_available,
            donor.last_donation_date,
        )

        compatible = is_compatible(
            donor.blood_type,
            request.blood_type,
        )

        if eligible and compatible:
            count += 1
            print(
                f"ID: {donor.id} | "
                f"Name: {donor.name} | "
                f"Blood Type: {donor.blood_type}"
            )

    print("-" * 50)
    print("Total compatible + eligible:", count)

finally:
    session.close()