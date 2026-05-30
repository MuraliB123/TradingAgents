## META (as of 2026-05-30) — Trend, Momentum, Volatility Read

### 1) Market regime: sharp selloff → short-term rebound attempts, but still below key trend gauges
**Price context (from your OHLCV):**
- META has been **in a broad drawdown since late March**, including a very steep gap/flush around **2026-03-26 to 2026-03-31** (close collapsing from the ~547–572 area).
- Since then, price has **attempted to stabilize and rebound** (e.g., climb into April), but it **rolled over again near 2026-04-30/05-01** (large down day), and has been **grinding/mean-reverting in May**.

**Moving averages confirm the longer-term weakness:**
- **close vs 200 SMA (long-term trend)**
  - 200 SMA is still very high vs price:  
    - **200 SMA (2026-05-29): ~665.83** while **Close (2026-05-29): ~632.51**
  - That means META remains **below its long-term trend benchmark**, consistent with a **bearish-to-neutral higher-timeframe regime**.
- **close vs 50 SMA (medium-term trend)**
  - **50 SMA (2026-05-29): ~618.53** while **Close (2026-05-29): ~632.51**
  - So META is **back above the 50 SMA**, which often marks **attempted trend repair** on an intermediate horizon—but it’s not enough to overturn the longer trend still below the 200 SMA.
- **10 EMA (short-term tactical trend)**
  - 10 EMA has been stepping up from about **~610–617** to **~621.53** by 2026-05-29, suggesting **near-term momentum improvement**.
  - However, the 10 EMA is still far below the 50 SMA and far below the 200 SMA → this looks like a **counter-trend rebound** rather than a full trend reversal.

**Indicator set choice rationale (complementary, non-redundant):**
- `close_10_ema` + `close_50_sma` + `close_200_sma` = trend across short/medium/long horizons (no redundancy beyond horizon separation).
- `macd` + `macdh` = momentum + momentum acceleration/deceleration (paired but complementary: direction vs. change-in-strength).
- `rsi` = overbought/oversold + momentum quality.
- `boll_lb` = downside “pressure zone” / oversold reference.
- `atr` = risk sizing / stop distance based on realized volatility.

---

### 2) Momentum: MACD has been deeply negative, but the histogram improving suggests rebound energy returning
**MACD level (direction):**
- By 2026-05-29, `macd` is around **-1.08** (still negative), which typically implies the **broader momentum remains below zero** (i.e., not fully bullish yet).

**MACD histogram (acceleration):**
- `macdh` at 2026-05-29 is about **+3.20** and had been **strongly negative earlier in May** (e.g., around **-8.21 on 2026-05-05**).
- This is a classic “**momentum is turning up**” signature:
  - When histogram moves from deeply negative to positive, it often indicates **selling pressure is fading** and upward impulse is developing.

**Actionable interpretation:**
- Treat the MACD negatives as “**trend not fully repaired**,” but the **positive histogram** as “**tactical rebound is being built**.”
- The most tradable setups usually occur when:
  1) histogram stays positive for multiple sessions, and  
  2) price holds above a near-term mean (often the 10 EMA / or prior breakout levels).

---

### 3) RSI: recovering from weak territory, now in a neutral-to-slightly-bullish band
- RSI around **2026-05-29: ~55.36**.
- Earlier in May, RSI was frequently ~40 or below (e.g., ~39–41), consistent with **oversold/weak momentum**.
- Now RSI is **back above 50**, which often indicates:
  - downside momentum has weakened,
  - and buyers have regained some control.

**Actionable interpretation:**
- RSI near mid-50s is supportive for **grind-up / mean reversion** strategies.
- It also means rallies can still fail if volatility expands and momentum rolls back below 50—so it’s not a “set and forget” bullish trigger.

---

### 4) Bollinger downside structure: price is above the lower band (less immediate “capitulation” risk)
- `boll_lb` on 2026-05-29 is roughly **592.58**, while price is **~632.51**.
- That means META is **not currently sitting near the downside extreme**.
- In practical terms:
  - You’re more in a “**recovering/normalizing**” condition than a “**at-the-bottom, mean-reversion lottery ticket**” condition.

**Actionable interpretation:**
- If price were to drop back toward the **620s → low 600s**, Bollinger lower band proximity would increase reversal odds.
- For now, upside continuation is more about **holding trend supports** than about “escaping oversold.”

---

### 5) Volatility (ATR): volatility is elevated vs late April/early May → widen stops / size down
- ATR around **2026-05-29: ~15.51**.
- ATR has decreased from the peak-ish period in late April/early May (it was ~20+ around 05-01/04-30), but it’s still relatively high.
- What this implies:
  - price can move **~15 points per day (on average true range)**.
  - Tight stops are more likely to be tagged by normal fluctuations.

**Actionable risk guidance:**
- For swing trades, consider stops/invalidations that account for ATR (e.g., **1.0–1.5× ATR** depending on how tight you trade).
- Use ATR expansion as a warning that breakouts may be more volatile and whippy.

---

## Practical trading takeaways (no “certainty,” but clear scenarios)

### Bullish continuation scenario (tactical long bias)
Look for:
- Price **holding above the 50 SMA region (~618–620 area)** (medium support),
- MACD histogram staying **positive** (momentum continuation),
- RSI holding **>50** on pullbacks.

If those persist, META is positioned for **another attempt to push higher**, but it may still face resistance until it can reclaim higher averages closer to the 200 SMA (not indicated as likely in the immediate data window).

### Bearish / failed-recovery scenario
Warning signs:
- MACD histogram turns back down toward/under zero,
- RSI falls back under 50,
- price loses the **10 EMA** and starts trending back toward the 50 SMA.

Given ATR, downside snapbacks could be fast—so “breaks” matter more than intraday noise.

---

## Summary Table (key signals & what they mean)

| Area | Latest Read (approx) | What it suggests | Trader takeaway |
|---|---:|---|---|
| Short-term trend (`close_10_ema`) | ~**621.5** (2026-05-29) | Near-term rebound/uptick attempts | Tactical longs favored **only if** price holds above/near 10 EMA |
| Medium-term trend (`close_50_sma`) | ~**618.5** (2026-05-29) vs close ~632.5 | Price above medium benchmark | Use ~618–620 as a key “trend health” support zone |
| Long-term trend (`close_200_sma`) | ~**665.8** (2026-05-29) vs close ~632.5 | Still below long-term trend (bearish higher timeframe) | Expect rebounds to face overhead resistance; favor shorter-term tactics |
| Momentum direction (`macd`) | ~**-1.08** | Momentum still net-negative | Don’t assume full bullish reversal yet |
| Momentum acceleration (`macdh`) | ~**+3.20** | Selling pressure fading; rebound energy returning | Strongest confirmation if histogram stays positive |
| RSI (`rsi`) | ~**55.4** | Neutral-to-bullish momentum recovery | Bullish bias holds while RSI stays >50 |
| Downside reference (`boll_lb`) | ~**592.6** | Not near oversold extreme | Reversal “lottery” is less immediate; watch supports instead |
| Volatility/risk (`atr`) | ~**15.5** | Elevated daily movement | Widen stops / reduce size; avoid overly tight risk limits |

If you want, tell me your trading horizon (day trade vs swing vs position), and I’ll convert these indicator readings into a concrete entry/stop/invalidations framework for META.