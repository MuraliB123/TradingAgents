"""Best-effort per-run logging of full tool response text.

Several dataflow fetchers (StockTwits, Reddit, yfinance news, technical
indicators) return plaintext blocks that are injected into agent prompts.
This module appends those full responses to a per-run artifact file so a
completed analysis run can be inspected after the fact.

Design constraints:
  * Best-effort only — a logging failure must never break response
    generation. Every public entry point swallows its own errors.
  * Opt-in via config — when ``tool_response_log_dir`` is not configured,
    logging is silently skipped.
  * Append-only — entries are delimited so the file stays greppable.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Any, Mapping, Optional

logger = logging.getLogger(__name__)

_LOG_FILENAME = "tool_responses.log"
_START_DELIMITER = "===== TOOL RESPONSE START ====="
_END_DELIMITER = "===== TOOL RESPONSE END ====="


def _resolve_log_dir() -> Optional[str]:
    """Return the configured per-run log directory, or ``None`` if disabled."""
    try:
        from tradingagents.dataflows.config import get_config

        config = get_config()
        enabled = config.get("tool_response_logging_enabled", True)
        if not enabled:
            return None
        log_dir = config.get("tool_response_log_dir")
    except Exception:  # pragma: no cover - config import/access failure
        return None
    if not log_dir:
        return None
    return str(log_dir)


def log_tool_response(
    source: str,
    response: str,
    *,
    ticker: Optional[str] = None,
    metadata: Optional[Mapping[str, Any]] = None,
) -> None:
    """Append a full tool ``response`` to the per-run log file.

    Args:
        source: Logical source name (e.g. ``"stocktwits"``, ``"reddit"``,
            ``"yfinance_news"``, ``"technical_indicators"``).
        response: Full response text to persist verbatim.
        ticker: Optional ticker symbol for the request.
        metadata: Optional JSON-serializable metadata (market, date range,
            indicator, vendor, etc.).

    Never raises: any failure is logged at debug level and swallowed.
    """
    log_dir = _resolve_log_dir()
    if not log_dir:
        return

    try:
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, _LOG_FILENAME)

        try:
            metadata_str = json.dumps(metadata or {}, default=str, sort_keys=True)
        except (TypeError, ValueError):
            metadata_str = str(metadata or {})

        lines = [
            _START_DELIMITER,
            f"timestamp: {datetime.now().astimezone().isoformat()}",
            f"source: {source}",
            f"ticker: {ticker if ticker is not None else '-'}",
            f"metadata: {metadata_str}",
            "",
            response if response is not None else "",
            _END_DELIMITER,
            "",
        ]

        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as exc:  # pragma: no cover - defensive best-effort guard
        logger.debug("Failed to log tool response for %s: %s", source, exc)
