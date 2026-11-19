import math
from hypothesis import given, strategies as st
from salon_booking import parse_booking, duration_average, payable_bill


# ---------- No-crash fuzz tests (random text and None) ----------
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"


@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    try:
        duration_average(s)
    except Exception as e:
        assert False, f"duration_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed with: {e!r}"


# ---------- Property tests (valid inputs must give sensible results) ----------
@given(st.text() | st.none())
def test_parse_booking_result_is_valid(s):
    result = parse_booking(s)
    if result is not None:
        service, minutes = result
        assert service != ""
        assert math.isfinite(minutes) and minutes >= 0


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_duration_average_matches_sum_over_count(values):
    csv = ",".join(str(v) for v in values)
    assert duration_average(csv) == sum(values) // len(values)


@given(st.floats(min_value=0, max_value=1e6), st.floats(min_value=0, max_value=1e6))
def test_payable_bill_never_negative(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert result is not None and result >= 0