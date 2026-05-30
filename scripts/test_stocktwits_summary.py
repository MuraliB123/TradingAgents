"""Standalone Sentiment Analyst smoke test focused on StockTwits inputs.

Examples:
    python scripts/test_stocktwits_summary.py --ticker AAPL --trade-date 2026-05-30
    python scripts/test_stocktwits_summary.py --ticker TCS.NS --trade-date 2026-05-30 --stocktwits-market india
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _extract_block(text: str, start_tag: str, end_tag: str) -> str:
    match = re.search(
        rf"{re.escape(start_tag)}\n(?P<body>.*?)\n{re.escape(end_tag)}",
        text,
        flags=re.DOTALL,
    )
    return match.group("body").strip() if match else "<block not found>"


def _build_capture_llm(show_prompt: bool = False):
    """Return a local fake LLM that reports what the agent passed to it."""

    def capture(prompt_value):
        messages = prompt_value.to_messages()
        system_prompt = messages[0].content if messages else ""
        news_block = _extract_block(system_prompt, "<start_of_news>", "<end_of_news>")
        stocktwits_block = _extract_block(
            system_prompt,
            "<start_of_stocktwits>",
            "<end_of_stocktwits>",
        )
        reddit_block = _extract_block(system_prompt, "<start_of_reddit>", "<end_of_reddit>")

        content = [
            "# Sentiment Analyst StockTwits Smoke Test",
            "",
            "This is a local fake-LLM response. It verifies the complete Sentiment Analyst node collected data and injected it into the prompt.",
            "",
            "## Source Blocks Seen By The Agent",
            f"- News block characters: {len(news_block)}",
            f"- StockTwits block characters: {len(stocktwits_block)}",
            f"- Reddit block characters: {len(reddit_block)}",
            "",
            "## StockTwits Block",
            stocktwits_block,
        ]
        if show_prompt:
            content.extend(["", "## Full System Prompt", system_prompt])
        return SimpleNamespace(content="\n".join(content))

    return capture


def _safe_print(text: str = "") -> None:
    """Print fetched social text even when the Windows console cannot encode it."""
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the complete Sentiment Analyst node and inspect its StockTwits input block."
    )
    parser.add_argument(
        "--ticker",
        default="AAPL",
        help="Ticker or cashtag symbol to fetch, e.g. AAPL, SPY, or TCS.NS.",
    )
    parser.add_argument(
        "--trade-date",
        default="2026-05-30",
        help="Trade date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--reddit-market",
        choices=("us", "india"),
        default="us",
        help="Reddit market mode used by the Sentiment Analyst while building the full prompt.",
    )
    parser.add_argument(
        "--stocktwits-market",
        "--stocktwist-market",
        choices=("us", "india"),
        default="us",
        help="StockTwits market mode used for symbol lookup, e.g. india maps TCS.NS to TCS.NSE.",
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Also print the full system prompt assembled by the agent.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        from tradingagents.dataflows.stocktwits import (
            fetch_stocktwits_messages,
            normalize_stocktwits_symbol,
        )
    except ModuleNotFoundError as exc:
        print(
            "Missing project dependency while importing the StockTwits fetcher: "
            f"{exc.name}. Install the project dependencies, then rerun this script.",
            file=sys.stderr,
        )
        return 1

    print("StockTwits summary consumer: Sentiment Analyst")
    print(
        "Downstream consumers: Bull/Bear Researchers and Aggressive/Neutral/"
        "Conservative Risk Debaters read sentiment_report; Trader and "
        "Portfolio Manager receive it indirectly through plans/debates."
    )
    print(f"Ticker: {args.ticker}")
    lookup_symbol = normalize_stocktwits_symbol(args.ticker, args.stocktwits_market)
    print(f"StockTwits lookup symbol: {lookup_symbol}")
    print(f"Trade date: {args.trade_date}")
    print(f"Reddit market mode: {args.reddit_market}")
    print(f"StockTwits market mode: {args.stocktwits_market}")

    print("\n--- Direct StockTwits fetcher output ---")
    _safe_print(fetch_stocktwits_messages(args.ticker, limit=30, market=args.stocktwits_market))

    try:
        from tradingagents.agents.analysts.sentiment_analyst import create_sentiment_analyst
        from tradingagents.dataflows.config import set_config
        from tradingagents.default_config import DEFAULT_CONFIG
    except ModuleNotFoundError as exc:
        print(
            "\nSkipping complete Sentiment Analyst node: missing project dependency "
            f"{exc.name}. Install the project dependencies to verify prompt injection.",
            file=sys.stderr,
        )
        return 0

    config = copy.deepcopy(DEFAULT_CONFIG)
    config["reddit_market"] = args.reddit_market
    config["stocktwits_market"] = args.stocktwits_market
    set_config(config)

    agent = create_sentiment_analyst(_build_capture_llm(show_prompt=args.show_prompt))
    state = {
        "company_of_interest": args.ticker,
        "trade_date": args.trade_date,
        "messages": [],
    }

    print("\n--- Running complete Sentiment Analyst node ---")
    result = agent(state)
    _safe_print(result["sentiment_report"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
