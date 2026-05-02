# RED phase — 失敗モード集計

3 ケース (A: leakage / B: pnl-accounting / C: claim-warrant) を現行 skill のみで
回したときに、ノートに発生する状態の悪化パターンを観察した。ユーザーが指摘した
2 症状

- 「当初デザインしていた構造とずれる」
- 「セル追加が『指摘されたから』になり、何を目的に何を確認するか読み取れない」

は、3 ケースとも別々の経路から再現した。以下、抽出した 8 個の失敗モード
(F1〜F8)。GREEN phase ではここに直接対応するルールを書く。

## F1. 編集履歴が本文化される

レビュー反映が本文 (markdown セル) の中に編集履歴として書き込まれてしまう。

| ケース | 抜粋 |
|---|---|
| A §3 | 「bug_review の high finding (§5 の whole-period 標準化が look-ahead leak) を反映し、§5 を per-date cross-sectional 標準化に置換 → §6〜§8 を再計算」 |
| B §3 | 「(§6 の turnover bug 修正後の再計算値)」 |
| B §0 | `> NOTE — post bug_review (case B: pnl-accounting): §6 の turnover を symbol 境界 phantom trade なしで再計算 (medium #1)…` |
| C §0 | 「コスト 5 bps でも黒字」は universe / period / window 数を明記した条件付き claim として読まれるべき (詳細は §7b の validation-sufficiency limitation 参照) |
| A §10 | bug_review (Step 11) — fired on `test Sharpe > 3` + state-change… 1 high finding (§5)… |

問題: 次に notebook を読むリーダー (= 自分自身を含む) は、研究の主張ではなく
「どのレビューで何が指摘され何を直したか」のメタ文脈を強制的に読まされる。
abstract が会議録になる。

## F2. レビュー用語が本文に残る

reviewer 名 / dimension 名 / severity / case 番号など、レビュー作法の語彙が
本文に出てくる。これは外向きの communication 文書としては漏れ。

| ケース | 抜粋 |
|---|---|
| A | 「bug_review の leakage-reviewer から high finding が出た」 |
| B | 「bug_review (case B) medium #1」「statistics-reviewer の low」 |
| C | 「Prior work and differentiation **(literature dimension)**」「claim-reviewer 指摘」「validation-sufficiency-reviewer 指摘 (§7b)」 |

問題: `case B`、`medium #1` のような番号は **fixture 命名規則由来** (我々が
findings ファイルに付けた接頭辞) であり、本来本文に出る情報ではない。
reviewer の dimension 分類はレビュー作法の内部用語であり、論文 / 共有可能な
研究記録としては不適切。

## F3. 当初構造に無い章番号が intercalary に乱立

新セルが必要になったとき、`§6a / §6b / §7b` のように **小数点番号** で
セクションを増設する習慣ができてしまっている。当初の figure plan
(`Fig 1〜Fig 6`) や notebook_narrative.md の主要セクション規定とずれる。

| ケース | 追加された章 |
|---|---|
| B | §6a (Sanity re-checks)、§6b (Daily gross exposure)、Fig 2b |
| C | §7b (Validation-sufficiency limitation) |

問題: `§6b` は figure plan に無いし、レビュー前のノート骨格にも無い。
「review 後にしか登場しない章」の存在自体が、ノートを review 前 / review 後の
2 状態に引き裂く。読者は当初骨格と review 反映後の追加章を頭の中で
仕分けする手間を負う。

## F4. 旧値 ↔ 新値の audit メモがコード / markdown に残る

修正後の値だけ書けばいいところを、旧値を audit 用に残す習慣が出る。

| ケース | 抜粋 |
|---|---|
| A code §7 | `walk_forward_sharpes_pre_fix = [1.8, 2.1, 2.4, 1.9, 2.7, 2.0, 2.6, 2.5]  # audit` |
| A md §7 | 「WF 平均 Sharpe は修正前 2.25 → 修正後 0.93 へ低下」 |
| A md §0 | 取り消し線 `~~2.4~~`、`~~3.1~~` に新数値併記 |

問題: marimo cell granularity は「one cell = one fit / one evaluation」を
規定しており、**前回値の audit はその責務に含まれない**。`pre_fix` 変数は
研究本筋では一切使われないコードノイズ。本文 markdown 上の「修正前→修正後」も
F1 の派生 (履歴本文化)。 audit が必要なら inline review summary
(= chat transcript) または `decisions.md` が定位置。

## F5. 「park した finding」「follow-up」「next-session で…」などタスク管理メモが本文化

| ケース | 抜粋 |
|---|---|
| B §7 | `**Parked finding** statistics-reviewer の low (N=8 では point estimate だけでは薄い → median / Q25 / Q75 を併記) は park。次の robustness 再走の際に Fig 4 box plot に headline 位置の hline を追加するタスクに紐付け、bug_review の medium 解消・battery 再走を優先する。` |
| C §7b | `**Follow-up (next-session, not run in this notebook)** F1 walk-forward を N ≥ 16 windows に拡張…F2 PSR / DSR を window 別 Sharpe の分布から計算…` |
| C §9 derived H 表 | 「`run-now` / `next-session` / `drop`」列、各行に「要追加 feature」「split 設計の見直しが要る」 |

問題: 「いつ何をやるか」「park したか run-now か」は **計画情報** であって、
notebook の研究記録としての役割ではない。`decisions.md` / `hypotheses.md` /
`hypothesis_cycles.md` 配下が本来の格納先。ノート本文に書かれると、読者は
「次に何をやるべきか」というタスクボードと、「この実験で何が分かったか」
という研究記録が同じセルから読まれる。

## F6. 修正後の数値と既存 figure / observation の不整合が放置される

| ケース | 不整合の所在 |
|---|---|
| A | §0 abstract / §3 H1 abstract / §7 / §9 は post-fix 数値を反映、しかし §8 の Fig 2 は placeholder 文字列のまま、observation cell は **修正後** に書き換えたが、Fig 自体は再生成 / 再走されたかは不明 |
| B | §3 H1 abstract と §0 abstract は post-fix 数値、しかし §8 Fig 2 / observation はオリジナルのまま (修正前 narrative) |
| C | §0 abstract と §3 abstract と §7b で「N=8 では識別不能」と書かれているが、§7 の数値も §8 figure も pre-review のまま、§9 interpretation だけ revise されている |

問題: 「コードを直す」と「ノート全体を再走する」は別物。エージェントは前者
(と本文の書き換え) は行うが、後者 (= 全セル再評価して figure / 数値が
最終状態に揃っていることの確認) は行っていない。これがユーザー指摘の
「整合性が悪い」の根幹。 marimo は reactive graph を持つので
**理論上は再走で揃うが、エージェントが「再走しました」と確認しないままノートを
"完成" として扱っている**。

## F7. スコープ外の問題は完全に不可視

| ケース | 残存問題 |
|---|---|
| B | §5 の whole-period leak は触らない (case B 起因では無いから)、しかし B の修正後の Sharpe 数値は **leaky pipeline 由来のまま**。abstract で「Sharpe ≈ 2.5 / 3.0」と claim している |
| C | §5 leak も §6 cost bug も触らない、abstract で「N=8 という条件付きで Sharpe = 2.4 / 3.1」と claim |

問題: review が**自分の triggering 範囲しか見ない**ため、過去ラウンドの
findings との整合チェックがない。ノートが累積してゆくと、レビュー反映の差分
がパッチ的に積み重なって、各 markdown が言及している「直前の修正」しか
反映していない一貫性の低い文書になる。

## F8. レビュー由来セルの位置が回ごとに違う

| ケース | 新セル位置 |
|---|---|
| A | 既存 §5 の中に observation cell を追加 (in-section) |
| B | §6a / §6b として独立セクション化 (新章) |
| C | §7b 独立セクション + §9 後ろに derived hypotheses 表 (新章 + 末尾) |

問題: 同じ「レビュー反映の追加セル」でも、毎回置き場所が違う。これは
**規定の不在**による。読者が「review 反映で増えたセルはここで読める」と
予測できないので、ノートの mental model を構築できない。

---

## 観察まとめ — GREEN phase で打つべき counters

ユーザーの 2 症状は、上の F1〜F8 が異なる経路で生み出している。
GREEN ではこれらを直接消す規定が要る:

| 失敗モード | GREEN で打つルール (案) |
|---|---|
| F1 編集履歴の本文化 | 本文 markdown には reviewer / finding / step 番号への言及を書かない (1 行マーカーで参照) |
| F2 レビュー用語の本文化 | reviewer 名 / dimension / severity / case 番号 は本文に出さない |
| F3 章番号 intercalary | 当初骨格 (§N / Fig N / `## H<id>`) を不変にする。新規追加は決められた 1 箇所 (`## Post-review addenda` または新 `## H<id>` ブロック) に集める |
| F4 audit メモ残存 | 旧値 / `pre_fix` / 取り消し線は本文 / コードに残さない。audit は inline review summary (chat) と `decisions.md` のみ |
| F5 タスクメモ本文化 | follow-up / park / next-session などの計画情報は `decisions.md` / `hypotheses.md` 側へ。本文には「結果」だけ |
| F6 数値 / figure 不整合 | レビュー反映の Definition of Done = 「依存セルすべて再走、figure / observation / abstract / verdict が同じ pipeline 出力に揃う」。dispatch protocol に追加 |
| F7 スコープ外残存 | レビュー反映後、ノート全体を 1 度通読する verification pass を要求。abstract と interpretation セルが直近 finding だけでなく **既知の全 finding** に整合しているか確認する |
| F8 セル位置の不統一 | レビュー反映の物理的場所は 4 パターンに正規化 (in-place rewrite / 同セクション末尾の re-compute セル / `## Post-review addenda` / 新 `## H<id>`)。判定は決められたフローチャートで |

これは GREEN phase で `references/post_review_reconciliation.md` (新規) +
`SKILL.md` Step 11 / 13 への 1 段落の補強 + `notebook_narrative.md` の
checklist 拡張で実装できる。
