import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ---------- extra_time_charge: validation ----------
def test_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)


def test_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


def test_zero_duration():
    assert extra_time_charge("haircut", 0, "junior", False) == 0


# ---------- extra_time_charge: membership ----------
def test_non_member_haircut_no_bonus_time():
    assert extra_time_charge("haircut", 45, "junior", False) == 150


def test_member_haircut_gets_bonus_time():
    assert extra_time_charge("haircut", 45, "junior", True) == 0


def test_member_spa_gets_no_bonus_time():
    assert extra_time_charge("spa", 100, "junior", True) == 100


# ---------- extra_time_charge: extra time boundary ----------
def test_extra_exactly_zero():
    assert extra_time_charge("colour", 60, "junior", False) == 0


def test_extra_one_minute():
    assert extra_time_charge("haircut", 31, "junior", False) == 10


# ---------- extra_time_charge: stylist level ----------
def test_junior_rate():
    assert extra_time_charge("haircut", 40, "junior", False) == 100


def test_senior_rate_up_to_60():
    assert extra_time_charge("colour", 90, "senior", False) == 540


def test_other_level_rate_up_to_60():
    assert extra_time_charge("haircut", 40, "intermediate", False) == 180


# ---------- extra_time_charge: long overrun (> 60) ----------
def test_extra_exactly_60_no_surcharge():
    assert extra_time_charge("haircut", 90, "junior", False) == 600


def test_junior_extra_over_60():
    assert extra_time_charge("haircut", 91, "junior", False) == 1098


def test_senior_extra_over_60():
    assert extra_time_charge("spa", 200, "senior", False) == 3300


def test_other_level_extra_over_60_no_senior_surcharge():
    assert extra_time_charge("haircut", 100, "intermediate", False) == 1820


# ---------- can_book ----------
def test_walk_in_party_of_two():
    assert can_book(2, 1, True) is True


def test_walk_in_party_of_three():
    assert can_book(3, 1, True) is False


def test_booking_party_too_large():
    assert can_book(5, 1, False) is False


def test_booking_party_of_four_two_services():
    assert can_book(4, 2, False) is True


def test_booking_party_of_four_three_services():
    assert can_book(4, 3, False) is False


def test_booking_single_guest_one_service():
    assert can_book(1, 1, False) is True


# ---------- arrival_status ----------
def test_non_colour_weekday_open():
    assert arrival_status(5, False, False) == "open"


def test_non_colour_weekday_late():
    assert arrival_status(4, False, False) == "late"


def test_non_colour_weekday_late_lower_edge():
    assert arrival_status(-10, False, False) == "late"


def test_non_colour_weekday_closed():
    assert arrival_status(-11, False, False) == "closed"


def test_colour_weekday_open():
    assert arrival_status(10, True, False) == "open"


def test_colour_weekday_late():
    assert arrival_status(9, True, False) == "late"


def test_colour_weekday_closed():
    assert arrival_status(-6, True, False) == "closed"


def test_non_colour_weekend_open():
    assert arrival_status(15, False, True) == "open"


def test_non_colour_weekend_late():
    assert arrival_status(14, False, True) == "late"


def test_non_colour_weekend_closed():
    assert arrival_status(-1, False, True) == "closed"


def test_colour_weekend_open():
    assert arrival_status(20, True, True) == "open"


def test_colour_weekend_late():
    assert arrival_status(19, True, True) == "late"


def test_colour_weekend_closed():
    assert arrival_status(4, True, True) == "closed"