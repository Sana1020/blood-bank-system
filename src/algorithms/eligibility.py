from datetime import date



# We use 56 days as a simplified project rule.
MIN_DAYS_BETWEEN_DONATIONS = 56


def is_eligible(
    age: int,
    is_available: bool,
    last_donation_date: date | None,
) -> bool:
    """
    Check whether a donor is currently eligible
    to be considered for a blood request.
    """

   
    if not is_available:
        return False

    
    if age < 18 or age > 65:
        return False

   
    if last_donation_date is not None:
        days_since_donation = (
            date.today() - last_donation_date
        ).days

        if days_since_donation < MIN_DAYS_BETWEEN_DONATIONS:
            return False

    return True