import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ---------- extra_time_charge ----------
def test_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0


def test_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)


def test_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


def test_member_gets_extra_included_time():
    assert extra_time_charge("haircut", 45, "junior", True) == 0


def test_junior_extra_time():
    assert extra_time_charge("haircut", 40, "junior", False) == 100


def test_non_junior_extra_time_up_to_60():
    assert extra_time_charge("colour", 90, "senior", False) == 540


def test_senior_extra_time_over_60():
    assert extra_time_charge("spa", 200, "senior", False) == 3300


# ---------- can_book ----------
def test_can_book():
    assert can_book(2, 1, False) is True


def test_walk_in_booking():
    assert can_book(2, 1, True) is True


def test_party_size_too_large():
    assert can_book(5, 1, False) is False


# ---------- arrival_status ----------
def test_arrival_open_colour_weekend():
    assert arrival_status(20, True, True) == "open"


def test_arrival_open_non_colour_weekday():
    assert arrival_status(5, False, False) == "open"


def test_arrival_late():
    assert arrival_status(0, False, False) == "late"


def test_arrival_closed():
    assert arrival_status(-11, False, False) == "closed"