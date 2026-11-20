from hypothesis import given, strategies as st
from salon_booking import parse_booking, duration_average, payable_bill

# Fuzz tests: any input must either succeed or raise a clean ValueError.
# Any other exception (AttributeError, TypeError, OverflowError, ...) is a bug.

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        service, minutes = parse_booking(s)
        assert isinstance(service, str) and minutes >= 0
    except ValueError:
        pass


@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    try:
        assert isinstance(duration_average(s), int)
    except ValueError:
        pass


@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        assert payable_bill(s) >= 0
    except ValueError:
        pass


# Targeted regression tests for the crashes fuzzing exposes
def test_known_good_inputs():
    assert parse_booking("haircut:45") == ("Haircut", 45.0)
    assert duration_average("30,45,60") == 45
    assert round(payable_bill("800|100"), 2) == 844.0
