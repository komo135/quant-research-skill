# RED research-goal-layer — 失敗モード集計

ユーザー指摘の問い「派生 H は現状放置される、やるとしても仮説が主になり、
**何の為にこの仮説を立証したいのか** が不明になる」を、**設計仮説レイヤーが
skill 構造から欠落している** という根本原因に紐付けて再現させた結果、
2 つの構造的失敗モード (F15 / F16) が観察された。

F12-F14 (= 派生 H 表のノート本文流入、整合不全) とは性質が異なる。F12-F14 は
**規定 A と規定 B が矛盾している** ことから生じる症状で、`hypothesis_cycles.md`
側の表テンプレを退去させれば解消する。F15 / F16 は **規定そのものが存在しない**
ことから生じる症状で、表を退去させても残る。両者は GREEN フェーズで別経路の
counter を要する。

## 抜けているレイヤー — 4 階層モデル

```
[研究目標 Research goal]   project README の Question
      ↓
[設計仮説 Design hypothesis] 「研究目標達成にこういう実験 (= Purpose) が必要そう」
                             という予想 — Purpose 選定根拠と事後検証
      ↓
[Purpose / cycle]          1 ノートの open-ended 問い
      ↓
[Hypothesis / H<id>]        ノート内の falsifiable claim
```

skill が定義しているのは **Purpose レイヤーから下** のみ。研究目標は project
README に静的に置かれるだけで skill の述語にならず、設計仮説レイヤーは存在
しない。Purpose を選ぶときの予想 (= 「Purpose A を解けば研究目標 X に N% 近づく」)
は `decisions.md` のテンプレに欄が無く、Purpose 終了時の事後検証 (= 「Purpose A
の結果から、研究目標との距離はどう変わったか」) も同様に欠落している。

## F15 — 派生 H 単発の根拠が研究目標に紐付かない

H1 → §H2 への派生時、§H2 ブロックを作る根拠は H1 の interpretation セルでの
「次に試したい」の自然な流れ **だけ** で、H2 が **研究目標サブクレームに
どう貢献するか** / **どの設計仮説 (= 「Purpose A を解けば研究目標に近づく」
の中身) を更新するか** は、ノート / `decisions.md` / `hypotheses.md` のいずれ
にも記録されない。

### Case J (`notebook_J_derivation_orphan.py`) からの抜粋

| 場所 | 抜粋 |
|---|---|
| Purpose ヘッダー | 「TOPIX500 universe / 2014–2024 において、quality factor 系シグナルが net 5 bps fee で…WF mean Sharpe ≥ 0.4 を達成するかを検証する」 |
| Cycle goal Consumer | 「自分の次 Purpose (JP equity quality factor を多 factor スタックに組む段階)」 |
| §H1 interpretation | 「ROE のシグナル強度は出ているが…独立軸を加えて turnover を平均化する余地がありそう。後者は…OCF margin を合成軸に加える方向で試せる」 |
| §H2 abstract / interpretation | 「H1 単独より turnover が下がり (45% → 32%)、edge が net で残った」 |
| Purpose-level synthesis | 「TOPIX500 quality factor のうち、ROE 単独は turnover で retire したが、OCF margin との合成で net 5 bps 帯に残る」 |
| 研究目標 | project README に「JP equity universe で live tradeable な quality factor を 1〜2 件特定する」と書かれている (= instruction_J.md 経由の前提) |

問題: H2 の根拠は「H1 で turnover が edge を食い切った、独立軸を加えたい」で
完結している。これは **Purpose 内の問い** (= TOPIX500 quality factor の net 5 bps
収益性) に対する H2 の貢献で、研究目標 (= live tradeable な quality factor を
1〜2 件特定する) への貢献ではない。

たとえば:

- H2 の supported_provisional は「Purpose A の Decision rule YES 条件を満たす」
  ことを意味するが、研究目標が要求している「live tradeable」(= 実際に取引
  できるか、bid-ask spread / market impact / available borrow に乗るか) の
  確認には未踏。Purpose A 単独では研究目標の sub-claim 「quality factor が
  edge を持つ」までしか到達せず、「live tradeable」までは届かない
- H2 を試した判断は H1 の turnover 観察から自然に出たが、もし研究者が「live
  tradeable」を目標として意識していれば、H2 ではなく **liquidity-filtered な
  H2'** (= ADV 上位銘柄に limit した版) を試すという選択肢があり得る
- 研究目標との紐付けが無い限り、派生 H の選び方は **直前の H の数値観察に
  ローカルに駆動** され、研究目標から見て遠回りな経路でも気付けない

### 観察された自然な誘惑

- 「H2 は H1 から自然に派生したので、根拠を別途書くのは冗長」 → 派生根拠は
  interpretation セルの数値観察で十分とする習慣
- 「研究目標は project README に書いてあるので、ノートで再述する必要はない」
  → 研究目標と H2 の紐付けは読者の頭の中で行う (実際は行われない)
- 「設計仮説を文書化するのは overhead」 → Purpose を選ぶ時点で「これを解けば
  研究目標に N% 近づく」を明示する場所が `decisions.md` のテンプレにも無い

`hypothesis_cycles.md` は派生 H の routing (どこに置くか) を扱うが、**派生 H
の根拠が研究目標サブクレームのどれに紐付くか** は規定外。`hypothesis_generation.md`
の Pathway 4 (failure-derived) は H1 → H2 の生成 **メカニズム** を扱うが、
研究目標との紐付けは Pathway 6 (mechanism-driven) に近いものの、Pathway 6 は
「経済 / マイクロストラクチャの mechanism」を指していて研究目標 sub-claim とは
別軸。F15 はこの紐付け規定の不在の症状。

## F16 — Purpose 終了 → 次 Purpose 開始時に研究目標との距離が更新されない

Purpose A が Primary YES で closing した時、研究目標 X への前進度を更新する
場所が `decisions.md` テンプレにない。次に Purpose B を開く根拠は `cross_h_synthesis.md`
Pattern action (= 派生 Purpose 候補の routing) に依存し、**Purpose B が研究目標
への次のステップとして妥当か** は誰も問わない。

### Case K (`notebook_K_purpose_close_no_review.py` + `decisions_fixture.md`) からの抜粋

`decisions_fixture.md` の Purpose A エントリ (現行テンプレ通り):

```markdown
## 2026-04-25 cycle 1 (exp_021_topix_quality_factor) — Purpose: TOPIX500 quality factor の net 5 bps 収益性

- Tested H1: ... Verdict: rejected
- Tested H2 (derived from H1): ... Verdict: supported_provisional
- Purpose-level synthesis: ROE 単独は turnover で retire したが、OCF margin との
  合成で net 5 bps 帯に残る。Decision rule の YES 条件は H2 で達成。
- Derived Purposes for the next notebook:
  - Purpose B (run-now): 3-factor (ROE / OCF margin / accruals quality) 拡張で
    Sharpe を更に伸ばせるか
- Direction rejected: ROE 単独 (turnover で retire)
- Robustness battery status (per H): H1 — N/A、H2 — pending
```

| 場所 | 不在 (= 書かれていない) もの |
|---|---|
| `Purpose-level synthesis` | 研究目標 X (= live tradeable な quality factor を 1〜2 件特定) との距離は更新されていない。Purpose A は YES だが、live tradeable の確認は未踏という前進度の記述が無い |
| `Derived Purposes for the next notebook` | Purpose B (3-factor 拡張) は **Sharpe を更に伸ばせるか** という Purpose 内側の動機で記述されており、研究目標 X への貢献 (= 「live tradeable な quality factor を 1〜2 件特定する」のためになぜ 3-factor が必要か) への紐付けが無い |
| 設計仮説の更新 | Purpose A 着手時に「これを解けば研究目標に N% 近づく」と予想していたか、その予想がどう外れた / 当たったか の振り返りが無い |
| 研究目標 sub-claim の進捗状態 | sub-claim ごとの「Purpose A で確認済み / Purpose B で確認予定 / 未踏」の整理が無い |

新ノート `notebook_K_purpose_close_no_review.py` の Purpose ヘッダー:

| 場所 | 抜粋 |
|---|---|
| `## Purpose` | 「TOPIX500 universe / 2014–2024 において、ROE / OCF margin / accruals quality の 3-factor を rank 平均で合成した quality シグナルが、net 5 bps fee で…WF mean Sharpe ≥ 0.5 を達成するかを検証する」 |
| Cycle goal Consumer | 「自分の次 Purpose (JP equity quality factor を多 factor スタックに組む段階の最終確認)」 |
| Cycle goal Decision | 「多 factor スタック組み込み時の重み比配分を決めるか / 棄却するか」 |

問題: Purpose B 自体は falsifiable な閾値 (Sharpe ≥ 0.5) を持ち、Cycle goal も
4 items 揃っている (= F12-14 / F15 の symptom は無い)。だが **「なぜ研究目標
達成のために 3-factor 拡張が次なのか」** は読み取れない。Purpose A で WF mean
0.41 が出た後、研究目標から見ての次の sub-claim は (a) live tradeability の検証
かもしれないし、(b) 3-factor 拡張で Sharpe を上げるかもしれないし、(c) 別の
universe (TOPIX1500) への横展開かもしれない。研究者は (b) を選んだが、その
判断根拠 = 設計仮説 (= 「研究目標達成には Sharpe を 0.5 以上に上げる必要があ
り、そのためには合成軸を増やすのが最短」) は `decisions.md` にも `notebook` にも
書かれていない。

### 観察された自然な誘惑

- 「Decision rule の YES が出たから次の Purpose に進む、で routing は完結」 →
  研究目標との距離レビューは routing の outside にあるので skip
- 「研究目標は project README に書いてある、変わらないので review 不要」 →
  研究目標 sub-claim ごとの進捗状態を更新する場所が無いことを問題視しない
- 「`cross_h_synthesis.md` の Pattern action が次 Purpose を提案してくれるので
  それに従う」 → Pattern action は Purpose 内側の出力からの派生で、研究目標
  との整合は別問題

`cycle_purpose_and_goal.md` は Cycle goal の 4 items (Consumer / Decision /
Decision rule / Knowledge output) を要求するが、Consumer は「downstream consumer」
として Purpose の **直近** 下流 (= 自分の次 Purpose) になりがちで、**研究目標
との整合チェックが Consumer 自身に丸投げ** される循環参照になる。F16 はこの
循環参照の症状。

## F14 (cross-notebook handoff の本文流入) との独立性

K の fixture は意図的に F14 を踏まないように書かれている — `## Origin` セクション、
exp_021 への前向き参照、`cross_h_synthesis.md` Pattern 名 / 「派生 Purpose」/
「handoff」のような skill プロセス由来語は **新ノート本文に侵入していない**。
それでもなお、F16 (研究目標との距離の不在) が観察される。

つまり F14 を GREEN で完全に潰しても F16 は残る。逆に F16 への counter (= 研究
目標 sub-claim の進捗追跡) を導入しても、F14 (本文への流入) は別途 counter が
要る。両者は **同じ場所 (= 新 Purpose 開始時) で起きる別問題**。

| | F14 | F16 |
|---|---|---|
| 規定 | 既存規定間の整合不全 | 規定そのものの不在 |
| 場所 | 新ノート本文 (docstring / Purpose ヘッダー) | `decisions.md` テンプレ + Purpose ヘッダー |
| 入る情報 | 旧ノート synthesis / Pattern 名 / handoff 経緯 | 何も入らない (= 抜け落ち) |
| 解消経路 | 新ノート本文に書かない (退去) | 新しい記録欄を導入 (追加) |

## ユーザー指摘との対応関係

ユーザー指摘: 「派生 H は現状放置される、やるとしても仮説が主になり、
**何の為にこの仮説を立証したいのか** が不明になる」

| ユーザー要素 | RED で再現された側面 |
|---|---|
| 派生 H が放置される | F15 — 派生 H の根拠が `decisions.md` / `hypotheses.md` のどこにも書かれず、interpretation セルに溶け込んで消える |
| 仮説が主になる | F15 + F16 — 上位レイヤー (研究目標 / 設計仮説) が skill の述語にならないので、ノート内では Hypothesis レイヤーが事実上の主役になる |
| 何の為にこの仮説を立証したいのか不明 | F15 (派生 H 単発の根拠不在) + F16 (Purpose 終了時の研究目標前進度の不在) |

3 要素は **同じ欠落の 3 側面**。skill が「研究目標 → 設計仮説 → Purpose → H」の
4 階層のうち上 2 つを述語化していないことから生じる。

## F12-F14 を GREEN で潰しても F15 / F16 は残る

これは GREEN フェーズで重要な区別:

- F12-F14 の counter (例えば案 A: 派生 H 表をノート本文から退去させ
  `hypotheses.md` に集約) を実施しても、`hypotheses.md` 側に **研究目標
  サブクレームへの紐付け列** が無ければ F15 は解消しない
- F14 の counter (= 旧ノート synthesis を新ノート本文に書かせない) を実施
  しても、`decisions.md` 側に **研究目標との距離更新エントリ** が無ければ F16 は
  解消しない

つまり F15 / F16 への counter は F12-F14 の counter とは別経路で必要で、
具体的には:

- `decisions.md` テンプレに「研究目標 sub-claim の進捗更新」セクションを追加
- `hypotheses.md` のスキーマに「target_sub_claim_id」「design_hypothesis_id」列を
  追加
- `cycle_purpose_and_goal.md` の Cycle goal 4 items に **5 項目目** (= 研究目標
  サブクレームへの紐付け) を追加するか、Consumer の定義に「研究目標 sub-claim
  ごとの進捗を更新する役割」を組み込む
- 新規 reference `references/research_goal_layer.md` (もしくは既存ファイルへの
  セクション追加) で 4 階層モデルを明示

詳細は GREEN フェーズで設計する。
