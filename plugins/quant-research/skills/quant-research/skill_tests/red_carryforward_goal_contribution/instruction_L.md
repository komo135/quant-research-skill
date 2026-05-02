# Instruction L — carry-forward derived H, mid-range parent result

You are mid-cycle on a quant-research notebook (`exp_034_eurpair_rsi_mr.py`).

**Purpose** (already declared in the notebook header):

> Does RSI-based intraday mean-reversion produce a tradeable edge on
> EUR-pair intraday at realistic transaction costs?

**Cycle goal** (already pre-committed in the notebook header):

- **Consumer**: my next Purpose — the lower-frequency variant scoping
  (whether to derive a daily-bar RSI Purpose or close the lineage).
- **Decision the consumer is blocked on**: whether to commit a
  2-engineer-week production build of an EUR-pair intraday RSI MR
  strategy.
- **Decision rule** (committed before the cycle ran):
  - **YES** (all conjuncts must hold):
    - (a) test PSR ≥ 0.95 net of 1 bp/side
    - (b) walk-forward positive-rate ≥ 60 % on **≥ 3 EUR pairs**
    - (c) no Pattern A binding axis from cross-H synthesis
  - **NO_1**: bootstrap CI of test PSR straddles 0 on val AND test
  - **NO_2**: ≥ 2 H rejected with shared `failure_mode='fee_model'`
    AND break-even fee < 1 bp/side
  - **KICK-UP**: `bug_review` surfaces unresolvable upstream
    contamination of FX tick data
- **Knowledge output**: per-H rows in `results.parquet` covering the
  three YES conjuncts, plus a Purpose-level synthesis paragraph naming
  Pattern (A-E), plus the headline cumulative-PnL figure with
  baselines.
- **Target sub-claim id**: G2.1 (`EUR-pair intraday RSI MR yields net
  edge ≥ Sharpe 0.5 after costs`).

**H1 already tested in this notebook**:

- Falsifiable statement: "RSI(14) ≤ 30 entry × signal-flip exit on
  **EUR/USD only**, train 2018–2022 / val 2023 / test 2024, fee 1
  bp/side, embargo 1 d, achieves test PSR ≥ 0.95."
- Result observed:
  - test PSR = **0.74**, bootstrap 95 % CI = **(0.41, 1.07)**
  - walk-forward mean Sharpe = 0.42, walk-forward positive-rate = 0.55
  - Tested on 1 instrument (EUR/USD)
  - No fee-model failure mode (break-even fee = 1.6 bp/side, above
    the NO_2 threshold of 1 bp)
- Verdict: **rejected** (point estimate below YES (a) threshold of
  0.95). NO_1 does not fire (CI does not straddle 0). NO_2 does not
  fire (only 1 H so far; break-even fee above 1 bp). KICK-UP does not
  fire.

**The user (researcher) tells you, in chat**:

> "H1 was rejected — PSR 0.74 not 0.95. I want to try H2 = same setup
> but RSI(7) ≤ 25 instead of RSI(14) ≤ 30. Same EUR/USD, same exit,
> same fee. Pathway 4 (failure-derived from H1's threshold being
> conservative). Same Purpose, run-now. Apply `hypothesis_cycles.md`
> and tell me where H2 goes, what row to add to `hypotheses.md`, and
> what the §H2 block in the notebook should open with."

## Your task

Apply the `quant-research` skill (especially `hypothesis_cycles.md`
routing rule + `hypotheses.md` schema + the per-H block opening
requirement from `SKILL.md` Step 2) to the situation above. Output:

1. **Routing decision**: same notebook vs. new notebook; run-now vs.
   next-session vs. drop.
2. **`hypotheses.md` row** to add (full row in the schema).
3. **§H2 block opening** in the notebook (falsifiable statement,
   acceptance / rejection thresholds, per-H headline figure plan).
4. Anything else the skill requires you to do at carry-forward time.

Do not run any code. This is a routing / bookkeeping task.

Be specific. Quote the skill text you are following where relevant.
