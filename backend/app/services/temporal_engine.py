import re
from datetime import datetime
from typing import Optional, List, Dict, Any

class TemporalEngine:
    MONTH_MAP = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12
    }

    @classmethod
    def parse_date(cls, text: str) -> Optional[datetime]:
        """
        Deterministically parses date strings into Python datetime objects.
        Supports: '2026-09-15', 'Sept 15, 2026', 'September 15', '15 Sep 2026', '09/15/2026'
        """
        if not text:
            return None
        text_str = str(text).strip()

        # ISO format YYYY-MM-DD
        iso_match = re.search(r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', text_str)
        if iso_match:
            try:
                return datetime(int(iso_match.group(1)), int(iso_match.group(2)), int(iso_match.group(3)))
            except ValueError:
                pass

        # Month Day, Year (e.g., September 15, 2026 or Sept 15)
        month_day_match = re.search(r'\b([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?(?:\s*,\s*(\d{4}))?\b', text_str, re.IGNORECASE)
        if month_day_match:
            m_str = month_day_match.group(1).lower()
            m_num = cls.MONTH_MAP.get(m_str) or cls.MONTH_MAP.get(m_str[:3])
            if m_num:
                day = int(month_day_match.group(2))
                year = int(month_day_match.group(3)) if month_day_match.group(3) else 2026
                try:
                    return datetime(year, m_num, day)
                except ValueError:
                    pass

        # Day Month Year (e.g. 15 Sept 2026)
        day_month_match = re.search(r'\b(\d{1,2})\s+([A-Za-z]{3,9})\.?\s*(\d{4})?\b', text_str, re.IGNORECASE)
        if day_month_match:
            day = int(day_month_match.group(1))
            m_str = day_month_match.group(2).lower()
            m_num = cls.MONTH_MAP.get(m_str) or cls.MONTH_MAP.get(m_str[:3])
            year = int(day_month_match.group(3)) if day_month_match.group(3) else 2026
            if m_num:
                try:
                    return datetime(year, m_num, day)
                except ValueError:
                    pass

        return None

    @classmethod
    def format_iso(cls, dt: Optional[datetime]) -> Optional[str]:
        return dt.strftime("%Y-%m-%d") if dt else None

    @classmethod
    def is_after(cls, date_a_str: str, date_b_str: str) -> Optional[bool]:
        """Returns True if Date A > Date B deterministically."""
        dt_a = cls.parse_date(date_a_str)
        dt_b = cls.parse_date(date_b_str)
        if dt_a and dt_b:
            return dt_a > dt_b
        return None

    @classmethod
    def check_deadline_violation(cls, event_date_str: str, deadline_date_str: str) -> Dict[str, Any]:
        """
        Determines if an event date violates a deadline date deterministically.
        """
        dt_event = cls.parse_date(event_date_str)
        dt_deadline = cls.parse_date(deadline_date_str)

        if not dt_event or not dt_deadline:
            return {"violated": False, "reason": "Unparseable date comparison"}

        is_violated = dt_event > dt_deadline
        return {
            "violated": is_violated,
            "event_date": dt_event.strftime("%Y-%m-%d"),
            "deadline_date": dt_deadline.strftime("%Y-%m-%d"),
            "days_late": (dt_event - dt_deadline).days if is_violated else 0
        }
