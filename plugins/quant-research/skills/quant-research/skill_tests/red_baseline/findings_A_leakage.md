# Bug review — H1 findings (case A: leakage)

Trigger fired: `Test Sharpe (after costs) > 3` AND `state-change: about to set verdict=supported on H1`.

Reviewers run: leakage / pnl-accounting / validation / statistics / code-correctness / adversarial.

## Findings

```
- severity: high
  reviewer: leakage-reviewer
  where:    notebook_skeleton.py §5 (cross-sectional standardization)
  what:     signal_h1 はパネル全体の mean / std で標準化されており、
            train/val/test の境界を跨いだ未来情報がシグナル値に混入している。
  why:      bug_review.md「Whole-period normalization, target encoding,
            scaler-fit-on-all-data」に該当。test set の moments が train 段階の
            シグナル値を変える look-ahead leak。
  fix:      symbol 横断の標準化を、各日付内 (cross-sectional) の rank/standardize、
            または expanding-window で train データのみから fit する形に置換し、
            §6〜§8 を再計算してから verdict を判定する。

- severity: low
  reviewer: code-correctness-reviewer
  where:    §6
  what:     pl.col("ret_fwd") を pct_change().shift(-1) で作っているが、shift(-1)
            は target 側の合法 shift。記述として合法であることをコメントで明示
            することを推奨。
  why:      bug_review.md「`shift(-k)` on signals or features (target-only
            `shift(-k)` is OK)」を読者が即時に判定できると安全。
  fix:      §6 の ret_fwd 行に「target-side leakage では無い: t→t+1 の forward
            return」とコメント。
```

Resolution intent: high finding を反映してから robustness battery を再走 → verdict 確定。
