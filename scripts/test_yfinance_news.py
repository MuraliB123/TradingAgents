"""Standalone Yahoo Finance news fetch smoke test.

Examples:
    python scripts/test_yfinance_news.py --ticker AAPL --start-date 2026-05-20 --end-date 2026-05-30
    python scripts/test_yfinance_news.py --ticker TCS.NS --global-news --curr-date 2026-05-30
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _default_dates() -> tuple[str, str]:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=10)
    return start.isoformat(), end.isoformat()


def build_parser() -> argparse.ArgumentParser:
    default_start, default_end = _default_dates()
    parser = argparse.ArgumentParser(
        description="Fetch and print Yahoo Finance stock news output."
    )
    parser.add_argument(
        "--ticker",
        default="AAPL",
        help="Ticker symbol to test, e.g. AAPL or TCS.NS.",
    )
    parser.add_argument(
        "--start-date",
        default=default_start,
        help=f"Start date in YYYY-MM-DD format (default: {default_start}).",
    )
    parser.add_argument(
        "--end-date",
        default=default_end,
        help=f"End date in YYYY-MM-DD format (default: {default_end}).",
    )
    parser.add_argument(
        "--global-news",
        action="store_true",
        help="Also fetch global market news via Yahoo Finance search.",
    )
    parser.add_argument(
        "--curr-date",
        default=default_end,
        help=f"Current date for global news in YYYY-MM-DD format (default: {default_end}).",
    )
    parser.add_argument(
        "--look-back-days",
        type=int,
        default=None,
        help="Override config lookback days for global news.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Override max article count for global news.",
    )
    return parser


def _validate_date(label: str, value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        print(f"Invalid {label}: {value}. Expected YYYY-MM-DD.", file=sys.stderr)
        return False


def _safe_print(text: str = "") -> None:
    """Print text even when terminal encoding cannot render some characters."""
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding))


def main() -> int:
    args = build_parser().parse_args()

    if not _validate_date("start-date", args.start_date):
        return 2
    if not _validate_date("end-date", args.end_date):
        return 2
    if not _validate_date("curr-date", args.curr_date):
        return 2

    try:
        from tradingagents.dataflows.yfinance_news import (
            get_global_news_yfinance,
            get_news_yfinance,
        )
    except ModuleNotFoundError as exc:
        print(
            "Missing project dependency while importing yfinance news modules: "
            f"{exc.name}. Install dependencies, then rerun this script.",
            file=sys.stderr,
        )
        return 1

    print("Yahoo Finance news smoke test")
    print(f"Ticker: {args.ticker}")
    print(f"Date range: {args.start_date} -> {args.end_date}")
    print("\n--- Ticker news output ---")
    _safe_print(get_news_yfinance(args.ticker, args.start_date, args.end_date))

    if args.global_news:
        print("\n--- Global market news output ---")
        _safe_print(
            get_global_news_yfinance(
                curr_date=args.curr_date,
                look_back_days=args.look_back_days,
                limit=args.limit,
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
