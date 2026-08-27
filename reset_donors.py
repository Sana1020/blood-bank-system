from src.database.connection import SessionLocal
from src.database.models import Donor, Donation, Match


session = SessionLocal()

try:
    # Delete matches related to donors
    session.query(Match).delete(synchronize_session=False)

    # Delete donations related to donors
    session.query(Donation).delete(synchronize_session=False)

    # Delete all donors
    session.query(Donor).delete(synchronize_session=False)

    session.commit()

    print("All old donor data deleted successfully.")

finally:
    session.close()