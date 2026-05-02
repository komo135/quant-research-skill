# RED meta-leak — 失敗モード集計

ユーザー指摘の症状「`skill v0.5.0`、`pivoted at § 4.0 per finding` のような
メタ情報がノート本文に染み出す」を、3 種別のシナリオ (skill upgrade /
mid-cycle pivot / cross-skill API 仕様変更) で再現させた結果、
**現行 reconciliation 規定では覆えない 3 つの失敗モード (F9〜F11)** が観察された。

## F9 — skill version 番号 / バージョン履歴の本文化

ノート本文 (docstring / Purpose ヘッダー / per-section markdown / verdict セル)
に skill 自体のバージョン番号や upgrade 履歴がそのまま侵入する。

### Case D (notebook_D_legacy_v07.py) からの抜粋

| 場所 | 抜粋 |
|---|---|
| docstring | 「このノートは quant-research skill v0.7.0 当時に書かれたものを v0.8.0 規約にあわせて in-place で upgrade したもの」「v0.8.0 で導入され、本ノートに反映した変更点 (元の v0.7.0 当時のノートには存在しなかった)…」「いずれも v0.8.0 で必須化された項目」 |
| Purpose | 「## Cycle goal — 4 items (added in v0.8.0 upgrade)」「以下 4 項目は v0.7.0 ノートには無く、v0.8.0 規約 (`cycle_purpose_and_goal.md`) にあわせて後付けで追加した」 |
| H1 sub-claim | 「(項目自体は v0.8.0 upgrade で追加。`research_design.md` 準拠。)」 |
| verdict | 「### Cycle stop status (v0.8.0 規約: primary vs emergency stops の分離)」「本欄は v0.8.0 upgrade で追記」 |

問題: 研究ノートの読者は **研究内容を読みたい**、skill のバージョン履歴
ではない。skill v0.7.0 / v0.8.0 / 規約準拠タグはノート本文には現れる必要
が無い。skill upgrade の履歴は git log と project の release notes
(README changelog) で追える。F1 の親戚 (編集履歴の本文化) だが、F1 は
review 由来、F9 は skill version 由来で観点が違う。

### 観察された自然な誘惑

- 「migration 経緯を後で追えるようにしたい」 → docstring に履歴を残す
- 「v0.8.0 で必須化された箇所だと示したい」 → セクションヘッダーに
  `(added in v0.8.0)` を付ける
- 「reference 名を脚注的に残したい」 → 「`cycle_purpose_and_goal.md` に
  あわせて後付けで追加した」のような記述

## F10 — pivot / narrowing 履歴の本文化

ノート途中で Purpose / hypothesis / scope を絞り直したとき、その経緯と
理由を本文セクションとして残してしまう。

### Case E (notebook_E_for_pivot.py) からの抜粋

| 場所 | 抜粋 |
|---|---|
| docstring | 「このノートは Purpose を 5-factor から 2-factor (ROE + OCF margin) に narrow した状態。pivot の根拠は Purpose section 内に明記する。」 |
| Purpose 内新設 | 「### Purpose narrowing — pivot rationale  当初の Purpose は quality factor 5 種…の合成を扱う想定だったが、H1 を走らせる前段階の独立 IC スクリーニングで…と判断した」 |
| 同上 | 「この narrowing は本ノートを開く前の判断 (Stage 1.5 hypothesis generation の段階で確定) であり、本ノートは 2-factor 版の Purpose で H1 から開始する」 |

問題: ノートを開いた読者にとって本ノートの Purpose は「2-factor で 0.5
を達成するか」だけが意味のある claim。Purpose narrowing の経緯
(= 5-factor を試みた → IC が薄かった → narrow した) は **計画レイヤー**
の情報で、`decisions.md` か pivot 元の旧ノート (もしあれば) に
属する。本文に書くと、Purpose ヘッダーが研究文書から日記に近づく。

### 観察された自然な誘惑

- 「半年後の自分が pivot 経緯を忘れる前に書き残したい」 → Purpose 直下に
  「Purpose narrowing — pivot rationale」セクション新設
- 「読者が「なぜ 5 factor じゃないのか」と疑問に思ったら答えを用意したい」
  → 過去判断の背景を本文化
- 「Stage 1.5 で確定した narrowing と分かるよう経緯を書く」 → skill の
  step 名が本文に侵入 (F2 の親戚: F2 は reviewer 用語、F10 は research-stage
  用語)

## F11 — cross-skill API 仕様 / 操作チュートリアルの本文化

別 skill (例: marimo widget) の API 仕様、操作方法、新旧仕様差分などが
研究ノート本文に書き込まれる。

### Case F (notebook_F_widget.py) からの抜粋

| 場所 | 抜粋 |
|---|---|
| §H1 widget markdown | 「**Widget options は `{label: value}` の dict で渡し、widget が返す value は dict のキー (label) ではなくキーに対応する値 (Bloomberg ticker 形式 `XXXX.T`) を保持する。**」 |
| §H1 widget markdown | 「**range_slider は `step` を明示し、単位を markdown で宣言する。** ここでは累積日数 (start = 0 が学習開始日 2010-01-04、stop = 3650 は約 10 年後) を単位とし、`step=30` (= 約 1 か月刻み) で走査する。step がないと連続 int 扱いとなり、月境界以外でスナップしやすい位置で zoom が止まる。」 |
| __generated_with | `0.10.0` への明示的な version bump (これ自体は marimo の自動メタ、本文では無いが上の API 説明と一体で読める) |

問題: これは widget の **使い方** の説明で、研究ノートが伝えるべき
研究内容ではない。読者は研究 claim を読みたいが、widget API の使い方が
途中に挟まる。subagent 自身は「『新仕様』『旧 API』のような表現も本文
markdown には残さず、『what / why』だけを書いた」と自己評価していたが、
実際には **API 仕様の説明そのものが本文化**。

### 観察された自然な誘惑

- 「読者が widget を使うときに迷わないようにしたい」 → widget API の
  spec を本文に書く
- 「step を入れた理由を残しておきたい」 → 旧 API の挙動と差分を本文に書く
- 「`__generated_with` を新版に bump したことを示したい」 → version 番号を
  ファイル全体で揃える

## ユーザー指摘との対応関係

ユーザー例: `skill v0.5.0; pivoted at § 4.0 per finding` がノート abstract に
染み出す。

| ユーザー要素 | RED で再現された側面 |
|---|---|
| `skill v0.5.0` | F9 (skill version 番号の本文化) — Case D で「v0.7.0 → v0.8.0」「v0.8.0 で必須化」 |
| `pivoted at § 4.0` | F10 (pivot 履歴の本文化) — Case E で「Purpose narrowing — pivot rationale」セクション新設 |
| `per finding` | F11 (cross-skill / cross-process 由来情報の本文化) — Case F で widget API 説明、また Case D の「`cycle_purpose_and_goal.md` 準拠」「`research_design.md` 準拠」型のリファレンスポインタ本文化 |

3 軸とも独立に発生し、ユーザー例の単一行 (`Purpose 4 (= 1 ノート =
1 Purpose, skill v0.5.0; pivoted at § 4.0 per finding)`) は **F9 + F10 + F11
が同一行で重畳した結果**。reconciliation 規定で個別に消す必要がある。

## GREEN で打つべき counters

| 失敗モード | counter |
|---|---|
| F9 skill version 番号の本文化 | 「本文に書かない語彙」表に **skill version (skill v0.X.0、v0.X.0 規約、`<reference>.md` 準拠) を skill 由来 attribution 全般として禁止** を追加。skill 改訂履歴は git log と README changelog の役目 |
| F10 pivot 履歴の本文化 | 同表に **pivot / narrowing / 旧 Purpose との対比 (「当初の Purpose は…」「pivot rationale」「narrowed from X to Y」) を禁止** を追加。pivot 経緯は `decisions.md`、または pivot 元の旧ノートの synthesis 行に属す。新ノートは新 Purpose 単独で読める形に |
| F11 cross-skill API 説明の本文化 | 同表に **API 仕様の解説 / widget の使い方 / 新旧 API 対比を禁止** を追加。widget の使い方は marimo / library 自体の docs の役目。研究ノートに書くのは「この widget で何を見るか / 結論にどう繋がるか」だけ |
| 共通 self-test 拡張 | 「書いた段落を、skill / library / process の固有名詞を一切使わずに研究者語彙だけで書き換えられるか?」を 4 番目の self-test 質問として追加 (現行 3 質問の延長) |

`post_review_reconciliation.md` の「本文に書かない語彙」表に行追加 +
self-test に質問追加 + checklist 1 項目で対応可能。新しい reference は
不要。
