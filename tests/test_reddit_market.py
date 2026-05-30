from __future__ import annotations

import copy

import pytest

from tradingagents.dataflows.config import set_config
from tradingagents.dataflows import reddit
from tradingagents.default_config import DEFAULT_CONFIG


def test_get_subreddits_for_supported_markets():
    assert reddit.get_subreddits_for_market("us") == (
        "wallstreetbets",
        "stocks",
        "investing",
    )
    assert reddit.get_subreddits_for_market("INDIA") == (
        "IndianStreetBets",
        "IndiaInvestments",
        "IndiaStockMarket",
    )


def test_get_subreddits_for_invalid_market_raises():
    with pytest.raises(ValueError, match="Unsupported Reddit market"):
        reddit.get_subreddits_for_market("europe")


def test_india_exchange_suffix_uses_base_ticker_for_reddit_search():
    assert reddit._search_query_for_ticker("RELIANCE.NS") == "RELIANCE"
    assert reddit._search_query_for_ticker("TCS.BO") == "TCS"
    assert reddit._search_query_for_ticker("BRK.B") == "BRK.B"


def test_fetch_reddit_posts_uses_configured_market(monkeypatch):
    seen_subreddits = []

    def fake_fetch(ticker, sub, limit, timeout):
        seen_subreddits.append(sub)
        return []

    monkeypatch.setattr(reddit, "_fetch_subreddit", fake_fetch)
    monkeypatch.setattr(reddit.time, "sleep", lambda _: None)

    try:
        config = copy.deepcopy(DEFAULT_CONFIG)
        config["reddit_market"] = "india"
        set_config(config)

        output = reddit.fetch_reddit_posts("RELIANCE.NS")
    finally:
        set_config(copy.deepcopy(DEFAULT_CONFIG))

    assert seen_subreddits == list(reddit.get_subreddits_for_market("india"))
    assert "r/IndianStreetBets" in output
    assert "r/IndiaInvestments" in output
    assert "r/IndiaStockMarket" in output

