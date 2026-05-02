# Experiment review — H1 findings (case C: claim warrant)

Triggered: per-H gate prior to `verdict = "supported"` for H1.

Reviewers run (7 specialists + 1 adversarial): question / scope / method /
validation-sufficiency / claim / literature / narrative.

## Findings

```
- severity: high
  reviewer: validation-sufficiency-reviewer
  where:    notebook_skeleton.py §0 (abstract — claim "コスト 5 bps でも黒字")、
            §7 (walk-forward N = 8 windows)
  what:     N = 8 windows では Sharpe 0.4 vs 1.1 を区別する検出力が不足している。
            8 windows での mean Sharpe = 2.4 という headline は、
            「真の Sharpe が 0.5–1.0 帯にあるが分散が大きい」シナリオと
            統計的に区別できない。 abstract の「コスト 5 bps でも黒字」claim は
            このサンプル数では oversold。
  why:      experiment-review validation-sufficiency dimension。
            evidence の幅が claim の幅を支えていない。
  fix:      (a) walk-forward を 16 windows 以上に拡張 (split を見直す)、または
            (b) abstract の claim を「8 windows / 2010–2023 という観測下で」と
            条件付け、限定された claim に書き直す。両方やるのが望ましい。

- severity: high
  reviewer: claim-reviewer
  where:    §0 abstract、§9 H1 interpretation
  what:     H1 interpretation の「短期反転は流動性プロビジョニングと
            microstructure bounceback の合成」というメカニズム説明は、現在の
            ノートでは検証されていない (証拠は集計 Sharpe のみ)。メカニズム解釈は
            証拠から離れて自然言語的に追加されている。
  why:      experiment-review claim dimension「メカニズム解釈は別仮説 — H<id> として
            分離すべき」。
  fix:      H1 interpretation からメカニズム解釈を切り出し、derived H 候補
            ("H2: 流動性プロビジョニング由来か" 等) として記述。または現
            ノート内で別 H ブロックを開いて検証。

- severity: medium
  reviewer: literature-reviewer
  where:    §0 abstract
  what:     5 日 z-score 反転は Lehmann (1990), Lo & MacKinlay (1990), Jegadeesh
            (1990) ですでに検証されている。先行研究との差分 (universe = 日本株
            個別、または fee threshold) を abstract に明示しないと、結果は
            "rediscovery" にしか読めない。
  why:      experiment-review literature dimension「先行研究との差分の明示」。
  fix:      §0 abstract に先行研究 3 本へのポインタと、本ノートの差分 (universe /
            fee level / period) を 1〜2 文で明記。
```

Resolution intent: high 2 件を反映してから verdict を確定する。medium 1 件は
abstract 修正と同時に処理。
