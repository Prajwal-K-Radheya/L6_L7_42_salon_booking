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


def test_exactly_included_time_is_free():
    assert extra_time_charge("haircut", 30, "junior", False) == 0


def test_member_gets_extra_15_min():
    # haircut member: included 45, duration 45 -> no charge
    assert extra_time_charge("haircut", 45, "junior", True) == 0
    # duration 55 -> extra 10 * 10
    assert extra_time_charge("haircut", 55, "junior", True) == 100


def test_member_spa_gets_no_bonus():
    # spa included stays 90; duration 100 -> extra 10 * 10
    assert extra_time_charge("spa", 100, "junior", True) == 100


def test_junior_rate_no_surcharge():
    assert extra_time_charge("haircut", 40, "junior", False) == 10 * 10


def test_non_junior_standard_rate():
    assert extra_time_charge("haircut", 40, "senior", False) == 10 * 18
    assert extra_time_charge("haircut", 40, "mid", False) == 10 * 18


def test_over_60_extra_junior():
    # extra = 70 > 60, rate 10+8 = 18
    assert extra_time_charge("haircut", 100, "junior", False) == 70 * 18


def test_over_60_extra_senior_gets_additional_surcharge():
    # rate 18 + 8 + 4 = 30
    assert extra_time_charge("haircut", 100, "senior", False) == 70 * 30


def test_over_60_extra_other_level():
    # rate 18 + 8 = 26
    assert extra_time_charge("haircut", 100, "mid", False) == 70 * 26


def test_extra_exactly_60_no_surcharge():
    assert extra_time_charge("haircut", 90, "junior", False) == 60 * 10


def test_colour_and_spa_services():
    assert extra_time_charge("colour", 70, "junior", False) == 100
    assert extra_time_charge("spa", 100, "senior", False) == 180


# ---------- can_book ----------
def test_can_book():
    assert can_book(2, 1, False) is True


def test_walk_in_small_party():
    assert can_book(2, 5, True) is True


def test_walk_in_large_party():
    assert can_book(3, 1, True) is False


def test_booking_party_too_large():
    assert can_book(5, 1, False) is False


def test_booking_too_many_services():
    assert can_book(4, 3, False) is False


def test_booking_boundaries():
    assert can_book(4, 2, False) is True


# ---------- arrival_status ----------
def test_open_non_colour_weekday():
    assert arrival_status(5, False, False) == "open"


def test_late_non_colour_weekday():
    assert arrival_status(4, False, False) == "late"
    assert arrival_status(-10, False, False) == "late"


def test_closed_non_colour_weekday():
    assert arrival_status(-11, False, False) == "closed"


def test_colour_cutoff():
    assert arrival_status(10, True, False) == "open"
    assert arrival_status(9, True, False) == "late"
    assert arrival_status(-6, True, False) == "closed"


def test_weekend_adds_10():
    assert arrival_status(14, False, True) == "late"
    assert arrival_status(15, False, True) == "open"
    assert arrival_status(-1, False, True) == "closed"
    assert arrival_status(20, True, True) == "open"
