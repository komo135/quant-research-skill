# GUARDRAILS — agent 失敗モードと構造的対策

このファイルは **agent が高確率でやらかす失敗** を列挙し、それぞれに **構造的な対策** を紐付けたもの。
セッション開始時に最初に読むこと。読まずに作業を始めると、以下の失敗を即座に犯す。

---

## ユーザが明示した 2 つの最重要失敗モード

### G1. 「すぐに楽に答えを出したがる」

**症状**:
- charter / pre-registration / 多重検定補正などの「重い手続き」を省略する
- promotion gate のチェック項目を「だいたい OK」で素通しする
- ユーザが急いでいる空気を感じると、規律を緩める
- "supported" / "matured" / "完了" の判定に bias する
- 1〜2 ファイル読んだだけで全体を把握したと宣言する

**構造対策**:
1. **どの promotion / gate / review も "全項目 pass のチェックリスト" を inline に貼り出す**。"reviewed and OK" のような summary 表現を禁止。各項目に対して具体的 evidence (file:line, metric value, hash) を書く。
2. **kill 基準が 1 つでも fire したら kill**。promote は全項目 pass を要求。非対称バイアスを構造で与える。
3. **ユーザの "急いでいる" シグナルに対して、deliverable の品質ではなく scope を縮める** ことで応える。"今日は smallest discriminating trial 1 個のみ"。手続きは省略しない。
4. **作業開始前に必ず「自分は何を見ていない」を書く**。"このセッションでは X / Y / Z を読んでいない、よって W について判断できない" を明示する。

### G2. 「表面情報だけですべてを把握したつもりになる」

**症状**:
- SKILL.md の frontmatter description だけ読んで内部構造を推測する
- ファイル一覧 (Glob 結果) だけ見て中身を読まずに「全体像はわかった」と宣言する
- reference の見出しだけ読んで本文を読まずに参照する
- スクリプトのファイル名だけ見て「PSR を計算する」と判断する (中身の実装と doc が乖離していることを見落とす)
- ユーザの過去発言を要約した自分の memory に基づいて判断する (実ファイルを読まない)

**構造対策**:
1. **判断の根拠は "今このセッションで実際に Read したファイルとその行番号" のみ**。memory 由来の知識に基づく判断は明示的に "未確認" タグを付ける。
2. **ファイル一覧やヘッダだけで判断する報告を禁止**。"X というスクリプトがある" は "X の中身を Read して行 N で Y を実装している" まで具体化しない限り、観察ではなく推測。
3. **CHARTER.md / DECISIONS.md / PROGRESS.md は毎セッション読み直す**。前セッションの記憶ではなく現ファイルを根拠にする。
4. **長い reference (>100 行) を読むときは、見出しだけのスキミングを禁止**。本文を順に読み、要約は agent ではなく Read 出力の引用に基づく。

---

## その他の高頻度失敗モード

### G3. 設計の事後変更 / 再交渉

**症状**: 実装中に「やっぱりこっちの設計のほうが良い」と気付き、CHARTER に反する変更を勝手に入れる。

**対策**:
- CHARTER.md は frozen。変更は CHARTER 内 "Amendments" にユーザ承認付きで append。
- 実装ファイルの先頭または該当箇所に "implements CHARTER §N" のコメントを書く。後でレビュー時に CHARTER と一致するか機械チェックできる。

### G4. 完了の宣言を急ぐ

**症状**: 半分終わったタスクを "完了" と PROGRESS に書く。テストを通さないまま "実装完了" と書く。

**対策**:
- PROGRESS.md の `[x]` (完了) 条件を厳格化: テスト pass + ledger validate pass + ユーザ承認 のすべて。
- 不確かな完了は `[~]` (部分完了、blocker XXX) で記録。

### G5. 進捗の捏造 / 想像

**症状**: 実際にはやっていない作業を "やった" と報告する。コードを書いたつもりになっているが Write していない。

**対策**:
- 報告内容に対し、対応する Write/Edit/Read のツールコール ID または file path を明示。
- "実装した" と言うときは Edit/Write の戻り値の hash または line count を引用。

### G6. ユーザに同意を求めるふりをして既に走り出す

**症状**: 「〜でよろしいですか?」と聞きながら、回答を待たずに次のステップを実行する。

**対策**:
- 質問を発したらそのターンで作業終了。ユーザの回答を受けてから次のターンで作業再開。
- AskUserQuestion ツールがある場合はそれを使う。

### G7. 過去のレビュー結果を見ずに同じ間違いを繰り返す

**症状**: 前のセッションで指摘されたバグを再導入する (例: psr_dsr の per-period vs annualized 混乱)。

**対策**:
- 該当ファイルを編集する前に DECISIONS.md と過去の audit 結果 (`docs/superpowers/specs/` および前回の audit 報告) を grep して、関連する決定を確認。

### G8. テンプレートの placeholder を残す

**症状**: `{{NEW_HYP_ID}}` を `?` で埋める、`TBD` のまま提出する、Lorem ipsum を残す。

**対策**:
- すべての template generation 後に `grep -E "(TBD|TODO|XXX|\\?\\?\\?|\\{\\{[^}]+\\}\\})"` を実行し、ヒットゼロを確認。

### G9. ファイル重複の放置

**症状**: `plugins/quant-research/skills/quant-research/` のような旧重複が残ったまま新ファイルを作る。

**対策**:
- ファイル作成前に Glob で類似名 / 重複位置をチェック。
- DECISIONS.md "D-3: 旧 plugins/ 重複ディレクトリは削除" を毎セッション再確認。

### G10. 引用と実装の乖離 (前回 audit の最大指摘)

**症状**: 「Politis & Romano 1994」と doc に書きながら Künsch 1989 の MBB を実装する。

**対策**:
- 数値ヘルパー実装時は **doc → code → test の 3 重一致** を確認。引用 paper の式を Read で開き、実装行と並べてレビューする。
- 引用の真偽が不明な場合は WebSearch で原典を確認してから書く。

### G11. 並列ツール呼び出しの忘却

**症状**: 独立した複数の Read を順次実行してコンテキストを浪費する。

**対策**:
- 独立タスクは同一メッセージ内で並列に発行。

### G12. プロトコル違反の隠蔽

**症状**: pre-registration の hash を後から書き換える、kill 基準 fire を見なかったことにする。

**対策**:
- すべての凍結は SHA-256 + timestamp で機械的に hash-locked。
- kill 基準 fire は append-only log。後からの編集は git diff で検出可能。

---

---

## 分析深度に関する失敗モード (DECISIONS D-11 / CHARTER C13 で追加)

### G13. 観察を結果と取り違える (A0 で停止)

**症状**:
- 「Sharpe 1.2 だった」を結果として報告し、analysis section を書かない
- 「動いた」「失敗した」「想定通り」を terminal な結論として扱う
- "We observed X" のあとに interpretation がない、あるいは数値の繰り返しだけがある

**構造対策**:
1. 各 trial の Analysis section を **テンプレート強制**: Observation / Decomposition / Evidence weighing / Tier rating / Gap to next tier の 5 項目すべてが埋まっていないと validate_ledger.py で error
2. 報告文書で "結果" と書く箇所には必ず **A2 以上 (≥1 競合説明) を併記** することを check item 化
3. promotion gate に "analysis_tier ≥ A4" を hard requirement で追加

### G14. 1 回の discriminating test で assertion (A5) を主張する

**症状**:
- A3 (1 つの discriminating evidence) を A5 (断言) と誤認する
- 「discriminating test を通したから supported」と判定する
- 単一 sub-period / 単一 instrument / 単一 metric で「機構を同定した」と書く

**構造対策**:
1. A4/A5 の判定基準を明示: A4 = 複数 source supporting evidence + scope conditions named, A5 = 複数 instrument + 複数 period + out-of-sample replicable + 外部 prediction 検証
2. promotion gate で "A5 主張は ≥3 種の独立証拠源" を check item 化
3. analysis_depth.md に「single discriminating test → A3 止まり」と明記

### G15. 成功側に generic terminal label を使う

**症状**:
- 「モデルが良かった」「regime に合っていた」「signal が強かった」「データが多かった」を成功の terminal explanation とする
- 失敗側では generic label decomposition の規律を守るのに、成功側では緩む

**構造対策**:
1. result_analysis.md に "成功側の generic label list" と decomposition 例を併記 (CHARTER C13 Amendment-1 の bad/good 表)
2. promotion gate で "成功要因が generic label でないこと" を check item 化
3. conclusion_review.md で "成功側 decomposition" を主要 axis に

### G16. 著者 narrative を evidence と取り違える

**症状**:
- 「論理的に明らかだから」「直感的に理解できるから」を evidence として扱う
- 自分が書いた解釈の文章を、後で読み返したときに observation と区別せずに引用する
- pre-registration で書いた expected diff を、結果が出た後に "確認した" と書くが実は数値検証していない

**構造対策**:
1. Analysis section の Evidence weighing 列に **"evidence type" を必須**: numerical / structural-argument / literature-reference / null-result-of-X のいずれかを明示
2. "structural-argument" のみで A4 主張は禁止 (numerical evidence ≥1 必須)
3. cold-eye review (conclusion_review の最終 section) で "narrative 由来の主張" を別カウントして flag

---

### G17. 過去 audit の前提を再確認せず引き継ぐ

**症状**:
- 「前回の audit で X と判断したから今回も X」と決定する
- 同じファイル / ディレクトリを再 Read せず memory で構造を述べる
- 削除・破壊的操作を行うときに対象の **現在の実態** を再確認しない

**実例 (2026-05-03)**:
前回 audit で `plugins/quant-research/skills/quant-research/` を「単なる重複」と判定し、CHARTER 起草時にもそのまま D-3 として「削除確定」と書いた。Phase 1 着手時に **再確認せずに削除を進めようとしたが、Glob で実態を見たら**:
- plugins/ は Claude Code / Codex の **publish 済み配布パッケージ**
- 中に `experiment-review` という別 skill が含まれていた (前回 audit では言及なし)
- 削除すれば公開済 plugin が破壊された

D-3 を D-12 で撤回。

**構造対策**:
1. **削除・破壊的操作の前に必ず Glob + Read で実態を再確認** する。memory での判断 (G2) を行わない。
2. 前 audit で「軽い重複」「単なるコピー」「廃止予定」と書いた対象についても、Phase 着手時に **改めて全 Glob → 必要なら Read** で実態確認。
3. **配布物 / publish 済み artifact は touch する前にユーザ確認**。次の major version まで遡及不能な変更は decision を frozen にする前にユーザに見せる。
4. CHARTER / DECISIONS の各エントリには「最終確認日」を記載するルールを検討 (将来 amendment)。

---

## このファイルへの追記ルール

agent が新たな失敗パターンに気付いたら、ここに append できる:

```
### G<N>. 失敗の名前
**症状**: ...
**対策**: ...
```

削除は禁止。失敗のリストが長くなることは健全。
