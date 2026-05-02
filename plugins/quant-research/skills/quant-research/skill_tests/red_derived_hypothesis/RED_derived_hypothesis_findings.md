# RED derived-hypothesis — 失敗モード集計

ユーザー指摘の問い「実験を通して新たに生まれた仮説の扱いがどうなるのか」を、
派生 H が発生する 3 つの典型シナリオ (G: run-now の昇格 / H: 多ラウンド表累積 /
I: 新 Purpose handoff) で再現させた結果、**現行 `hypothesis_cycles.md` を
文字通り守って書くと必ず壊れる 3 つの失敗モード (F12〜F14)** が観察された。

3 ケースとも「subagent が誤動作した」のではなく「**現行 skill の規定に
忠実に従った帰結**」として失敗が出る。これが本 RED の証拠力。

## 中心的緊張 — skill 内部の整合不全 (carve-out なし)

| 規定 | 場所 | 言っていること |
|---|---|---|
| (A) 「H ラウンド末尾に `### Derived hypotheses` 表を書け」 | `hypothesis_cycles.md` L120-128 | run-now / next-session / drop 列付きの表をテンプレ化 |
| (B) 「状態語 `run-now` / `next-session` / `parked` / `follow-up` を本文 markdown / コードに残してはいけない」 | `post_review_reconciliation.md` L62-66 (F5 counter の禁止語彙表) | 状態語は文字列レベルで明示的に列挙されて禁止 |

(A) のテンプレ表は (B) の禁止語彙表が列挙する文字列を **そのまま** 列ヘッダー
(`Run-now / next-session / drop`) に含み、行のセルにも `run-now` / `next-session`
を書く。(A) と (B) の間に carve-out (= 表は例外的に許可) は存在しない —
`post_review_reconciliation.md` 内に「ただし `### Derived hypotheses` 表は除く」
という但し書きは無く、`hypothesis_cycles.md` 側にも「この表は本文ではなく
audit/planning レイヤー」と区別する記述は無い。subagent が両規定に律儀に
従うと、A を守って表を置いた瞬間に B を文字列単位で破る。

F12〜F14 はこの整合不全が異なる経路で発症した症状で、表自体をノート本文から
退去させれば F12 / F13 は構造的に消える (案 A、後段で詳述)。

## F12 — run-now 派生 H の昇格時、`### Derived hypotheses` 表行のライフサイクルが無規定

派生 H が `same notebook / run-now` 行から次の `## H<id>` ブロックに昇格
された後、元の表行をどう扱うかが `hypothesis_cycles.md` に書かれていない。
表行を残す / 消す / 「昇格済み」マーキングする — どれが正解か skill 側に
規定が無く、subagent の挙動はラウンドごとに揺れる。

### Case G (`notebook_G_promotion.py`) からの抜粋

| 場所 | 抜粋 |
|---|---|
| §H1 末尾 表 | `H2: Bollinger(20, 2.0σ) lower-touch entry × signal-flip exit、test Sharpe ≥ 0.5  \| same notebook \| run-now      \| 同 Purpose、別レンズで MR 再検証 (alternative formulation)` |
| §H2 ブロック (= 昇格後) | `## H2 — Bollinger(20, 2.0σ) lower-touch entry × signal-flip exit` 以下、abstract / config / result placeholder / verdict PENDING |

問題: 同一の派生 H が **2 箇所に同時存在** する。読者は §H1 末尾の表行を
「これから着手する未消化の派生 H」と読み、しかし下にスクロールすると同じ
ものが既に §H2 として走り始めている。ノート mental model が破綻する。

### 観察された自然な誘惑

- 「run-now で同 notebook なら、表に書いた予告を実装したのが下の §H<id>
  なので、両方残しておいた方が link 関係が読める」 → 二重登録
- 「表行を消すのは履歴を捨てる感じがして抵抗がある」 → 残置を選択
- 「`(promoted to §H2)` のような注記を表行に追記」 → F2/F9 親戚 (skill
  プロセス用語の本文化) として再発
- 取り消し線で旧表行を残す → F4 (旧値 audit メモ残存) と同形

`hypothesis_cycles.md` は「run-readiness は routing には影響しない、Purpose
継続性のみが routing を決める」と明記しているのに、**同 Purpose で run-now
昇格した時の表行の扱い** だけ穴が開いている。F12 はこの穴の症状。

## F13 — 多ラウンドで `### Derived hypotheses` 表が累積、消化済み / 生きている / 別ラウンドで吸収済みが判別不能

H1 / H2 / H3 と複数ラウンドが進むと、各 H 末尾に同形式の `### Derived
hypotheses` 表が並ぶ。同 Purpose 継続中、過去ラウンドの表行のうち
何が消化されたか / 何がまだ生きているか / 何が後ラウンドで吸収済みかを、
ノート単独で読み取る方法が無い。

### Case H (`notebook_H_table_carryover.py`) からの抜粋

| 場所 | 抜粋 (一部省略) |
|---|---|
| §H1 末尾 表 | H2 (run-now) / H4 (next-session) / H5 (next-session) / earnings revision (drop) |
| §H2 末尾 表 | H3 (run-now) / H6 (next-session) / H7 (next-session) |
| §H3 末尾 表 | H8 (next-session) / H9 (new notebook) |

問題:

- §H1 末尾の H2 行 は §H2 ブロックで消化済み (F12 と同じ二重登録)
- §H1 末尾の H4 / H5 行 はまだ生きている。だが §H2 末尾には H4/H5 の
  status update が無い (= 過去ラウンドの表に書いた未消化行を、後のラウンドで
  追跡更新する規定が存在しない)
- §H2 末尾の H7 (= 重み比 sweep) は §H3 (regime conditional) に吸収された
  可能性があるが、ノート上では別行として並列に残る
- 結果として、ノートが「永久未消化 TODO ボード」に変質する。F5 (タスク
  メモ本文化) の **同 Purpose 内での累積版**。F5 は単発のタスクメモ漏れだが、
  F13 はラウンド数が増えるほど指数的に悪化する構造的問題

### 観察された自然な誘惑

- 「ラウンドごとの表は当該ラウンド時点のスナップショットなので、後で
  上書きせずに歴史として残す」 → 歴史本文化 (F1 親戚)
- 「未消化行は最新ラウンドの表にだけ転記する」 → 当初の skill 規定
  (= 各 H 末尾に表) と矛盾
- next-session 行に「(updated: still pending @ H3)」のような注記 → F2/F9
  親戚 (skill プロセス用語の本文化)

`hypothesis_cycles.md` は「end of each H round」に表を書けと言うが、
**ラウンド間で表行をどう統合 / 退避 / archive するか** が無規定。F13 は
この統合規定の不在の症状。

## F14 — 新 Purpose handoff 時、旧ノート synthesis が新ノート Purpose ヘッダーに本文化

`cross_h_synthesis.md` の Pattern A〜E が出て新 Purpose に split された場合、
新ノートを開く際に **旧ノートの synthesis 結果と新 Purpose の派生関係** を
新ノート本文 (docstring / Purpose ヘッダー / Cycle goal) に残してしまう。
F10 (mid-cycle pivot 履歴の本文化) の **異なるノート間版**。

### Case I (`notebook_I_purpose_handoff.py`) からの抜粋

| 場所 | 抜粋 |
|---|---|
| docstring | 「このノートは exp_012 (EUR/USD 5min mean-reversion の網羅検証) で H1-H4 が `failure_mode='turnover'` を共有して emergency-stop (N=5 advisory) にヒットし、cross_h_synthesis.md の Pattern A (binding axis = turnover) が出た結果として開かれた、派生 Purpose のうちの 1 本」 |
| `## Origin (handoff from exp_012)` | 「本ノートは exp_012 の Purpose-level synthesis (Pattern A: `failure_mode='turnover'` が H1-H4 全件で共通) から派生した 2 つの候補 Purpose のうち、P_X (turnover-controlled re-test) を扱う。もう一方の派生 Purpose P_Y (signal-flip の代わりに TP/SL exit) は exp_014 で別途開く予定」 |
| `## Purpose` | 「exp_012 で binding axis として特定された turnover を 30%/month 以下に制約 (= 強い一次制約) した上で…」 |
| `### H1 abstract` | 「exp_012 で binding axis と認定された turnover を 30%/month に制約した上で…閾値は exp_012 の H1 と同じ (= synthesis を承けて変更しない)」 |

問題: 本ノートを単独で読んだ第三者は、「turnover を 30%/month に cap した
RSI MR が EUR/USD で edge を持つか」という研究内容より先に、**exp_012 cluster の
synthesis 経緯と Pattern A の認定** という skill プロセス由来のメタ情報を
読まされる。F10 と何が違うか:

- **F10**: 同じノート内で Purpose を狭く絞った (5-factor → 2-factor) 経緯が
  Purpose 直下のセクションとして本文化
- **F14**: 異なるノート間で派生 Purpose の handoff が発生し、新ノートの
  Purpose ヘッダー / docstring / `## Origin` セクションに旧ノートの synthesis が
  本文化

両者とも「過去のメタ判断が新研究文脈に染み出す」点で同じだが、**経路が違う**:
F10 は単一ノート内、F14 は cross-notebook。F10 の counter (「pivot rationale
を本文に書かない」) だけでは F14 を覆えない — 新ノートに対しては「pivot」
ですらなく「派生 Purpose の handoff」と認識されているので、F10 の語彙
ブロックリストの対象外として通過する。

### 観察された自然な誘惑

- 「半年後に自分が新ノートを開いた時、なぜこの Purpose / なぜこの閾値
  なのかが分からなくなる前に書き残したい」 → docstring / Purpose に handoff
  経緯
- 「`cross_h_synthesis.md` の Pattern A 由来であることを provenance として
  残したい」 → skill プロセス用語が新ノート本文に侵入 (F2/F9 の cross-notebook
  版)
- 「P_X / P_Y の役割分担を明示したい」 → 兄弟ノート (exp_014) への前方参照
  が本文化

## ユーザー指摘との対応関係

ユーザー問い: 「実験を通して新たに生まれた仮説の扱いがどうなるのか」

| 派生 H 発生シナリオ | RED で再現された失敗 |
|---|---|
| H ラウンド末尾で run-now 派生 H が出る | F12 (表行ライフサイクル無規定) |
| 同 Purpose で複数ラウンド回す | F13 (多ラウンド表累積で TODO ボード化) |
| Pattern A〜E から新 Purpose に split | F14 (cross-notebook handoff で旧 synthesis が新ノート本文化) |

3 つは独立に発生する。F12 が単発で出ることもあれば (Case G)、F12 と F13 が
同時に出ることもあれば (Case H)、F12/F13 と無関係に F14 だけが出ることも
ある (Case I)。GREEN ではそれぞれを独立に counter する必要がある。

## 既往 F1〜F11 との境界

新規性の証拠として、既往の失敗モードと **どこが違うか** を明示する:

| 既往 | F12 | F13 | F14 |
|---|---|---|---|
| F1 (編集履歴本文化) | 表行残存は履歴ではなく **二重登録**。経路が違う | 同左 | 旧 synthesis の handoff は履歴ではなく **前提共有** |
| F2 (レビュー用語本文化) | reviewer 用語は出ない | 同左 | `cross_h_synthesis.md` Pattern A の語が侵入する点で近いが、reviewer dimension 由来ではない |
| F4 (旧値 audit) | 数値ではなく **行** が残る | 同左 | — |
| F5 (タスクメモ本文化) | F5 は単発、F12 は **昇格時の二重登録** | F13 は F5 の **多ラウンド累積構造** で、ラウンド数とともに指数的悪化 | — |
| F8 (レビュー由来セルの位置不統一) | レビュー由来ではなく **派生 H 由来** | 同左 | — |
| F9 (skill version の本文化) | — | — | バージョン番号ではなく **synthesis 結果** が侵入 |
| F10 (pivot 履歴本文化) | — | — | F10 は同ノート内、F14 は **cross-notebook handoff** |
| F11 (cross-skill API 仕様) | — | — | API ではなく **synthesis 結論** だが、`cross_h_synthesis.md` Pattern 名の侵入は F11 の派生 |

F12 / F13 は F5 の系譜だが構造が違う (単発 vs 多ラウンド累積)。F14 は F10 の
系譜だが経路が違う (同ノート vs cross-notebook)。どれも既往 counter の単純
拡張では覆えない。

## GREEN で打つべき counters (叩き台 — GREEN phase で確定)

| 失敗モード | counter (案) |
|---|---|
| F12 表行ライフサイクル無規定 | (案 A) `### Derived hypotheses` 表テンプレ自体を `hypothesis_cycles.md` から削除し、行き先を `hypotheses.md` (planning artifact) に統一する。同 Purpose run-now 昇格後はノート本文に表行が残らない。(案 B) 表は本文に残すが「昇格済み行は次ラウンド開始時に削除」「next-session/drop 行は最新ラウンドの表に **のみ** 集約、過去ラウンドの表からは削除」と統合規定を入れる。 |
| F13 多ラウンド表累積 | F12 案 A なら自動解消。案 B を取る場合、「ラウンド N の表は最新 (= ラウンド N の時点) のスナップショットとして上書き、過去ラウンドの表は archive」が必要。 |
| F14 cross-notebook handoff | 「派生 Purpose の handoff 経緯 (旧ノート ID / 旧 Purpose synthesis / Pattern 種別 / 引き継ぐ binding axis) は **新ノート本文に書かない**。これは `decisions.md` の cross-Purpose entry と `hypotheses.md` の H provenance 行 (`parent_hypothesis_id` / `pathway=4` failure-derived) に格納する。新ノートは新 Purpose 単独で読める形に。」を `post_review_reconciliation.md` の「本文に書かない語彙」表に追加 — または `cross_h_synthesis.md` 側に「synthesis 後の派生 Purpose を新ノートに開くときの handoff ルール」セクションを新設。 |

ユーザーの過去フィードバック (`feedback_notebook_meta_leak.md` —
skill version / pivot 履歴のノート漏れを問題視) と整合的なのは **案 A**
(表をノート本文から退去させる) で、F12 / F13 が同時に解消する。GREEN
phase の議論はこの方向を起点にして、Pattern A〜E から派生 Purpose に
split された時の cross-notebook handoff (F14) の counter をどこに置くかを
決める。

`hypothesis_cycles.md` の「routing rule」セクション + `hypotheses.md` の
スキーマ拡張 + `post_review_reconciliation.md` の本文禁止語彙の 3 段で
実装可能。新しい reference は不要。
