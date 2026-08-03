"""Global market hours service.

Provides open/close status, next open time, and trading calendar
for major stock exchanges worldwide. Handles timezones, DST, and holidays.
"""

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, time, timezone
from typing import Optional

logger = logging.getLogger(__name__)

WEEKEND = {5, 6}

EXCHANGE_INFO: dict[str, dict] = {
    "NYSE": {"name": "New York Stock Exchange", "country": "US", "tz": "America/New_York", "open": time(9, 30), "close": time(16, 0)},
    "NASDAQ": {"name": "NASDAQ", "country": "US", "tz": "America/New_York", "open": time(9, 30), "close": time(16, 0)},
    "TSX": {"name": "Toronto Stock Exchange", "country": "CA", "tz": "America/Toronto", "open": time(9, 30), "close": time(16, 0)},
    "LSE": {"name": "London Stock Exchange", "country": "GB", "tz": "Europe/London", "open": time(8, 0), "close": time(16, 30)},
    "EURONEXT": {"name": "Euronext", "country": "NL", "tz": "Europe/Amsterdam", "open": time(9, 0), "close": time(17, 30)},
    "XETRA": {"name": "Deutsche Börse Xetra", "country": "DE", "tz": "Europe/Berlin", "open": time(9, 0), "close": time(17, 30)},
    "SIX": {"name": "SIX Swiss Exchange", "country": "CH", "tz": "Europe/Zurich", "open": time(9, 0), "close": time(17, 30)},
    "TSE": {"name": "Tokyo Stock Exchange", "country": "JP", "tz": "Asia/Tokyo", "open": time(9, 0), "close": time(15, 0), "lunch_start": time(11, 30), "lunch_end": time(12, 30)},
    "HKEX": {"name": "Hong Kong Stock Exchange", "country": "HK", "tz": "Asia/Hong_Kong", "open": time(9, 30), "close": time(16, 0), "lunch_start": time(12, 0), "lunch_end": time(13, 0)},
    "SSE": {"name": "Shanghai Stock Exchange", "country": "CN", "tz": "Asia/Shanghai", "open": time(9, 30), "close": time(15, 0), "lunch_start": time(11, 30), "lunch_end": time(13, 0)},
    "NSE": {"name": "National Stock Exchange of India", "country": "IN", "tz": "Asia/Kolkata", "open": time(9, 15), "close": time(15, 30)},
    "ASX": {"name": "Australian Securities Exchange", "country": "AU", "tz": "Australia/Sydney", "open": time(10, 0), "close": time(16, 0)},
    "B3": {"name": "B3 Brazil", "country": "BR", "tz": "America/Sao_Paulo", "open": time(10, 0), "close": time(17, 0)},
    "BMV": {"name": "Bolsa Mexicana de Valores", "country": "MX", "tz": "America/Mexico_City", "open": time(8, 30), "close": time(15, 0)},
    "MERVAL": {"name": "BCBA Merval", "country": "AR", "tz": "America/Argentina/Buenos_Aires", "open": time(11, 0), "close": time(17, 0)},
    "BCS": {"name": "Santiago Stock Exchange", "country": "CL", "tz": "America/Santiago", "open": time(9, 30), "close": time(16, 0)},
    "DFM": {"name": "Dubai Financial Market", "country": "AE", "tz": "Asia/Dubai", "open": time(10, 0), "close": time(15, 0)},
    "TADAWUL": {"name": "Saudi Stock Exchange", "country": "SA", "tz": "Asia/Riyadh", "open": time(10, 0), "close": time(15, 0)},
    "JSE": {"name": "Johannesburg Stock Exchange", "country": "ZA", "tz": "Africa/Johannesburg", "open": time(9, 0), "close": time(17, 0)},
}

HOLIDAYS: dict[str, set[tuple[int, int, int]]] = {
    "NYSE": {
        (1, 1), (1, 20, 2025), (2, 17), (4, 18), (5, 26), (6, 19), (7, 4), (9, 1), (11, 27), (12, 25),
    },
    "LSE": {
        (1, 1), (4, 18), (4, 21), (5, 5), (5, 26), (8, 25), (12, 25), (12, 26),
    },
    "TSE": {
        (1, 1), (1, 13), (2, 11), (2, 23), (3, 21), (4, 29), (5, 3), (5, 4), (5, 5), (7, 21), (8, 11), (9, 23), (10, 13), (11, 3), (11, 23), (12, 31),
    },
    "HKEX": {
        (1, 1), (1, 29), (1, 30), (1, 31), (4, 4), (4, 18), (4, 21), (5, 1), (5, 5), (10, 1), (10, 7), (12, 25), (12, 26),
    },
    "SSE": {
        (1, 1), (1, 28), (1, 29), (1, 30), (1, 31), (2, 1), (2, 2), (2, 3), (2, 4), (4, 4), (5, 1), (5, 2), (5, 5), (10, 1), (10, 2), (10, 3), (10, 6), (10, 7), (10, 8),
    },
    "NSE": {
        (1, 26), (3, 14), (3, 31), (4, 10), (4, 14), (4, 18), (5, 1), (8, 15), (8, 27), (10, 2), (10, 21), (11, 3), (12, 25),
    },
    "ASX": {
        (1, 1), (1, 27), (4, 18), (4, 21), (4, 25), (6, 9), (10, 6), (12, 25), (12, 26),
    },
    "B3": {
        (1, 1), (4, 18), (4, 21), (5, 1), (6, 19), (9, 7), (10, 12), (11, 15), (11, 20), (12, 25),
    },
    "BMV": {
        (1, 1), (2, 3), (3, 17), (4, 17), (4, 18), (5, 1), (5, 5), (9, 16), (11, 18), (12, 12), (12, 25),
    },
    "JSE": {
        (1, 1), (3, 21), (4, 18), (4, 21), (4, 27), (5, 1), (6, 16), (8, 9), (9, 24), (12, 16), (12, 25), (12, 26),
    },
}

EASTER_MONDAY_EXCHANGES = {"LSE", "EURONEXT", "XETRA", "SIX", "ASX", "B3", "JSE"}


def _get_holidays_for_year(exchange: str, year: int) -> set[date]:
    holidays = HOLIDAYS.get(exchange, set())
    result = set()
    for h in holidays:
        if len(h) == 2:
            month, day = h
            result.add(date(year, month, day))
        elif len(h) == 3:
            h_year, month, day = h
            if h_year == year:
                result.add(date(year, month, day))
    return result


@dataclass
class MarketHours:
    exchange: str
    date: date
    is_open: bool
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    lunch_start: Optional[time] = None
    lunch_end: Optional[time] = None
    next_open: Optional[datetime] = None
    timezone: str = "UTC"
    reason: str = ""


class MarketHoursService:
    """Service for querying market hours, open status, and holidays."""

    @staticmethod
    def get_exchange_info(exchange: str) -> Optional[dict]:
        code = exchange.upper()
        return EXCHANGE_INFO.get(code)

    @staticmethod
    def list_exchanges() -> list[dict]:
        return [
            {"code": code, **{k: v for k, v in info.items() if k in ("name", "country")}}
            for code, info in EXCHANGE_INFO.items()
        ]

    @staticmethod
    def is_open(exchange: str, when: Optional[datetime] = None) -> bool:
        return MarketHoursService.market_hours(exchange, when).is_open

    @staticmethod
    def next_open(exchange: str, after: Optional[datetime] = None) -> Optional[datetime]:
        info = EXCHANGE_INFO.get(exchange.upper())
        if not info:
            return None
        tz_name = info["tz"]
        try:
            import zoneinfo
            tz = zoneinfo.ZoneInfo(tz_name)
        except Exception:
            return None

        now = (after or datetime.now(timezone.utc)).astimezone(tz)
        check = now.replace(second=0, microsecond=0)

        for _ in range(365):
            check += timedelta(days=1)
            if check.weekday() in WEEKEND:
                continue
            if MarketHoursService._is_holiday(exchange.upper(), check.date()):
                continue
            dt_open = datetime.combine(check.date(), info["open"], tz)
            return dt_open

        return None

    @staticmethod
    def _is_holiday(exchange: str, d: date) -> bool:
        holidays = _get_holidays_for_year(exchange, d.year)
        if d in holidays:
            return True
        if exchange in EASTER_MONDAY_EXCHANGES:
            from dateutil.easter import easter
            try:
                easter_date = easter(d.year)
                if d == easter_date + timedelta(days=1):
                    return True
            except Exception:
                pass
        return False

    @staticmethod
    def market_hours(exchange: str, when: Optional[datetime] = None) -> MarketHours:
        code = exchange.upper()
        info = EXCHANGE_INFO.get(code)
        if not info:
            return MarketHours(exchange=code, date=date.today(), is_open=False, reason="Unknown exchange")

        tz_name = info["tz"]
        try:
            import zoneinfo
            tz = zoneinfo.ZoneInfo(tz_name)
        except Exception:
            tz = timezone.utc

        now = (when or datetime.now(timezone.utc)).astimezone(tz)
        today = now.date()

        if now.weekday() in WEEKEND:
            next_open = MarketHoursService.next_open(exchange, now)
            return MarketHours(
                exchange=code, date=today, is_open=False,
                open_time=info["open"], close_time=info["close"],
                timezone=tz_name, next_open=next_open, reason="Weekend",
            )

        if MarketHoursService._is_holiday(code, today):
            next_open = MarketHoursService.next_open(exchange, now)
            return MarketHours(
                exchange=code, date=today, is_open=False,
                open_time=info["open"], close_time=info["close"],
                timezone=tz_name, next_open=next_open, reason="Holiday",
            )

        open_dt = datetime.combine(today, info["open"], tz)
        close_dt = datetime.combine(today, info["close"], tz)

        if now < open_dt:
            return MarketHours(
                exchange=code, date=today, is_open=False,
                open_time=info["open"], close_time=info["close"],
                timezone=tz_name, next_open=open_dt, reason="Before open",
            )

        if now > close_dt:
            next_open = MarketHoursService.next_open(exchange, now)
            return MarketHours(
                exchange=code, date=today, is_open=False,
                open_time=info["open"], close_time=info["close"],
                timezone=tz_name, next_open=next_open, reason="After close",
            )

        lunch_start = info.get("lunch_start")
        lunch_end = info.get("lunch_end")
        if lunch_start and lunch_end:
            lunch_start_dt = datetime.combine(today, lunch_start, tz)
            lunch_end_dt = datetime.combine(today, lunch_end, tz)
            if lunch_start_dt <= now < lunch_end_dt:
                next_open = lunch_end_dt
                return MarketHours(
                    exchange=code, date=today, is_open=False,
                    open_time=info["open"], close_time=info["close"],
                    lunch_start=lunch_start, lunch_end=lunch_end,
                    timezone=tz_name, next_open=next_open, reason="Lunch break",
                )

        return MarketHours(
            exchange=code, date=today, is_open=True,
            open_time=info["open"], close_time=info["close"],
            lunch_start=info.get("lunch_start"), lunch_end=info.get("lunch_end"),
            timezone=tz_name,
        )


class MarketHolidayService:
    """Service for querying market holiday calendars."""

    @staticmethod
    def get_holidays(exchange: str, year: Optional[int] = None) -> list[dict]:
        year = year or date.today().year
        holidays = _get_holidays_for_year(exchange.upper(), year)
        info = EXCHANGE_INFO.get(exchange.upper(), {})
        return [
            {"date": str(d), "exchange": exchange.upper(), "name": f"{info.get('name', exchange)} Holiday"}
            for d in sorted(holidays)
        ]

    @staticmethod
    def next_trading_day(exchange: str, after: Optional[date] = None) -> Optional[str]:
        info = EXCHANGE_INFO.get(exchange.upper())
        if not info:
            return None
        after = after or date.today()
        check = after
        for _ in range(365):
            check += timedelta(days=1)
            if check.weekday() in WEEKEND:
                continue
            if MarketHoursService._is_holiday(exchange.upper(), check):
                continue
            return str(check)
        return None

    @staticmethod
    def list_holidays_by_year(year: Optional[int] = None) -> dict[str, list[dict]]:
        year = year or date.today().year
        result = {}
        for code in EXCHANGE_INFO:
            holidays = MarketHolidayService.get_holidays(code, year)
            if holidays:
                result[code] = holidays
        return result

    @staticmethod
    def is_holiday_today(exchange: str) -> bool:
        return MarketHoursService._is_holiday(exchange.upper(), date.today())
