# Parent H1 fixture (for RED on derived-hypothesis depth)

This fixture deliberately gives the researcher *only what is normally
present at the moment a derived H is being proposed in a real session*:
headline numbers, the `verdict`, the `failure_mode` label, and one
short observation cell. **It does NOT pre-compute a mechanism-level
post-mortem.** The data and trade log are available; running a
post-mortem would be the researcher's own choice.

The RED question is: under the current skill, does the researcher do a
mechanism-level post-mortem *before* deriving H's, or do they jump
straight to derivation from the headline + failure_mode label?

## Setup

- **Notebook (Purpose):** "Mean-reversion at H1 frequency on EUR/USD generates
  risk-adjusted edge net of cost on 2018-2024 data."
- **H1 (parent):** "RSI(14)≤30 entry × signal-flip exit on EUR/USD H1 beats
  B&H on test Sharpe by ≥ 0.5 with fee 1 bp/side."
  - Acceptance: test Sharpe ≥ 0.5 AND walk-forward positive-rate ≥ 0.6 at
    fee 1 bp/side.
  - Rejection: test Sharpe < 0.3 OR break-even fee < 0.5 bp/side.

## What the notebook recorded for H1

### Headline numbers (the H1 result table)

| Quantity | Value |
|---|---|
| Test Sharpe (gross) | 1.42 |
| Test Sharpe (net, 1 bp/side) | 0.32 |
| Walk-forward positive-rate (1 bp/side) | 0.55 (12 of 22 windows) |
| Break-even fee | 0.42 bp/side |
| Bootstrap 95 % CI on net Sharpe | [-0.18, 0.74] |
| Number of trades | 1840 |

### H1's observation cell (verbatim, what the researcher wrote at H1 close)

> Net Sharpe lands at 0.32, below the 0.5 acceptance floor and at the
> rejection floor. Break-even fee is 0.42 bp/side, well under the
> 1 bp/side fee assumption. The strategy does not survive deployment-
> grade cost. **failure_mode = `fee_model`**.

### Verdict written into `hypotheses.md`

`verdict = rejected`, `failure_mode = fee_model`.

That is the entirety of the notebook's H1 record at the moment a
derived H is being proposed. No regime breakdown, no holding-time
analysis, no session decomposition, no cross-asset / external-proxy
correlations have been computed; the researcher *could* compute them
but has not.

## What is available if the researcher chooses to dig further

The following artifacts are accessible (you do not need to inspect
them; they are listed here to indicate that a deeper post-mortem is
*possible*, not that one has been done):

- `pnl_per_trade.csv` — per-trade gross/net PnL, entry timestamp, exit
  timestamp, holding time, entry RSI, exit reason.
- `trades_with_features.parquet` — every trade joined with concurrent
  realized vol, VIX (lagged), session-of-day, EUR/USD spot return.
- `monthly_pnl.csv` — H1 monthly PnL series (suitable for joining
  against external return streams: CTA index, long-vol benchmarks,
  EUR/USD monthly return).
- `analyze_trades(...)` — helper to slice the trade log by any
  feature.

## Your situation

You are the researcher. H1 was just verdicted rejected with
`failure_mode = fee_model`. You have to decide what comes next. The
notebook's Purpose statement is unchanged. Per the skill, you may
generate up to three derived hypotheses to test next.
