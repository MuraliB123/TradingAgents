"""Standalone Sentiment Analyst smoke test focused on Reddit inputs.

Examples:
    python scripts/test_reddit_summary.py --ticker RELIANCE.NS --market india --trade-date 2026-05-30
    python scripts/test_reddit_summary.py --ticker SPY --market us --trade-date 2026-05-30 --show-prompt
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
        reddit_block = _extract_block(system_prompt, "<start_of_reddit>", "<end_of_reddit>")
        news_block = _extract_block(system_prompt, "<start_of_news>", "<end_of_news>")
        stocktwits_block = _extract_block(
            system_prompt,
            "<start_of_stocktwits>",
            "<end_of_stocktwits>",
        )

        content = [
            "# Sentiment Analyst Smoke Test",
            "",
            "This is a local fake-LLM response. It verifies the complete Sentiment Analyst node collected data and injected it into the prompt.",
            "",
            "## Source Blocks Seen By The Agent",
            f"- News block characters: {len(news_block)}",
            f"- StockTwits block characters: {len(stocktwits_block)}",
            f"- Reddit block characters: {len(reddit_block)}",
            "",
            "## Reddit Block",
            reddit_block,
        ]
        if show_prompt:
            content.extend(["", "## Full System Prompt", system_prompt])
        return SimpleNamespace(content="\n".join(content))

    return capture


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the complete Sentiment Analyst node and inspect its Reddit input block."
    )
    parser.add_argument(
        "--ticker",
        default="SPY",
        help="Ticker or query string to search for, e.g. SPY or RELIANCE.NS.",
    )
    parser.add_argument(
        "--market",
        choices=("us", "india"),
        default="us",
        help="Subreddit set to use.",
    )
    parser.add_argument(
        "--trade-date",
        default="2026-05-30",
        help="Trade date in YYYY-MM-DD format.",
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
        from tradingagents.agents.analysts.sentiment_analyst import create_sentiment_analyst
        from tradingagents.dataflows.config import set_config
        from tradingagents.dataflows.reddit import get_subreddits_for_market
        from tradingagents.default_config import DEFAULT_CONFIG
    except ModuleNotFoundError as exc:
        print(
            "Missing project dependency while importing the Sentiment Analyst: "
            f"{exc.name}. Install the project dependencies, then rerun this script.",
            file=sys.stderr,
        )
        return 1

    subreddits = get_subreddits_for_market(args.market)

    print("Reddit summary consumer: Sentiment Analyst")
    print(
        "Downstream consumers: Bull/Bear Researchers and Aggressive/Neutral/"
        "Conservative Risk Debaters read sentiment_report; Trader and "
        "Portfolio Manager receive it indirectly through plans/debates."
    )
    print(f"Ticker: {args.ticker}")
    print(f"Trade date: {args.trade_date}")
    print(f"Market mode: {args.market}")
    print("Subreddits: " + ", ".join(f"r/{sub}" for sub in subreddits))

    config = copy.deepcopy(DEFAULT_CONFIG)
    config["reddit_market"] = args.market
    set_config(config)

    agent = create_sentiment_analyst(_build_capture_llm(show_prompt=args.show_prompt))
    state = {
        "company_of_interest": args.ticker,
        "trade_date": args.trade_date,
        "messages": [],
    }

    print("\n--- Running complete Sentiment Analyst node ---")
    result = agent(state)
    print(result["sentiment_report"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
