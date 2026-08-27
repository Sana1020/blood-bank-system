from datetime import date, timedelta

from src.algorithms.compatibility import (
    is_compatible,
    get_compatible_donor_types,
)
from src.algorithms.distance import calculate_distance
from src.algorithms.eligibility import is_eligible
from src.algorithms.ranking import calculate_ranking_score


# =========================
# Compatibility Tests
# =========================

def test_compatible_blood_types():
    assert is_compatible("O-", "A+")
    assert is_compatible("A+", "A+")
    assert is_compatible("B-", "AB-")


def test_incompatible_blood_types():
    assert not is_compatible("B+", "A+")
    assert not is_compatible("A+", "O-")


def test_compatible_donor_types():
    donors = get_compatible_donor_types("A+")

    assert "O-" in donors
    assert "O+" in donors
    assert "A-" in donors
    assert "A+" in donors


# =========================
# Distance Tests
# =========================

def test_distance_same_location():
    distance = calculate_distance(
        31.0400,
        31.3800,
        31.0400,
        31.3800,
    )

    assert distance == 0


def test_distance_is_positive():
    distance = calculate_distance(
        31.0400,
        31.3800,
        31.0500,
        31.3900,
    )

    assert distance > 0


# =========================
# Eligibility Tests
# =========================

def test_eligible_donor():
    result = is_eligible(
        age=25,
        is_available=True,
        last_donation_date=date.today() - timedelta(days=100),
    )

    assert result is True


def test_unavailable_donor():
    result = is_eligible(
        age=25,
        is_available=False,
        last_donation_date=date.today() - timedelta(days=100),
    )

    assert result is False


def test_invalid_age():
    result = is_eligible(
        age=17,
        is_available=True,
        last_donation_date=date.today() - timedelta(days=100),
    )

    assert result is False


def test_recent_donation():
    result = is_eligible(
        age=25,
        is_available=True,
        last_donation_date=date.today() - timedelta(days=20),
    )

    assert result is False


# =========================
# Ranking Tests
# =========================

def test_ranking_score():
    score = calculate_ranking_score(
        compatibility_score=100,
        distance_km=5,
        urgency="Emergency",
    )

    assert score == 92.5


def test_better_distance_gives_higher_score():
    near_score = calculate_ranking_score(
        compatibility_score=100,
        distance_km=2,
        urgency="Emergency",
    )

    far_score = calculate_ranking_score(
        compatibility_score=100,
        distance_km=10,
        urgency="Emergency",
    )

    assert near_score > far_score


def test_emergency_has_higher_score_than_normal():
    emergency_score = calculate_ranking_score(
        compatibility_score=100,
        distance_km=5,
        urgency="Emergency",
    )

    normal_score = calculate_ranking_score(
        compatibility_score=100,
        distance_km=5,
        urgency="Normal",
    )

    assert emergency_score > normal_score