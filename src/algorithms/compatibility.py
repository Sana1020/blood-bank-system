

COMPATIBILITY = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": [
        "O-",
        "O+",
        "A-",
        "A+",
        "B-",
        "B+",
        "AB-",
        "AB+",
    ],
}


def is_compatible(donor_type: str, recipient_type: str) -> bool:
    """
    Check whether a donor blood type is compatible
    with a recipient blood type for red blood cell donation.
    """

    donor_type = donor_type.upper().strip()
    recipient_type = recipient_type.upper().strip()

    if recipient_type not in COMPATIBILITY:
        return False

    return donor_type in COMPATIBILITY[recipient_type]


def get_compatible_donor_types(recipient_type: str) -> list[str]:
    """
    Return all donor blood types compatible with a recipient.
    """

    recipient_type = recipient_type.upper().strip()

    return COMPATIBILITY.get(recipient_type, [])