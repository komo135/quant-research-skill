# Bug review — H1 findings (case B: pnl-accounting)

Trigger fired: `Test Sharpe (after costs) > 3` AND `state-change: about to set
verdict=supported on H1`.

Reviewers run: leakage / pnl-accounting / validation / statistics / code-correctness / adversarial.

## Findings

```
- severity: medium
  reviewer: pnl-accounting-reviewer
  where:    notebook_skeleton.py §6 (turnover / cost)
  what:     pl.col("pos").diff().abs() を symbol で groupby しないまま flattened
            panel に対して計算しており、symbol 境界 (例: 銘柄 A 末尾 → 銘柄 B 先頭)
            で phantom trade が発生する。コストが overestimate される一方で、
            銘柄ごとに本来計算されるべきポジション切替が境界で潰れている。
  why:      bug_review.md「Cost: position.diff().abs() * fee is only valid when
            position is per-symbol; on a flattened multi-instrument frame it
            generates fake trades at ticker boundaries」に該当。
  fix:      diff() を .over("symbol") に書き換え、§6 で turnover と pnl_net を
            再計算。Fig 2 (累積 PnL net), Fig 3 (コスト感度) を再生成し、
            walk-forward (§7) と headline メトリクスも更新する。

- severity: medium
  reviewer: pnl-accounting-reviewer
  where:    §6
  what:     ポジションが [-1, 1] にクリップされている一方で、複数銘柄 long/short
            の合算 exposure が日次でどれだけ振れているかが計算されていない。
            net 5 bps というコスト想定はポジション規模に依存する。
  why:      bug_review.md「Fee monotonicity」「pnl[t] = position[t-1] * ret[t]」と
            照合すると、銘柄ごと PnL の集約規則が暗黙。
  fix:      §6 の最後に gross exposure 系列 (Σ|pos|) を作り、Fig 2 と並べて
            一日あたり exposure を可視化する追加セルを置く。

- severity: low
  reviewer: statistics-reviewer
  where:    §7
  what:     walk-forward N = 8 windows での mean Sharpe を point estimate のみ
            報告している。N = 8 は分布として薄いので分位点も併記したい。
  why:      bug_review.md「Bootstrap CI must bracket the headline metric」関連の
            metric internal-consistency。
  fix:      §7 の表に median / 25th / 75th を追加し、Fig 4 box plot に headline
            位置の hline を引く。
```

Resolution intent: medium 2 件を直してから robustness battery を再走、low は park。
