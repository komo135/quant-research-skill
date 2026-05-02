# Case I — 旧ノートの synthesis を引き継いで派生 Purpose の新ノートを開く

## 状況

`exp_012_eurusd_meanreversion_universe_sweep.py` (EUR/USD 5min mean-reversion の
網羅検証) で、H1-H4 の 4 ラウンドが回り、いずれも `failure_mode='turnover'` を
共有して emergency-stop (N=5 advisory) にヒットした。`cross_h_synthesis.md` の
Pattern A (binding axis = turnover) として synthesis が完了し、その action として
2 つの派生 Purpose に split することが決まった:

- **P_X (turnover-controlled re-test)**: turnover を 30%/month 以下に制約した上で
  MR が edge を保つかを再検証する。本ノート (`exp_013`) でこれを扱う。
- **P_Y (alternative exit)**: signal-flip 以外の exit (TP/SL、time-stop max-hold) で
  MR を再構成。別ノート (`exp_014`) で扱う予定。

P_X の Purpose は exp_012 の cluster synthesis から派生したが、Purpose 自体としては
独立した falsifiable 仮説 (turnover-cap 制約下で test Sharpe ≥ 0.5) を持ち、
新ノート 1 本として開かれる。

## あなたのタスク

派生 Purpose P_X 用の新ノート `notebook_I_purpose_handoff.py` を、
`hypothesis_cycles.md` の "Across Purposes — next notebook (`exp_<NNN+1>_*.py`)"
規定と `experiment_protocol.md` / `research_design.md` の Purpose ヘッダー規定に
従って書いてください。最低限必要なセル:

1. docstring (ファイル先頭)
2. Purpose ヘッダー (`## Purpose`)
3. Cycle goal — 4 items (Consumer / Decision / Decision rule / Knowledge output)
4. Hypotheses tested セクション (H1 のみ)
5. Conclusion (preliminary)
6. Figure plan
7. `## H1` ブロック (config / abstract / result placeholder / verdict PENDING)

派生 Purpose の handoff として、**exp_012 の synthesis 結果と本 Purpose の
関係 (= なぜこの Purpose が選ばれたか、どの binding axis を引き継いでいるか)
が、後で読む第三者 (= 同チームの別研究者、半年後の自分) に追えるように
残してください**。半年後にこのノートを開いた時に「なぜ turnover を 30%/month
にキャップしたのか、どこで決まったのか」が読み取れない notebook では困ります。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/hypothesis_cycles.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cross_h_synthesis.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cycle_purpose_and_goal.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/experiment_protocol.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`

最終ノートを `notebook_I_purpose_handoff.py` に上書き保存してください。
