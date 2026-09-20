import pytest
from app.services.temporal_engine import TemporalEngine

def test_date_parsing_formats():
    dt1 = TemporalEngine.parse_date("2026-09-15")
    dt2 = TemporalEngine.parse_date("September 15, 2026")
    dt3 = TemporalEngine.parse_date("15 Sept 2026")

    assert dt1 is not None
    assert dt1.year == 2026 and dt1.month == 9 and dt1.day == 15
    assert dt2.month == 9 and dt2.day == 15
    assert dt3.day == 15

def test_deadline_violation_check():
    res = TemporalEngine.check_deadline_violation("2026-09-17", "2026-09-15")
    assert res["violated"] is True
    assert res["days_late"] == 2

    res_met = TemporalEngine.check_deadline_violation("2026-09-14", "2026-09-15")
    assert res_met["violated"] is False
