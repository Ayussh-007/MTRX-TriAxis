"""
MTRX-TriAxis | Calendar & Holiday Planner
Provides holiday awareness, calendar data, and AI-powered date-based
teaching suggestions.
"""

import calendar
from datetime import date, timedelta
from backend.llm_utils import get_llm


# ----- Indian National & Common Holidays -----
# Format: (month, day): "Holiday Name"
# Covers major national holidays + common school holidays

INDIAN_HOLIDAYS = {
    # Fixed-date national holidays
    (1, 26): "Republic Day",
    (8, 15): "Independence Day",
    (10, 2): "Gandhi Jayanti",

    # Common school holidays (approximate — varies by year/region)
    (1, 1): "New Year's Day",
    (1, 14): "Makar Sankranti",
    (3, 29): "Holi",
    (4, 14): "Ambedkar Jayanti",
    (5, 1): "May Day",
    (8, 19): "Janmashtami",
    (9, 5): "Teachers' Day",
    (10, 12): "Dussehra",
    (10, 24): "Diwali",
    (10, 25): "Diwali (Day 2)",
    (11, 1): "Kannada Rajyotsava",
    (11, 15): "Guru Nanak Jayanti",
    (12, 25): "Christmas",

    # School vacation markers
    (5, 10): "Summer Vacation Begins (approx)",
    (6, 15): "Summer Vacation Ends (approx)",
}


def get_holidays_for_month(year: int, month: int) -> list[dict]:
    """
    Get all holidays for a given month.

    Returns:
        List of dicts: [{date, name, day_of_week}, ...]
    """
    holidays = []
    for (m, d), name in INDIAN_HOLIDAYS.items():
        if m == month:
            try:
                dt = date(year, m, d)
                holidays.append({
                    "date": dt.isoformat(),
                    "day": d,
                    "name": name,
                    "day_of_week": dt.strftime("%A"),
                })
            except ValueError:
                pass  # Invalid date

    holidays.sort(key=lambda x: x["day"])
    return holidays


def get_upcoming_holidays(days_ahead: int = 14) -> list[dict]:
    """
    Get holidays coming up in the next N days.

    Returns:
        List of dicts with date, name, and days_until.
    """
    today = date.today()
    upcoming = []

    for day_offset in range(days_ahead + 1):
        check_date = today + timedelta(days=day_offset)
        key = (check_date.month, check_date.day)

        if key in INDIAN_HOLIDAYS:
            upcoming.append({
                "date": check_date.isoformat(),
                "name": INDIAN_HOLIDAYS[key],
                "days_until": day_offset,
                "day_of_week": check_date.strftime("%A"),
            })

    return upcoming


def is_holiday_today() -> dict:
    """
    Check if today is a holiday.

    Returns:
        Dict with name and is_holiday flag, or None.
    """
    today = date.today()
    key = (today.month, today.day)

    if key in INDIAN_HOLIDAYS:
        return {
            "is_holiday": True,
            "name": INDIAN_HOLIDAYS[key],
            "date": today.isoformat(),
        }

    # Also check if today is a weekend
    if today.weekday() >= 5:  # Saturday/Sunday
        return {
            "is_holiday": True,
            "name": "Weekend" if today.weekday() == 5 else "Weekend (Sunday)",
            "date": today.isoformat(),
        }

    return {"is_holiday": False, "name": None, "date": today.isoformat()}


def get_month_calendar(year: int = None, month: int = None) -> list[list[int]]:
    """
    Get the calendar grid for a month.

    Returns:
        List of week lists (0 = days from other months).
    """
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month

    cal = calendar.Calendar(firstweekday=0)  # Monday first
    return cal.monthdayscalendar(year, month)


def get_teaching_suggestion_for_date(target_date: date = None) -> str:
    """
    Generate an AI teaching suggestion based on the date context
    (holidays, weekends, vacation proximity).

    Args:
        target_date: The date to check. Defaults to today.

    Returns:
        AI-generated teaching suggestion string.
    """
    if target_date is None:
        target_date = date.today()

    # Gather context
    upcoming = get_upcoming_holidays(days_ahead=7)
    today_status = is_holiday_today()

    # Check if we're near a holiday
    holiday_context = ""
    if today_status["is_holiday"]:
        holiday_context = f"Today is {today_status['name']}. "
    if upcoming:
        names = [f"{h['name']} ({h['days_until']} day(s) away)" for h in upcoming if h['days_until'] > 0]
        if names:
            holiday_context += f"Upcoming holidays: {', '.join(names[:3])}. "

    if not holiday_context:
        return (
            f"📅 **{target_date.strftime('%A, %B %d')}** — "
            "No holidays nearby. Great day for regular teaching!"
        )

    # Generate AI suggestion
    prompt = f"""You are a school planning assistant.

Today is {target_date.strftime('%A, %B %d, %Y')}.
{holiday_context}

Based on this context, provide a brief teaching plan suggestion:
- Should the teacher introduce new topics or revise?
- Any special activities to consider?
- How to handle students' attention around holidays?

Keep it to 3-4 concise bullet points. Be practical and supportive."""

    llm = get_llm(temperature=0.6)
    return llm.invoke(prompt)
